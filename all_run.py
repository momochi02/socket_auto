import threading
import subprocess
import time

def run_server():
    subprocess.run(["python3", "server_socket.py"])  # dùng python3 nếu cần

def run_client():
    time.sleep(2)  # Đợi server chạy ổn định
    subprocess.run(["python3", "client_socket.py"])

t1 = threading.Thread(target=run_server)
t2 = threading.Thread(target=run_client)

t1.start()
t2.start()

t1.join()
t2.join()
