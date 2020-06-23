## odrive folder/file download

This is a downloader for sharepoint folder and files. Works on Windows/Linux.

Since authorization is given through the share URL, links must follow the format:

```https://<dominio>:f:/g/personal/<caminho>/<id>?e=<id>```

## Requirements

- python3 + requests module + selenium module
- [aria2c](https://github.com/aria2/aria2/releases/tag/release-1.35.0) on PATH
- [chromedriver](https://chromedriver.storage.googleapis.com/index.html?path=83.0.4103.39/) on PATH

## Usage
```bash
usage: python3 odrive.py [-h] -u URL [-i] [-p PASSWORD]
odrive sharepoint file/folder downloader

required arguments:
  -u URL, --url URL  download url
optional arguments:
  -h, --help         
                        show this help message and exit
  -i, --interactive  
                        interactive mode (select which items to download)
  -p PASSWORD, --password PASSWORD
                        passando senha se preciso
```

## To-do

- [x] extract bit.ly
- [x] auto cookies export
- [x] recursive folder download (kinda. it works for one level of depth)
- [x] add support for folder locked with password 
- [ ] dont add file to download list if it's already in the folder


