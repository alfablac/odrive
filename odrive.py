import requests
import bs4
import re
import json
import subprocess
import argparse
from urllib.parse import quote


def get_folder_list(HTTP_ROOT, ROOT_FOLDER, ARROBA_1):
    API_URL = HTTP_ROOT + '/_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream?@a1=' + '%27{}%27&RootFolder={}&TryNewExperienceSingle=TRUE'.format(ARROBA_1.replace('/','%2F').replace('_','%5F'), quote(ROOT_FOLDER).replace('/','%2F').replace('_','%5F').replace('-','%2D'))
    # todo: better handling of unicode chars
    print("Primeiro POST para pegar inicio da lista")
    page_request = requests.post(url=API_URL, headers=HEADERS_JSON, cookies=auth_url.cookies, data=json.dumps(page_payload_json))
    page_request_json = json.loads(page_request.text)
    return page_request_json

COOKIE_BASE = "DOMAIN	FALSE	/	TRUE	0	FedAuth	AUTH    \n     DOMAIN	FALSE	/	FALSE	0	FeatureOverrides_enableFeatures	 \n   DOMAIN	FALSE	/	FALSE	0	FeatureOverrides_disableFeatures"
parser = argparse.ArgumentParser(
    description='odrive sharepoint file/folder downloader'
)
parser.add_argument('-u', '--url', help='url para download', required=True)
args = parser.parse_args()
BAIXAR = args.url

if 'bit.ly' in BAIXAR:
    extract_url = requests.get(url=BAIXAR)
    BAIXAR = extract_url.history[0].headers['location']

print("Baixando URL:")
print(BAIXAR)
auth_url = requests.get(url=BAIXAR)

HEADERS_COOKIES = auth_url.headers['Set-Cookie']
PCBROWSER_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
AUTH = re.search('(FedAuth=)(.+?)(\;)', HEADERS_COOKIES, re.IGNORECASE).group(2)
DOMAIN = re.search('(http(s?):\/\/)(.+?)(\/)', BAIXAR, re.IGNORECASE).group(3)

COOKIE_BASE = re.sub(r"DOMAIN", DOMAIN, COOKIE_BASE)
COOKIE_BASE = re.sub(r"AUTH", AUTH, COOKIE_BASE)

with open('cookies.txt', 'w') as f:
    f.write(COOKIE_BASE)

HEADERS_JSON = {
    'Accept': 'application/json;odata=verbose',
    'Accept-Language': 'en-US',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json;odata=verbose',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': PCBROWSER_UA,
    'Set-Cookie': HEADERS_COOKIES,
    'Referer': BAIXAR,
}
print("Fazendo request para autorização")
page_iq = requests.get(url=auth_url.url, headers=HEADERS_JSON, cookies=auth_url.cookies)
page_data = re.search('(var g_listData = )({.*})(\;)', page_iq.text, re.IGNORECASE | re.DOTALL).group(2)
page_payload = re.search('(var g_payload = )({.*})(\;)', page_iq.text, re.IGNORECASE).group(2)
page_payload_json = json.loads(page_payload)
page_data_json = json.loads(page_data)
uniqueid_list = []
HTTP_ROOT = page_data_json['HttpRoot']
if len(page_data_json['ListData']['Row']) > 0:
    ROOT_FOLDER = page_data_json['rootFolder']
else:
    ROOT_FOLDER = re.search('^(.+)\/([^/]+)$', page_data_json['rootFolder'], re.IGNORECASE).group(1)
ARROBA_1 = page_data_json['ListUrl']


page_request_json = get_folder_list(HTTP_ROOT, ROOT_FOLDER, ARROBA_1)
API_URL_REP = HTTP_ROOT + '/_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream?@a1=\'{}\'&TryNewExperienceSingle=TRUE'.format(ARROBA_1)

for data in page_request_json['ListData']['Row']:
    if data['FSObjType'] == '1':
        page_request_json = get_folder_list(HTTP_ROOT, data['FileRef'], ARROBA_1)
        for inside_data in page_request_json['ListData']['Row']:
            uniqueid_list.append(inside_data)
    else:
        uniqueid_list.append(data)

next_href = True
while next_href == True:
    if 'NextHref' in page_data_json['ListData']:
        print("Pegando próxima página de itens")
        page_iq = requests.post(url=API_URL_REP+page_data_json['ListData']['NextHref'].replace('?Paged','&Paged'), headers=HEADERS_JSON, cookies=auth_url.cookies, data=json.dumps(page_payload_json))
        page_data_json = json.loads(page_iq.text)
        for data in page_data_json['ListData']['Row']:
            uniqueid_list.append(data)
    else:
        next_href = False

print("Gerando lista de itens")
download_list = []
for data in uniqueid_list:
    download_list.append(HTTP_ROOT + '/_layouts/15/download.aspx?UniqueId=' + data['UniqueId'].replace('{','').replace('}',''))

with open('download_list.txt', 'w') as f:
    for data in download_list:
        f.write(data + '\n')

print("Chamando aria2c")
subprocess.call(["aria2c", "--dir=./", "--input-file=download_list.txt",
                 "--load-cookies=cookies.txt","--max-concurrent-downloads=1", "--connect-timeout=60",
                 "--max-connection-per-server=16", "--continue=true", "--split=16", "--min-split-size=1M",
                 "--human-readable=true", "--download-result=full", "--file-allocation=none"])

print(download_list)
