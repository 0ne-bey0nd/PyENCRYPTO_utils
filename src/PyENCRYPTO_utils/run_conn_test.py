import subprocess

if __name__ == '__main__':
    client_process = subprocess.Popen(['python', 'new_conn.py', '--role', '1', '--port', '65432'])
    server_process = subprocess.Popen(['python', 'new_conn.py', '--role', '0', '--port', '65432'])

    client_process.wait()
    server_process.wait()

    print("end of main")
    ...
