from style import Style
from requests import get, RequestException
from os import path, makedirs


class BurpHelper:

    @staticmethod
    def download_certificate(cert_dir: str, host: str, port: int) -> str:
        """Download the Burp Suite CA certificate from the specified host and port

        Arguments:
            cert_dir {str} -- The directory to save the certificate
            host {str} -- The host where Burp Suite is running
            port {int} -- The port where Burp Suite is running

        Returns:
            str -- The path to the downloaded certificate
        """
        # Check if the directory exists then create it
        if not path.exists(cert_dir):
            print(f"{Style.YELLOW}[INFO] Creating directory: {cert_dir}{Style.RESET}")
            makedirs(cert_dir)

        try:
            url = f"http://{host}:{port}/cert"
            response = get(url, timeout=10)
            if response.status_code == 200:
                file_path = path.join(cert_dir, "burp_cacert.der")
                with open(file_path, "wb") as cert_file:
                    cert_file.write(response.content)
                print(
                    f"{Style.GREEN}[SUCCESS] Certificate downloaded successfully as {file_path}{Style.RESET}"
                )
                return file_path
            else:
                print(
                    f"{Style.RED}[ERROR] Failed to download certificate. Status code: {response.status_code}{Style.RESET}"
                )
                raise RequestException("Failed to download certificate")
        except RequestException as e:
            print(f"{Style.RED}Error downloading certificate: {e}{Style.RESET}")
            exit(1)
