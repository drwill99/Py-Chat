## About

This program uses TCP (Transmission Control Protocol) for communication. 

Both the `chat_client.py` and `chat_server.py` programs support at least three different kinds of requests that the server or peer can respond to:

1. Joining the Chat:

    * When a client joins the chat by running chat_client.py, it sends a join request to the server with the client's nickname, client ID, and timestamp. The server responds by adding the client to the list of active clients and acknowledging the connection.

2. Sending Messages:

    * Clients can send messages to the server, which are then broadcasted to all other clients. The server receives message requests from clients and forwards the messages to all other connected clients, excluding the sender. It tracks the message size, sender's details, and timestamp.

3. Disconnecting from the Chat:

    * Clients can disconnect from the chat by sending a disconnect request to the server. The server acknowledges the disconnection, removes the client from the active clients list, and notifies other clients about the disconnection.

## How to Run:

1. Open new terminal windows for the server and each of the clients who want to join.

2. On the server window, run `python chatServer.py <port between 10000-11000>`.
    * Replace `<port between 10000-11000>` with an integer between 10000 and 11000.

3. On the client windows, run `python chatClient.py <hostname or server IP> <port> <nickname> <clientID>`.
    * Replace `<hostname or server IP>` with a hostname or IP address of the server ("localhost").
    * Replace `<port>` with the same port used for the server.
    * Replace `<nickname>` with a unique name.
    * Replace `<clientID>` with an integer ID.

## How to End:

1. Type "q!" on client terminal windows

2. Enter "ctrl+c" on the server terminal window