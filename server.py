import socket
import threading
import time 

# contains the size of the upcoming data
HEADER = 102400
FORMAT = "utf-8"
DISCONNECT = "EXIT!"

def make_file(filename, data):
    with open(filename, "wb") as fp:
        fp.write(data)
    
def handle_client(conn, addr):
    print("New Connection: ", addr)
    connected = True
    state: int = 0
    while connected:
        msg_sz = conn.recv(HEADER).decode(FORMAT)
        if msg_sz:
            state += 1
            msg_sz = int(msg_sz)
            msg = conn.recv(msg_sz).decode(FORMAT)
            if state == 1:
                filename = 'recv'+msg
            # Collect all data
            if state >= 2:
                done = False
                data = b''
                file_bytes = b' '
                while not done:
                    data += conn.recv(HEADER)
                    if (data[-4::] == b'END!'):
                        done = True
                        state=0
                    else:
                        file_bytes += data
                make_file(filename, data)
            if msg == DISCONNECT:
                connected=False
    conn.close()
    

def handle_server(server):
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print("Active Connections: ", threading.activeCount()-1)
    
def main():
    PORT = 9999
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    print("Server Starting...")
    handle_server(server)

    
    

if __name__ == "__main__":
    main()
