import argparse

from system import ADB
from system import Style
from os import path

adb = None
parser = None

BASE_DIR = path.dirname(path.abspath(__file__))


def banner():
    x = f"""{Style.CYAN}                                                     / ,e,   d8   
888-~88e  e88~-888 888  888   /~~~8e  888-~88e e88~88e  "  _d88__ 
888  888 d888  888 888  888       88b 888  888 888 888 888  888   
888  888 8888  888 888  888  e88~-888 888  888 "88_88" 888  888   
888  888 Y888  888 888  888 C888  888 888  888  /      888  888   
888  888  "88_-888 "88_-888  "88_-888 888  888 Cb      888  "88_/ 
               888                              Y8""8D            

                    {Style.RESET}{Style.MAGENTA}{Style.UNDERLINE}Created by: @nquangit{Style.RESET}
"""
    print(x)


def init():
    global adb
    try:
        adb = ADB(BASE_DIR)
    except Exception as e:
        print(Style.RED + "Error: " + str(e) + Style.RESET)
        exit(1)


def arg_parse():
    global adb
    global parser
    parser = argparse.ArgumentParser(description="Frida/ADB automation tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    ADB.add_parser(adb, subparsers)
    return parser.parse_args()


def main():
    global adb
    global parser

    cli_args = arg_parse()
    if hasattr(cli_args, "func"):
        if hasattr(cli_args, "child_func"):
            cli_args.func(cli_args.child_func(cli_args))
        elif hasattr(cli_args, "args"):
            cli_args.func(cli_args.args)
        else:
            cli_args.func(cli_args)
    else:
        parser.print_help()


if __name__ == "__main__":
    banner()
    init()
    main()
    print()
