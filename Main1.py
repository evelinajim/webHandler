import socket
import WebHandler



def main():
    # https: // docs.python.org / 3 / howto / sockets.html
    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    serversocket.bind(('localhost', 81))
    # become a server socket
    serversocket.listen(5)

    threads = []
    while True:
        # accept connections from outside
        (clientsocket, address) = serversocket.accept()

        myHandler = WebHandler.Web_Handler(clientsocket)
        threads.append(myHandler)
        myHandler.start()

    pass





if __name__  == '__main__':
    main()

