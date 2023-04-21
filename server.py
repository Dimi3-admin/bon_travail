import socket
import threading


PORT = 10007



class Server_receiver(threading.Thread):

    def __init__(self,client_socket,addr,users_dict,*args, **kwargs):

        super().__init__(*args, **kwargs)
        self.client_socket =client_socket
        self.addr = addr
        self.users_dict = users_dict
        
        

    def send_all(self,message):
        for name,(thread,sock) in self.users_dict.items():
            if name != self.client_name:
                print(f"Sending {self.client_name}'s message to {name}")
                data = f"{self.client_name} : {message}".encode()
                sock.send(data)

    def run(self):
        print("Spawned new thread")
        self.client_name = self.client_socket.recv(1024).decode()
        print(f"Speaking to {self.client_name}")
        self.users_dict[self.client_name] = (self,self.client_socket)
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = self.client_socket.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            print(f"from {self.client_name} user: {data}")
            self.send_all(data)
        self.client_socket.close()  # close the connection
        print(f"Received BYE, closing connection to {self.addr}")

def launch_server(port = PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # look closely. The bind() function takes tuple as argument
    server_socket.bind(('localhost', port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(10)
    users_dict = {}
    while True:
        client_socket, address = server_socket.accept()  # accept new connection
        print("New connection from: " + str(address))
        thread = Server_receiver(client_socket,address,users_dict)
        thread.start()


if __name__ == '__main__':
    launch_server()