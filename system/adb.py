import os
import argparse
import subprocess
from os import environ
from .style import Style
from .burp import BurpHelper
from .crypt import CryptHelper


class ADB:
    __adb_path = None

    def __init__(self, base_dir: str):
        self.__crypt = CryptHelper(base_dir)
        self.__base_dir = base_dir
        self.__cert_dir = os.path.join(base_dir, "certs")
        self.__adb_path = self.__find_adb()
        # Start the ADB server
        self.start_server()

    def get_adb_path(self):
        return self.__adb_path

    def __find_adb(self) -> str | FileNotFoundError:
        """Find the adb executable in the PATH environment variable

        Raises:
            FileNotFoundError: If the adb executable is not found in the PATH environment variable or local directory

        Returns:
            _type_: str -- The path to the adb executable
        """
        # Check the local directory first
        adb_path_linux = os.path.join(self.__base_dir, "bin", "adb")
        adb_path_win = os.path.join(self.__base_dir, "bin", "adb.exe")
        if os.path.exists(adb_path_linux):
            return adb_path_linux
        elif os.path.exists(adb_path_win):
            return adb_path_win

        # Check the PATH environment variable
        for path in os.getenv("PATH").split(os.pathsep):
            adb_path_linux = os.path.join(path, "adb")
            adb_path_win = os.path.join(path, "adb.exe")
            if os.path.exists(adb_path_linux):
                return adb_path_linux
            elif os.path.exists(adb_path_win):
                return adb_path_win
        raise FileNotFoundError("adb not found in PATH")

    def start_server(self) -> None:
        """Start the ADB server
        :return: None
        """
        # Run without printing the output
        subprocess.run([self.__adb_path, "start-server"], capture_output=True)

    def list_devices(self, *args) -> tuple[int, list]:
        """List all connected devices
        :return: Tuple[int, str] -- The return device count and the device list
        """
        result = subprocess.run(
            [self.__adb_path, "devices"], capture_output=True, text=True
        )
        output = result.stdout.strip()
        count = len(output.split("\n")) - 1
        devices = output.split("\n")[1:]
        # Format the device list
        devices = [device.replace("\tdevice", "") for device in devices]
        return count, devices

    def __get_device_state(self, device_id: str) -> str:
        """Get the state of a device
        :param device_id: str -- The device ID
        :return: str -- The state of the device
        """
        result = subprocess.run(
            [self.__adb_path, "-s", device_id, "get-state"],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def __get_device_model(self, device_id: str) -> str:
        """Get the model of a device
        :param device_id: str -- The device ID
        :return: str -- The model of the device
        """
        result = subprocess.run(
            [self.__adb_path, "-s", device_id, "shell", "getprop", "ro.product.model"],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def __get_device_serial(self, device_id: str) -> str:
        """Get the serial number of a device
        :param device_id: str -- The device ID
        :return: str -- The serial number of the device
        """
        result = subprocess.run(
            [self.__adb_path, "-s", device_id, "get-serialno"],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def __get_device_android_version(self, device_id: str) -> str:
        """Get the android version of a device
        :param device_id: str -- The device ID
        :return: str -- The android version of the device
        """
        result = subprocess.run(
            [
                self.__adb_path,
                "-s",
                device_id,
                "shell",
                "getprop",
                "ro.build.version.release",
            ],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def __get_device_android_sdk_version(self, device_id: str) -> str:
        """Get the android sdk version of a device
        :param device_id: str -- The device ID
        :return: str -- The android sdk version of the device
        """
        result = subprocess.run(
            [
                self.__adb_path,
                "-s",
                device_id,
                "shell",
                "getprop",
                "ro.build.version.sdk",
            ],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def __get_device_manufacturer(self, device_id: str) -> str:
        """Get the manufacturer of a device
        :param device_id: str -- The device ID
        :return: str -- The manufacturer of the device
        """
        result = subprocess.run(
            [
                self.__adb_path,
                "-s",
                device_id,
                "shell",
                "getprop",
                "ro.product.manufacturer",
            ],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def get_device_info_dict(self, device_id: str, *args) -> dict:
        """Get all information of a device
        :param device_id: str -- The device ID
        :return: dict -- The information of the device
        """
        return {
            "model": self.__get_device_model(device_id),
            "serial": self.__get_device_serial(device_id),
            "android_version": self.__get_device_android_version(device_id),
            "android_sdk_version": self.__get_device_android_sdk_version(device_id),
            "manufacturer": self.__get_device_manufacturer(device_id),
        }

    def get_pretty_device_info(self, device_id: str, *args) -> str:
        """Get all information of a device in a pretty format
        :param device_id: str -- The device ID
        :return: str -- The information of the device
        """
        device_info = self.get_device_info_dict(device_id)
        return f"{Style.BOLD}Name:{Style.RESET} {device_info['manufacturer']} {device_info['model']} SDK-{device_info['android_sdk_version']}\n{Style.BOLD}Serial:{Style.RESET} {device_info['serial']}\n{Style.BOLD}Android Version:{Style.RESET} {device_info['android_version']}"

    def run_adb_command(self, *args) -> str:
        """Run an adb command on a device
        :param device_id: str -- The device ID
        :param command: str -- The command to run
        :return: str -- The output of the command
        """
        # Check args.device
        command_args = args[0]

        result = subprocess.run(
            [self.__adb_path, "-s", command_args.device, "shell", command_args.command],
            capture_output=True,
            text=True,
        )
        # Check if the command is valid
        if result.returncode != 0:
            return f"{Style.RED}[Error] {result.stderr.strip()}{Style.RESET}"
        return result.stdout.strip()

    def __push_file(self, device_id: str, local_file: str, remote_file: str) -> str:
        """Push a file to a device
        :param device_id: str -- The device ID
        :param local_file: str -- The path to the local file
        :param remote_file: str -- The path to the remote file
        :return: str -- The output of the command
        """
        result = subprocess.run(
            [self.__adb_path, "-s", device_id, "push", local_file, remote_file],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def install_ca_cert(self, *args) -> str:
        """Install the Burp CA certificate on a device
        :param device_id: str -- The device ID
        :return: str -- The output of the command
        """
        cli_args = args[0]
        # Download the certificate
        ca_cert_path = BurpHelper.download_certificate(
            self.__cert_dir, cli_args.host, cli_args.port
        )
        # Convert the certificate from DER to PEM
        pem_cert_path = os.path.join(self.__cert_dir, "burp_cacert.pem")
        self.__crypt.convert_der_to_pem(ca_cert_path, pem_cert_path)
        old_subject_hash = self.__crypt.extract_old_subject_hash(pem_cert_path)

        # Push the certificate to the device
        remote_cert_path = f"/data/local/tmp/{old_subject_hash}.0"
        self.__push_file(cli_args.device, pem_cert_path, remote_cert_path)
        print(
            f"{Style.GREEN}[SUCCESS] Pushed certificate to {remote_cert_path}{Style.RESET}\n"
        )

        # Install the certificate
        result = subprocess.run(
            [
                self.__adb_path,
                "-s",
                cli_args.device,
                "shell",
                "su",
                "-c",
                f'"mount -o rw,remount /system && mv {remote_cert_path} /system/etc/security/cacerts/"',
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"{Style.RED}[Error] {result.stderr.strip()}{Style.RESET}")
            print(f"{Style.CYAN}[INFO] Trying to remount the file system{Style.RESET}")
            # Find the mount point
            root_mount_point = subprocess.run(
                [
                    self.__adb_path,
                    "-s",
                    cli_args.device,
                    "shell",
                    "su -c",
                    "\"cat /proc/mounts | grep -i ' / '\"",
                ],
                capture_output=True,
                text=True,
            )
            output = root_mount_point.stdout.strip()
            if output == "":
                print(f"{Style.RED}[Error] Could not find the mount point{Style.RESET}")
            else:
                mount_point = output.split(" ")[0]
                print(
                    f"{Style.GREEN}[SUCCESS] Found the mount point: {mount_point}{Style.RESET}"
                )
                # Remount the file system
                print(f"{Style.CYAN}[INFO] Remounting the file system{Style.RESET}")
                result = subprocess.run(
                    [
                        self.__adb_path,
                        "-s",
                        cli_args.device,
                        "shell",
                        "su -c",
                        f'"mount -o rw,remount {mount_point}"',
                    ],
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    print(f"{Style.RED}[Error] {result.stderr.strip()}{Style.RESET}")
                else:
                    print(
                        f"{Style.GREEN}[SUCCESS] Remounted the file system{Style.RESET}\n"
                    )
                    # Try to install the certificate again
                    result = subprocess.run(
                        [
                            self.__adb_path,
                            "-s",
                            cli_args.device,
                            "shell",
                            "su",
                            "-c",
                            f'"mv {remote_cert_path} /system/etc/security/cacerts/"',
                        ],
                        capture_output=True,
                        text=True,
                    )
                    if result.returncode != 0:
                        print(
                            f"{Style.RED}[Error] {result.stderr.strip()}{Style.RESET}"
                        )
                    else:
                        print(
                            f"{Style.GREEN}[SUCCESS] Installed certificate on the device{Style.RESET}"
                        )
        else:
            print(
                f"{Style.GREEN}[INFO] Installed certificate on the device{Style.RESET}"
            )

        # Clean up the downloaded files
        print(f"{Style.MAGENTA}[INFO] Cleaning up the downloaded files{Style.RESET}")
        os.remove(ca_cert_path)
        os.remove(pem_cert_path)

    # Arg parser
    @staticmethod
    def add_parser(adb, subparsers):
        parser = subparsers.add_parser("adb", help="ADB commands")

        subparsers = parser.add_subparsers(dest="subcommand", help="Subcommands")
        # List all devices
        devices_list_parser: argparse.ArgumentParser = subparsers.add_parser(
            "devices", help="List all connected devices"
        )
        devices_list_parser.set_defaults(
            func=ADBView.print_devices, args=adb.list_devices()
        )

        # Run a command on a device
        run_parser = subparsers.add_parser("run", help="Run an adb command")
        # Run an adb command
        run_parser.add_argument(
            "-d", "--device", type=str, help="The device ID", required=False, default=""
        )
        run_parser.add_argument(
            "-c", "--command", type=str, help="The command to run", required=True
        )
        run_parser.set_defaults(
            func=ADBView.print_command_output, child_func=adb.run_adb_command
        )

        # Install the Burp CA certificate on a device
        install_cert_parser = subparsers.add_parser(
            "install-cert", help="Install the Burp CA certificate on a device"
        )
        install_cert_parser.add_argument(
            "-d", "--device", type=str, help="The device ID", default=""
        )
        install_cert_parser.add_argument(
            "-u",
            "--host",
            type=str,
            help="The host where Burp Suite is running (default: localhost)",
            default="localhost",
        )
        install_cert_parser.add_argument(
            "-p",
            "--port",
            type=int,
            help="The port where Burp Suite is running (default: 8080)",
            default=8080,
        )
        install_cert_parser.set_defaults(func=adb.install_ca_cert)
        return parser


class ADBView:

    @staticmethod
    def print_devices(data: tuple[int, list]):
        count, devices = data
        print(f"{Style.BOLD}Connected devices: {count}{Style.RESET}")
        for device in devices:
            print(f" - {Style.GREEN}{device}{Style.RESET}")

    @staticmethod
    def print_device_info(device_info):
        print(f"{Style.BOLD}Device Info{Style.RESET}")
        print(device_info)

    @staticmethod
    def print_command_output(output):
        print(f"{Style.BOLD}Output{Style.RESET}")
        print(output)


# Test the ADB class
if __name__ == "__main__":
    adb = ADB()
    # print(adb.get_adb_path())
    count, devices = adb.list_devices()
    first_device = devices[0]

    print(adb.get_pretty_device_info(first_device))

    print(adb.run_adb_command(first_device, "whoami"))
