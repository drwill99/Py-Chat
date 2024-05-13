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