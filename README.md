## odrive folder/file download

This is a downloader for sharepoint folder and files. Works on Windows/Linux.
Since authorization is giving through the share URL, links must follow the format:
```https://<dominio>:f:/g/personal/<caminho>/<id>?e=<id>```

## Requirements

- python3 + requests module
- [aria2c](https://github.com/aria2/aria2/releases/tag/release-1.35.0) on PATH

## Usage
```bash
python3 odrive.py -u <URL>
```

## To-do

- [x] extract bit.ly
- [x] auto cookies export
- [x] recursive folder download (kinda. it works for one level of depth)
- [ ] dont add file to download list if it's already in the folder


