import ftplib
import json
import io

def upload_json_to_ftp(json_data, file_name, ftp_host, ftp_user, ftp_passwd, remote_path):
    json_string = json.dumps(json_data)

    try:
        # Connect to the FTP server
        with ftplib.FTP(ftp_host) as ftp:
            ftp.login(ftp_user, ftp_passwd)

            # Upload the JSON file as a file-like object
            with io.BytesIO(json_string.encode()) as file:
                ftp.storbinary(f"STOR {file_name}", file)
                print(f"File {file_name} uploaded to {remote_path} successfully.")

    except ftplib.all_errors as e:
            print(f"FTP error: {e}")

# Example usage:
ftp_host = 'localhost'  # Localhost for testing
ftp_user = 'testuser'
ftp_passwd = 'testpass'
remote_path = '/'  # Ensure this path exists or modify as needed
file_name = 'file.json'

# Example JSON data
json_data = {
    'name': 'John Doe',
    'email': 'johndoe@example.com',
    'age': 30
}

upload_json_to_ftp(json_data, file_name, ftp_host, ftp_user, ftp_passwd, remote_path)
