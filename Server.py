
# HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import re
# TO DO: set constants
IP = '127.0.0.1'
PORT = 8080
SOCKET_TIMEOUT = 1000
DEFAULT_URL = r'E:\Rambam\Exercises (Networks)\webroot'
REDIRECTION_DICTIONARY = {}
FORBIDDEN = ()

def get_file_data(filename):
    """ Get data from file """
    f = open(DEFAULT_URL + '\\' + filename.replace('/','\\'), 'rb')
    return f.read()

def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if resource == '':
        url = DEFAULT_URL + '\\index.html'
    else:
        url = resource

    # TO DO: check if URL had been redirected, not available or other error code. For example:
    http_header = ""
    data = b''
    if url in REDIRECTION_DICTIONARY:
        # TO DO: send 302 redirection response
        http_header = "HTTP/1.1 303 See Other\r\n"
        http_header += "Location: " + REDIRECTION_DICTIONARY[url] + '\r\n'
    elif url in FORBIDDEN:
        http_header = "HTTP/1.1 403 Forbidden\r\n"
    else:
        http_header = "HTTP/1.1 200 OK\r\n"
    # TO DO: extract requested file type from URL (html, jpg etc)
        filetype = url[url.rfind('.') + 1:]
        if filetype == 'html':
            http_header += "Content-Type: text/html; charset=utf-8\r\n"# TO DO: generate proper HTTP header
        elif filetype == 'jpg':
            http_header += "Content-Type: image/jpeg\r\n"# TO DO: generate proper jpg header
        # TO DO: handle all other headers
        elif filetype == 'js':
            http_header += "Content-Type: text/javascript; charset=UTF-8\r\n"
        elif filetype == 'css':
            http_header += "Content-Type: text/css\r\n"
        filename = url[url.rfind('\\') + 1:]
        data = get_file_data(filename)
        http_header += "Content-Length: {}\r\n".format(len(data))
    http_header += '\r\n'
    # TO DO: read the data from the file
    http_response = http_header.encode() + data
    client_socket.send(http_response)


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    # TO DO: write function
    request = str(request)
    if re.match('^GET .* HTTP/1.1$', request) is not None:
        return True, request[request.find('/')+1:request.rfind('H')-1]
    return False, request[request.find('/')+1:request.rfind('H')-1]


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        # TO DO: insert code that receives client request
        # ...
        just_sent_in, client_request = "", ""
        while '\r\n\r\n' not in client_request:
            just_sent_in = client_socket.recv(64).decode()
            client_request += just_sent_in
        only_get_request = client_request[:client_request.find('\r\n')]
        valid_http, resource = validate_http_request(only_get_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print ('Error: Not a valid HTTP request')
            break
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print("Listening for connections on port %d" % PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
