import requests
from requests.auth import HTTPBasicAuth

# Define the endpoint
url = 'http://localhost:8000/'

# Define the data you want to send in the POST request (as a dictionary)
data = {
    'key1': 'value1',
    'key2': 'value2'
}

# Define your credentials
username = 'username'
password = 'password'

# Make the POST request with Basic Authentication
response = requests.post(url, data=data, auth=HTTPBasicAuth(username, password))

# Print the status code and response content
print(f'Status Code: {response.status_code}')
print(f'Response Content: {response.text}')
