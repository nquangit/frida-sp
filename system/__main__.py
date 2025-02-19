from .adb import ADB
from style import Style


adb = ADB()
count, devices = adb.list_devices()
print(f"{Style.BOLD}Connected devices:{Style.RESET}")
for device in devices:
    print(f"  {device}")
print(f"{Style.BOLD}Total devices:{Style.RESET} {Style.GREEN}{count}{Style.RESET}")
