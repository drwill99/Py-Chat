from socket import *
import threading
import datetime
import sys
import json
import signal

active_clients = {} #structure to store active clients

def add_client(connectionSocket, addr):   
    #variables to store nickname and clientID
    name = None
    id = None
    try:
        while 1:
            new_client = connectionSocket.recv(1024).decode() #receive data from client
            info = json.loads(new_client) #import data from client

            if info["type"] == "join": #if client is joining, get nickname and clientID
                name = info["nickname"]
                id = info["clientID"]
                if name in [data["nickname"] for data in active_clients.values()]: #check if nickname is already in use
                    connectionSocket.send(json.dumps({"type": "error", "message": "Nickname already in use"}).encode())
                    connectionSocket.close() #close connection if nickname is already in use
                    return
                else: #if nickname is available, add to active clients list and display connection message
                    active_clients[connectionSocket] = {"nickname": name, "clientID": id}
                    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{time} :: {name}: connected.")

            elif info["type"] == "message": #if client is sending a message, print message information on server
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Received: IP:{addr[0]}, Port:{addr[1]}, Client-Nickname:{name}, ClientID:{id}, Date/Time:{time}, Msg-Size:{len(info['message'])}")
                others = [client for client in active_clients.keys() if client is not connectionSocket] #determines list of clients that are not the sender
                dump = json.dumps(info)

                for client in others: #send message to all clients not the sender
                    try: 
                        client.sendall(dump.encode())
                    except:
                        client.close()
                        del active_clients[client] #close connection if client disconnects

                #get users that received a message to print broadcast message
                clients_broadcasted = [data["nickname"] for client, data in active_clients.items() if client is not connectionSocket]
                print(f"Broadcasted: {', '.join(clients_broadcasted)}")

            elif info["type"] == "disconnect": #if client disconnects, display disconnect message
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{time} :: {name}: disconnected.")
                break #break from loop to close connection

    except Exception as e: #catch any errors
        print(e)

    finally: #close connection
        connectionSocket.close()
        if connectionSocket in active_clients:
            del active_clients[connectionSocket]

def resolve_ip(): #get server IP
    try:
        tempSocket = socket(AF_INET, SOCK_DGRAM) #create temporary socket
        tempSocket.connect(("0.0.0.0", 80)) #connect to open port
        ip = tempSocket.getsockname()[0] #get IP
        tempSocket.close() #close socket
    except Exception: #if unable to resolve IP
        ip = "127.0.0.1" #set IP to localhost
    return ip

def main(port):   
    try:
        #create server socket
        welcomeSocket = socket(AF_INET, SOCK_STREAM) 
        welcomeSocket.bind(('', port))
        welcomeSocket.listen()

        ip = resolve_ip() #resolve server IP
        print (f"ChatServer started with server IP: {ip}, port: {port} ...") #print starting message
        while 1: #keep server running
            connectionSocket, addr = welcomeSocket.accept() #accept connection from client
            threading.Thread(target=add_client, args=(connectionSocket, addr)).start() #start new thread to handle client
            
    except OSError: #catch any errors while creating socket
        print(f"ERR - cannot create ChatServer socket using port number {port}")
        exit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL) #handle ctrl+c from terminal
    args = sys.argv
    if len(args) != 2: #check if correct number of arguments
        print (f"ERR - arg {len(args)}")
        exit()
    port = int(args[1])
    if 10000 > port or port > 11000: #check if port is in valid range
        print (f"ERR - arg {port}")
        exit()
    main(port)