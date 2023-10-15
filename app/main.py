import socket


def main():
    # Create a TCP socket bound to local host
    with socket.create_server(("127.0.0.1", 4221), reuse_port=True) as server_socket:
        client_socket, _ = server_socket.accept() # wait for client
        client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
