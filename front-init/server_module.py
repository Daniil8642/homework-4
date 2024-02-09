# server_module.py

import http.server
import socketserver
import threading
import json
import socket
from datetime import datetime

# Конфігурація HTTP-сервера
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Визначаємо обробку запитів GET для різних URL-шляхів
        if self.path == '/':
            self.path = 'index.html'
        elif self.path == '/message':
            self.path = 'message.html'
        elif self.path == '/style.css':
            self.path = 'style.css'
        elif self.path == '/logo.png':
            self.path = 'logo.png'
        else:
            # Якщо URL не знайдено, повертаємо помилку 404
            self.send_error(404, "Not Found")
            return
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Конфігурація сервера сокетів
class SocketServerThread(threading.Thread):
    def __init__(self):
        super(SocketServerThread, self).__init__()
        # Створюємо сокет для обробки датаграмних (UDP) пакетів
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('localhost', 5000))

    def run(self):
        # Безперервно обробляємо датаграми, що приходять
        while True:
            data, addr = self.server_socket.recvfrom(1024)
            message_dict = json.loads(data.decode('utf-8'))
            save_message_to_json(message_dict)

# Функція для збереження повідомлення в форматі JSON
def save_message_to_json(message_dict):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    with open('storage/data.json', 'r') as file:
        data = json.load(file)

    # Додаємо нове повідомлення до існуючих даних
    data[timestamp] = {
        "username": message_dict['username'],
        "message": message_dict['message']
    }

    with open('storage/data.json', 'w') as file:
        json.dump(data, file, indent=2)

# Функція для створення HTTP-сервера
def create_http_server():
    handler = MyHttpRequestHandler
    return socketserver.TCPServer(('localhost', 3000), handler)

# Функція для створення потоку для сервера сокетів
def create_socket_server_thread():
    return SocketServerThread()
