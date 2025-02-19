# Just a simple Frida/ADB support tool for Android

## Requirements

-   Python 3

## Installation

```bash
virtualenv -p python3 venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Usage

```bash
python main.py --help
```

```
                                                     / ,e,   d8
888-~88e  e88~-888 888  888   /~~~8e  888-~88e e88~88e  "  _d88__
888  888 d888  888 888  888       88b 888  888 888 888 888  888
888  888 8888  888 888  888  e88~-888 888  888 "88_88" 888  888
888  888 Y888  888 888  888 C888  888 888  888  /      888  888
888  888  "88_-888 "88_-888  "88_-888 888  888 Cb      888  "88_/
               888                              Y8""8D

                    Created by: @nquangit

usage: main.py [-h] {adb} ...

Frida/ADB automation tool

positional arguments:
  {adb}       Commands
    adb       ADB commands

options:
  -h, --help  show this help message and exit
```
