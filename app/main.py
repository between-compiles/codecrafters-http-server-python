import socket


def main():
    # Create a TCP socket bound to local host
    with socket.create_server(("127.0.0.1", 4221), reuse_port=True) \
        as server_socket:
        
        while True:
            # Wait for the client connection
            client_socket, _ = server_socket.accept()

            # Get the data (as bytes) from the client socket
            client_data_buffer = client_socket.recv(4096)

            # Decode the bytes using UTF-8
            raw_http_request = client_data_buffer.decode("utf-8")
            
            # The HTTP message start line is the first line in the HTTP request
            request_line = raw_http_request.split("\r\n")[0]

            # Get the path from the HTTP message start line
            path = request_line.split(" ")[1]

            # Get the HTTP header fields
            header_fields = {}
            for field in raw_http_request.split("\r\n"):
                if ":" in field:
                    field_name, _, field_value = field.partition(":")
                    header_fields[field_name] = field_value.strip()

            # Handle the request
            if path == "/":
                client_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode("ascii"))
            elif path.startswith("/echo/"):
                resp = bytearray()
                resp.extend("HTTP/1.1 200 OK\r\n".encode("ascii"))
                resp.extend("Content-Type: text/plain\r\n".encode("ascii"))
                # Take everything after /echo/
                body = f"{path.partition('/echo/')[2]}".encode("utf-8")
                resp.extend(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
                resp.extend(body)
                client_socket.send(resp)
            elif path.startswith("/user-agent"):
                resp = bytearray()
                resp.extend("HTTP/1.1 200 OK\r\n".encode("ascii"))
                resp.extend("Content-Type: text/plain\r\n".encode("ascii"))
                body = f"{header_fields['User-Agent']}".encode("utf-8")
                resp.extend(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
                resp.extend(body)
                client_socket.send(resp)
            else:
                client_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode("ascii"))
            client_socket.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye!")
