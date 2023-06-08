import socket
import xml.etree.ElementTree as ET

def main():
    print('Hi from tcp_server_xml.')
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        root = ET.fromstring(data)
        cat_element = root.find("id")
        if cat_element is not None:
            cat_number = cat_element.text
            if(int(cat_number) > 8):
                data = "<id>0</id>" 
            else:
                data = "<id>1</id>" 
        else:
            data = "<id> element not found in XML."
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    main()
