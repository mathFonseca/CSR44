
import hashlib
import syslog
import pysyslogclient
import threading
from socket import *

PORT = 8080



class Server:

    CRLF = '\r\n'
    Socket = socket(AF_INET,SOCK_STREAM)

    def __init__(self, socket):
        try:
            self.Socket = socket
            self.syslogClient = pysyslogclient.SyslogClientRFC5424("192.168.18.10", 1468, proto="TCP")
            threading.Thread(target=self.run, args=()).start()
        except print(0):
            pass

    def run(self):
        try:
            self.request()
        except Exception as E:
            # syslog E
            print(E)

    def request(self):
        request = self.Socket.recv(1024)
        # print('Request: ',request)

        rType = request.decode().split(' ')[0]

        if(rType == 'GET'):
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
            # Website needs to be blocked.
            if( url.find("monitorando") != -1 or after_slash.find("monitorando") != -1):
                self.syslogClient.log("URL -Monitorando- found: " + url, severity=pysyslogclient.SEV_EMERGENCY)
                self.syslogClient.close()

                header = "HTTP/1.1 200 OK" + self.CRLF + self.CRLF

                data = "<HTML>" + "<HEAD><TITLE>Exemplo de resposta HTTP </TITLE></HEAD>" + "<BODY>Acesso não autorizado!</BODY> " + "</HTML>"

                self.Socket.send(str.encode(header + data))
                self.Socket.close()
            else:
                # Website can be accessed.
                self.getObject()
                 
        else:
            self.sysLogClient.log("HTTP/1.1 405 Method Not Allowed", severity=pysyslogclient.SEV_ERROR)
            self.sysLogClient.close()
            self.Socket.send(str.encode("HTTP/1.1 405 Method Not Allowed" + self.CRLF + self.CRLF))
            self.Socket.close()


        
    
    def getObject(self):
        print('eae')

        

def main():
    syslog.syslog(syslog.LOG_ERR,'System Init')
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',PORT))
    serverSocket.listen(1)
    print("Server is ready to listen")
    while True:
        conn, addr = serverSocket.accept()
        request = Server(conn)


if __name__ == "__main__":
    main()