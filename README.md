## How to Run:

open new terminal windows for the server and each of the clients who want to join

on the server window, run `python chatServer.py <port between 10000-11000>` 
* replace `<port between 10000-11000>` with an integer between 10000 and 11000

on the client windows, run `python chatClient.py <hostname or server IP> <port> <nickname> <clientID>`
* replace `<hostname or server IP>` with a hostname or IP address of the server ("localhost")
* replace `<port>` with the same port used for the server
* replace `<nickname>` with a unique name
* replace `<clientID>` with an integer ID

## How to End:

type "q!" on client terminal windows

enter "ctrl+c" on the server terminal window