import threading
import mimetypes




class Web_Handler(threading.Thread):
    def __init__(self,Connected_Socket,group=None, target=None, name=None, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.connected_socket=Connected_Socket
        self.HTTPStatus = 'HTTP/1.1 200 OK\r\n'.encode('utf8')
        self.HTTPContent = 'Content-Type: text/html; charset=ISO-8859-4\r\n'.encode('utf8')
        self.HTTPBlankLine ='\r\n'.encode('utf8')
        pass

    def run(self):
        self.process_request()

    def send_header(self):
        # https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html
        self.connected_socket.send(self.HTTPStatus)
        self.connected_socket.send(self.HTTPContent)
        self.connected_socket.send(self.HTTPBlankLine)  # blank line required before message body

    def process_request(self):
        #persistent connection is here. make sure lines are aligned correctly
        while(1 == 1):
            try:
                raw_request = self.connected_socket.recv(2048)    #rocket recieve. Header take out close.
            except:
                #self.HTTPContent = 'Content-Type: text/html; charset=ISO-8859-4\r\n'
                break
                # https://tools.ietf.org/html/rfc2616
            request_str = raw_request.decode('utf8')
            request_lines = request_str.split('\r\n')
            request_line = request_lines[0]
            # Request-Line   = Method SP Request-URI SP HTTP-Version CRLF
            (Method, Request_URI, HTTP_Version) = request_line.split(' ')

            body = self.makeBody(Request_URI)
            self.send_header()
            self.connected_socket.send(body)
            #self.connected_socket.close()   CLOSES CONNECTION. TAKE THIS OUT!
        pass

    def makeBody(self,Request_URI):

        print(Request_URI)
        if Request_URI == '/' :
            filename = 'index.html'
        else:
            filename = '.' + Request_URI
        #if Request_URI == '/profile/<name>':
            #filename = 'profile.html'
        #else:
            #filename = '.' + Request_URI

        (type,encoding) = mimetypes.guess_type(Request_URI)
        print(type,encoding)
        try:
            self.HTTPContent = 'Content-Type: '+type+'; '
        except TypeError:
            self.HTTPContent = 'Content-Type: text/html; charset=ISO-8859-4\r\n'
        else:
            try:
                self.HTTPContent = self.HTTPContent + encoding + '\r\n'
            except TypeError:
                self.HTTPContent = self.HTTPContent + 'None \r\n'
        print(self.HTTPContent)

        self.HTTPContent = self.HTTPContent.encode('utf-8')
        print(self.HTTPContent)
        try:
            with open(filename,'rb') as f:
                body = f.read()
        except IOError:
            self.HTTPStatus = 'HTTP/1.1 404 File Not Found\r\n'.encode('utf8')
            body = 'BadFile'
        else:
            self.HTTPStatus = 'HTTP/1.1 200 OK\r\n'.encode('utf8')

        print(self.HTTPStatus)
        try:
            return(body.encode())
        except AttributeError:
            return(body)