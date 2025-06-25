import time

def run_test_for_app(app_name, serial):
    logs = []
    for i in range(5):
        log = f"[{serial}] Testing {app_name}... step {i+1}"
        print(log)
        logs.append(log)
        time.sleep(1)
    return {
        "serial": serial,
        "app": app_name,
        "status": "PASSED",
        "log": logs
    }
