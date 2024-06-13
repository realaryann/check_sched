import socket
import os

HEADER = 102400
FORMAT = "utf-8"
DISCONNECT = "EXIT!"

def handle_format(msg: str) -> bool:
    if (msg[-4::] not in (".pdf", ".PDF")):
        print(f"ERROR: Unsupported file format '{msg[-4::]}', only PDF files are accepted")
        return False
    return True

def open_file(msg: str):
    try:
        file_n = open(msg, "rb")
        return file_n
    except:
        print(f'ERROR: File {msg} unable to open')
        
def send(client) -> None:
    # Must send a .PDF/.pdf file
    # Name of file, its data, Message to show end of file
    msg = input()
    # Handle if the inputed file does not have .png format
    if handle_format(msg):
        file = open_file(msg)
        file_size = int(os.path.getsize(msg))
        ## Size of filename -> Filename -> Size of file -> File -> Terminate
        file_name_size = str(len(msg)).encode(FORMAT)
        file_name_size += b' ' * (HEADER - len(file_name_size))
        client.send(file_name_size)
        client.send(msg.encode(FORMAT))
        
        file_size = str(file_size).encode(FORMAT)
        file_size += b' ' * (HEADER - len(file_size))
        client.send(file_size)    
        
        data = file.read()
        client.sendall(data)
        client.send(b"END!")          
        
    
def main():
    PORT = 9999
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send(client)
    client.close()

if __name__ == "__main__":
    main()