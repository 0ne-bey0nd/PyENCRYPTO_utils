import subprocess

server_process = subprocess.Popen(["python", "test_server.py"])
client_process = subprocess.Popen(["python", "test_client.py"])

server_process.wait()
client_process.wait()

print("test finished")

