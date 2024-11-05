import socket
import ssl

# Define the host and port
host = 'makeup.md'  # The hostname of the website
port = 443  # The HTTPS port (443)

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Wrap the socket with SSL for HTTPS
    context = ssl.create_default_context()
    with context.wrap_socket(sock, server_hostname=host) as ssock:
        # Connect to the server
        ssock.connect((host, port))

        request = f"GET /product/795029/ HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

        # Send the request
        ssock.sendall(request.encode())

        # Receive the full response from the server
        response = b""
        while True:
            data = ssock.recv(4096)  # Receiving data in chunks
            if not data:
                break
            response += data

# Split the headers and body
response_str = response.decode()
headers, body = response_str.split("\r\n\r\n", 1)

# Now `body` contains the HTML response, you can pass it to your scraping logic
print(body)
