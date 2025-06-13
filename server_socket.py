import socket
import json
import subprocess


def handle_command(cmd):
    action = cmd.get("action")
    if action == "click":
        x = cmd.get("x")
        y = cmd.get("y")
        if x is not None and y is not None:
            print(f"🖱️ Thực hiện click tại ({x}, {y})")
            subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
        else:
            print("⚠️ Thiếu tọa độ x hoặc y")
    else:
        print(f"⚠️ Hành động không hỗ trợ: {action}")


def start_server():
    host = '127.0.0.1'
    port = 9000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"🖥️ Server đang lắng nghe tại {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"🔌 Kết nối từ: {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break

        try:
            msg = data.decode()
            json_data = json.loads(msg)
            print(f"📥 Nhận lệnh JSON: {json_data}")
            handle_command(json_data)  # <-- Gọi xử lý tại đây
        except json.JSONDecodeError:
            print("❌ Dữ liệu không phải JSON")

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    start_server()
