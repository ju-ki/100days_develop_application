import os
import socket

HOST = 'localhost'
PORT = 8000
BASE_DIR = './public'

address = (HOST, PORT)

# TODO: create_response渡ってきたメッセージはログに出力して、contentだけsendできるようにする

def find_available_ports(start_port, end_port):
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((HOST, port)) != 0:
                return port

def connect_to_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as  s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)

        print(f'Server started at {host}:{port}')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print('No data received')
                        break
                    request_lines = data.decode('UTF-8', errors='ignore').splitlines()
                    if not request_lines:
                        print('No request line found')
                        continue

                    parts = request_lines[0].split()
                    if len(parts) < 3:
                        print(f'Invalid request line: {request_lines[0]}')
                        continue

                    method, path, _ = parts
                    if path == '/':
                        path = '/index.html'
                    print(f'Request: {method} {path}')
                    response = create_response(path)
                    conn.sendall(response)
            finally:
                print('Connection closed')
                conn.close()
                s.close()
                print('Server stopped')

def create_response(path):
    print('Executing create response')
    full_path = BASE_DIR + path
    print(f'Full path: {full_path}')
    if os.path.isfile(full_path):
        with open(full_path, 'rb') as f:
            body = f.read()
        if full_path.endswith('.html'):
            content_type = 'text/html'
        elif full_path.endswith('.css'):
            content_type = 'text/css'
        elif full_path.endswith('.js'):
            content_type = 'application/javascript'
        header = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode()
    else:
        body = b'404 not found'
        header = b'HTTP/1.1 404 Not Found\r\n'
    return header + body
try:
    connect_to_server(HOST, PORT)
except OSError as e:
    print(f'Error: {e}')
    print('Port is already in use, finding an available port...')
    available_port = find_available_ports(PORT + 1, PORT + 100)
    if available_port:
        print(f'Using available port: {available_port}')
        address = (HOST, available_port)
        print(f'Restarting server at {HOST}:{available_port}')
        connect_to_server(HOST, available_port)
    else:
        print('No available ports found. Exiting.')
        exit(1)