
import pysyslogclient
import threading
import hashlib
from socket import *

PORT = 8080
SYSLOGIP = "192.168.100.242"
SYSLOGPORT = 514
class Server:

    CRLF = '\r\n'
    Socket = socket(AF_INET,SOCK_STREAM)

    def __init__(self, socket):
        try:
            self.Socket = socket
            self.sysLogClient = pysyslogclient.SyslogClientRFC5424("192.168.100.242", 514, proto="TCP")
            threading.Thread(target=self.run, args=()).start()
        
        except error as e:
            self.sysLogClient.log("Unable to create/re-use the socket. Error: " + e, severity=pysyslogclient.SEV_EMERGENCY)
            self.sysLogClient.close()

        print("Server is ready to listen")

    def run(self):
        try:
            self.processRequest()
        except Exception as e:
            print(e)

    def processRequest(self):
        request = self.Socket.recv(1024)
        print(request.decode())
        req_type = request.decode().split(' ')[0]
        if req_type == "GET":
            http = request.decode().split(' ')[1]
            double_slash_pos = str(http).find("//")
            url = ""
            
            if double_slash_pos == -1:
                url_part = http[1:]
                url = url_part.split('/')[0]
            else:
                if http.split('//')[1][-1] == "/":
                    url_part = http.split('//')[1][:-1]
                    url = url_part.split('/')[0]
                else:
                    url_part = http.split('//')[1]
                    url = url_part.split('/')[0]

            slash_check = url_part.split('/')[1:]
            after_slash = ""
            if slash_check:
                for path in slash_check:
                    after_slash += "/"
                    after_slash += path
            if (url.find("monitorando") != -1 or after_slash.find("monitorando") != -1):
                statusLine = "HTTP/1.1 200 OK" + self.CRLF + self.CRLF
                self.sysLogClient.log("Endereco monitorado! - " + url + after_slash + " - " + statusLine, severity=pysyslogclient.SEV_EMERGENCY)
                self.sysLogClient.close()
                entityBody = "<HTML>" + "<HEAD><TITLE>Acesso nao autorizado!</TITLE></HEAD>" + "<BODY>Acesso nao autorizado!</BODY></HTML>"
                self.Socket.send(str.encode(statusLine + entityBody))
                self.Socket.close()    
            else:
                self.getFile(url, after_slash)
        else:
            self.sysLogClient.log("HTTP/1.1 405 Method Not Allowed", severity=pysyslogclient.SEV_ERROR)
            self.sysLogClient.close()
            self.Socket.send(str.encode("HTTP/1.1 405 Method Not Allowed" + self.CRLF + self.CRLF))
            self.Socket.close()

    def getFile(self, url, after_slash):
        proxy_socket = socket(AF_INET, SOCK_STREAM)
        try:
            proxy_socket.settimeout(2)
            proxy_socket.connect((url, 80))
            web_request = str()
            if after_slash:
                web_request = "GET /" + after_slash[1:] + " HTTP/1.1\nHost: " + url + "\n\n"
            else:
                web_request = "GET / HTTP/1.1\nHost: " + url + "\n\n"
            
            proxy_socket.send(str.encode(web_request))
            server_socket_details = getaddrinfo(url, 80)
            server_details_message = "<body> Web Server Details:- <br />"
            server_details_message += "Server host name: " + url + " <br /> Server port number: 80" + "<br />"
            server_details_message += "Socket family: " + str(server_socket_details[0][0]) + "<br />"
            server_details_message += "Socket type: " + str(server_socket_details[0][1]) + "<br />"
            server_details_message += "Socket protocol: " + str(server_socket_details[0][2]) + "<br />"
            server_details_message += "Timeout: " + str(self.Socket.gettimeout()) + "<br /> </body>"
            web_server_response_append = str.encode("")
            timeout_flag = False
            while True:
                try:
                    web_server_response = proxy_socket.recv(4096)
                except timeout:
                    if len(web_server_response_append) <= 0:
                        timeout_flag = True
                    break
                if len(web_server_response) > 0:
                    web_server_response_append += web_server_response
                else:
                    break
            file = web_server_response_append
            web_server_response_append += str.encode(server_details_message)
            if timeout_flag:
                error_response = "HTTP/1.1 408 Request timeout" + self.CRLF + self.CRLF
                error_response += server_details_message
                self.sysLogClient.log(proxy_socket.getsockname()[0] + " - " + server_socket_details[4][4][0] + " - " + "HTTP/1.1 408 Request timeout", severity=pysyslogclient.SEV_ERROR)
                self.sysLogClient.close()
                self.Socket.send(str.encode(error_response))
            else:
                self.sysLogClient.log(proxy_socket.getsockname()[0] + " - " + server_socket_details[4][4][0] + " - " + "HTTP/1.1 200 OK", severity=pysyslogclient.SEV_INFO)
                hash = hashlib.sha256(file).hexdigest()
                self.sysLogClient.close()
                self.Socket.send(web_server_response_append)
            proxy_socket.close()

        except error as e:
            self.sysLogClient.log(proxy_socket.getsockname()[0] + " - " + server_socket_details[4][4][0] + " - " + "HTTP/1.1 404 not found", severity=pysyslogclient.SEV_ERROR)
            self.sysLogClient.close()
            self.Socket.send(str.encode('HTTP/1.1 404 not found' + self.CRLF + self.CRLF))
        self.Socket.close()


def generateHASH():
    fh = open("proxy.py").read()
    hash_ = hashlib.md5(fh.encode("utf-8")).hexdigest()[:16]
    f = open("hash.txt",'w+')
    f.write(hash_)
    f.close()

def checkIntegrity():
    fh = open("hash.txt").read()
    th = open("proxy.py").read()
    hash_ = hashlib.md5(th.encode("utf-8")).hexdigest()[:16]
    if(fh == hash_):
        return True
    return False

def main():
    generateHASH()
    if(checkIntegrity()):
        serverPort = 8080
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(1)
        print("The server is ready to listen")
        while(True):
            connectionSocket, addr = serverSocket.accept()
            request = Server(connectionSocket)
    else:
        print("APPLICATION INTEGRITY COMPROMISED!")

if __name__ == "__main__":
    main()


