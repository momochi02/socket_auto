import socket
import json
import time

def start_client():
    host = '127.0.0.1'
    port = 9000

    time.sleep(1)  # Đợi server khởi động

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("📲 Client kết nối đến server")

    # Gửi JSON lệnh
    command = {
        "action": "tap",
        "x": 100,
        "y": 200
    }
    message = json.dumps(command)
    client_socket.send(message.encode())
    print(f"📤 Gửi lệnh: {command}")


    client_socket.close()

if __name__ == "__main__":
    start_client()
