from .burp import BurpHelper
from style import Style
import os
import subprocess


class CryptHelper:
    __openssl_path = None

    def __init__(self, base_dir):
        self.__base_dir = base_dir
        self.__openssl_path = self.__find_openssl()

    def get_openssl_path(self):
        return self.__openssl_path

    def __find_openssl(self):
        """Find the openssl executable in the PATH environment variable

        Raises:
            FileNotFoundError: If the openssl executable is not found in the PATH environment variable or local directory

        Returns:
            _type_: str -- The path to the openssl executable
        """
        # Check the local directory first
        openssl_path_linux = os.path.join(self.__base_dir, "bin", "openssl")
        openssl_path_win = os.path.join(self.__base_dir, "bin", "openssl.exe")
        if os.path.exists(openssl_path_linux):
            return openssl_path_linux
        elif os.path.exists(openssl_path_win):
            return openssl_path_win

        # Check the PATH environment variable
        for path in os.getenv("PATH").split(os.pathsep):
            openssl_path_linux = os.path.join(path, "openssl")
            openssl_path_win = os.path.join(path, "openssl.exe")
            if os.path.exists(openssl_path_linux):
                return openssl_path_linux
            elif os.path.exists(openssl_path_win):
                return openssl_path_win
        raise FileNotFoundError("openssl not found in PATH")

    def convert_der_to_pem(self, der_file: str, pem_file: str):
        """Convert a DER certificate to a PEM certificate using the openssl executable

        Arguments:
            der_file {str} -- The path to the DER certificate file
            pem_file {str} -- The path to save the PEM certificate file
        """
        cmd = f"{self.__openssl_path} x509 -inform DER -outform PEM -in {der_file} -out {pem_file}"
        result = subprocess.run(cmd, shell=True, check=True)
        if result.returncode == 0:
            print(
                f"{Style.GREEN}[SUCCESS] Certificate converted successfully as {pem_file}{Style.RESET}"
            )
        else:
            print(f"{Style.RED}Failed to convert certificate{Style.RESET}")
            print(result.stderr)
            exit(1)

    def extract_old_subject_hash(self, pem_file: str) -> str:
        """Extract the old subject hash from a PEM certificate

        Arguments:
            pem_file {str} -- The path to the PEM certificate file

        Returns:
            str -- The old subject hash
        """
        cmd = f"{self.__openssl_path} x509 -noout -subject_hash_old -in {pem_file}"
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
        if result.returncode == 0:
            # Get the old subject hash from the output like head -n -1
            return result.stdout.decode().strip()
        else:
            print(f"{Style.RED}Failed to extract old subject hash{Style.RESET}")
            print(result.stderr)
            exit(1)