from socket import *
import threading
import hashlib
import pysyslogclient
import csv
import pandas as pd

class Server:
    CRLF = '\r\n'
    Socket = socket(AF_INET,SOCK_STREAM)

    def __init__ (self, socket):
        self.Socket = socket
        self.sysLogClient = pysyslogclient.SyslogClientRFC5424("192.168.100.242", 514, proto="TCP")
        threading.Thread(target=self.run, args=()).start()

    def run(self):
        try:
            self.processRequest()
        except Exception as e:
            print(e)

    def logIntegrity(self, ip, hash):
        with open('integrity_verification.csv', 'a+', newline='') as database:
            databasewriter = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            databasewriter.writerow([ip, hash])
            return

    def verifyIP(self, ip):
        col_list = ["ip", "hash"]
        df = pd.read_csv("integrity_verification.csv", usecols=col_list)
        for row in df["ip"]:
            if(ip == row):
                return(True)
        return(False)

    def verifyIntegrity(self, ip, hash):
        data = pd.read_csv("integrity_verification.csv", index_col="ip")
        if(data.loc[ip][0] != hash):
            return(False)
        else:
            return(True)

    def updateIntegrity(self, ip, hash):
        data = pd.read_csv("integrity_verification.csv")
        data.loc[data["ip"]==ip, "hash"] = hash
        data.to_csv("integrity_verification.csv", index=False)

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
                if (self.verifyIP(server_socket_details[4][4][0]) == False):
                    self.logIntegrity(server_socket_details[4][4][0], hash)
                    self.sysLogClient.log("Integrity OK - " + server_socket_details[4][4][0] + " - " + hash, severity=pysyslogclient.SEV_INFO)
                else:
                    if (self.verifyIntegrity(server_socket_details[4][4][0], hash)):
                        self.sysLogClient.log("Integrity OK - " + server_socket_details[4][4][0] + " - " + hash, severity=pysyslogclient.SEV_INFO)
                    else:
                        self.updateIntegrity(server_socket_details[4][4][0], hash)
                        self.sysLogClient.log("Integrity CHANGED! - " + server_socket_details[4][4][0] + " - " + hash, severity=pysyslogclient.SEV_WARNING)
                self.sysLogClient.close()
                self.Socket.send(web_server_response_append)
            proxy_socket.close()

        except error as e:
            self.sysLogClient.log(proxy_socket.getsockname()[0] + " - " + server_socket_details[4][4][0] + " - " + "HTTP/1.1 404 not found", severity=pysyslogclient.SEV_ERROR)
            self.sysLogClient.close()
            self.Socket.send(str.encode('HTTP/1.1 404 not found' + self.CRLF + self.CRLF))
        self.Socket.close()

def main():
    serverPort = 8080
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print("The server is ready to listen")
    while(True):
        connectionSocket, addr = serverSocket.accept()
        request = Server(connectionSocket)

if __name__ == "__main__":
    main()