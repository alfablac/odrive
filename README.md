## odrive folder/file download

This is a downloader for sharepoint folder and files. Works on Windows/Linux.

Since authorization is given through the share URL, links must follow the format:

```https://<dominio>:f:/g/personal/<caminho>/<id>?e=<id>```

## Requirements

[python3](https://www.python.org/downloads/) + requests module + selenium module

``` pip install -r requirements.txt ``` 

should be enough to run this. aria2c and chromedriver binaries are included in the root path.

## Usage
```
usage: python3 odrive.py [-h] -u URL [-i] [-p PASSWORD] [-o OUTPUT]
odrive sharepoint file/folder downloader

required arguments:
  -u URL, --url URL  download url
optional arguments:
  -h, --help         
                        show this help message and exit
  -i, --interactive  
                        interactive mode (select which items to download)
  -p PASSWORD, --password PASSWORD
                        given folder password if it's needed
  -o OUTPUT, --output OUTPUT
                        output folder. Should work for either relative or absolute paths (Win/*nix)
```



## To-do

- [x] extract bit.ly
- [x] auto cookies export
- [x] recursive folder download (kinda. it works for one level of depth)
- [x] add support for folder locked with password 
- [x] dont add file to download list if it's already in the folder ("-i" option might covers that)


