import ftplib
import json

def download_json_from_ftp(ftp_host, ftp_user, ftp_passwd, remote_path):
    # Connect to the FTP server
    with ftplib.FTP(ftp_host) as ftp:
        ftp.login(ftp_user, ftp_passwd)

        # Download the JSON file
        with open('downloaded_file.json', 'wb') as local_file:
            ftp.retrbinary(f"RETR {remote_path}", local_file.write)

        # Read the downloaded file
        with open('downloaded_file.json', 'r') as local_file:
            json_data = json.load(local_file)
            print(f"Downloaded JSON data: {json_data}")


ftp_host = 'localhost'  # Localhost for testing
ftp_user = 'testuser'
ftp_passwd = 'testpass'
remote_path = '/file.json'  # Ensure this path exists or modify as needed

download_json_from_ftp(ftp_host, ftp_user, ftp_passwd, remote_path)
