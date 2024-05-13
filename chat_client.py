from socket import *
import threading
import sys
import datetime
import json
import time

numRcvMsgs, numSntMsgs, numRcvChar, numSntChar = 0, 0, 0, 0 #variables to track message information for summary report
lock = threading.Lock() #race condition lock

def add_client(clientSocket): #function to add client
    global numRcvMsgs, numRcvChar, error
    error = False #reset error
    while 1: 
        try: 
            new_client = clientSocket.recv(1024).decode() #receive new client from server and decode for json
            info = json.loads(new_client) #import data from server

            if info["message"] == "Nickname already in use": #check if nickname is already in use, set error if true
                with lock: 
                    error = True
                break
            
            if info["type"] == "message": #if client sends message, increment counters and print message
                numRcvMsgs += 1
                numRcvChar += len(info["message"])
                print(f"{info['timestamp']} :: {info['nickname']}: {info['message']}")
                
        except Exception as e: #if error, break out of loop
            break

def main():
    #create variables for essential information from command line arguments
    global numRcvMsgs, numSntMsgs, numRcvChar, numSntChar, error
    hostname = args[1] 
    port = int(args[2])
    name = args[3]
    id = args[4]
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error = False

    while True:
        try:
            ip = gethostbyname(hostname) #resolves ip address
            clientSocket = socket(AF_INET, SOCK_STREAM) #creates socket
            clientSocket.connect((ip, port)) #connects socket to server with ip and port

            #sends join message to server
            info = json.dumps({"type": "join", "nickname": name, "clientID": id, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) 
            clientSocket.sendall(info.encode())

            threading.Thread(target=add_client, args=(clientSocket,)).start() #starts new thread to add client

            time.sleep(1) #give time to check if nickname is already in use

            with lock: #if nickname is already in use, get new nickname and reset error flag
                if error:
                    name = input("Nickname already in use. Please enter a different name: \n")
                    error = False
                    continue
                
            #if nickname is not in use, start sending messages
            print(f"ChatClient started with server IP: {ip}, port: {port}, nickname: {name}, clientID: {id}")
            print("Enter Message: \n")

            while True:
                client_input = input() #user's message
                if client_input == "disconnect": #if user disconnects, send disconnect message and print summary
                    clientSocket.sendall(json.dumps({"type": "disconnect", "nickname": name, "clientID": id}).encode())
                    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"Summary: start:{start_time}, end:{end_time}, msg sent:{numSntMsgs}, msg rcv:{numRcvMsgs}, char sent:{numSntChar}, char rcv:{numRcvChar}")
                    return
                else: #if message is not disconnect, send message to server and increment counters
                    numSntMsgs += 1
                    numSntChar += len(client_input)
                    clientSocket.sendall(json.dumps({"type": "message", "nickname": name, "message": client_input, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}).encode())
        
        except Exception as e: #catch any errors
            print(e)
            print("Unable to connect to server")
            exit()                           

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 5: #check if command line arguments are correct
        print (f"ERR - arg {len(args)}")
        exit()
    main()