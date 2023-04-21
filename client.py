import socket
import threading

PORT = 10007


def listen_server(client_socket,name):
    print(f"Spawned listening thread")
    while True:
        data = client_socket.recv(1024).decode()
        print(f"\nReceived from server : {data}\n{name} -> : ")
        if not data:
            # This is added to avoid core dumps when server disconnects
            raise RuntimeError("Server was forcefully disconnected")

def sender(client_socket,name):
    print(f"Spawned sender thread")
    message = input(f"{name} -> : ")  # take input
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        message = input(f"{name} -> : ")  # take new input

    client_socket.close()

def connect_server(name,server_address= ('localhost', PORT)):
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    client_socket = socket.socket()  # instantiate
    client_socket.connect(server_address)  # connect to the server
    print("Connected to the server")

    client_socket.send(name.encode())

   
    listening_thread = threading.Thread(target=listen_server, args = (client_socket,name))
    sender_thread = threading.Thread(target=sender, args = (client_socket,name))

    listening_thread.start()

    print("Trying to start sender thread")
    sender_thread.start()



    sender_thread.join()
    print("Sender thread finished, wrapping up")
    
    # TODO: For now, the listening thread is simply ignored 
    # (its values are already properly destroyed )
    
    # listening_thread.join()       
    # print("Listening thread finished")
    




if __name__ == '__main__':
    name = input(f"Who are you? ")
    print(f"Hello {name}!")
    connect_server(name)