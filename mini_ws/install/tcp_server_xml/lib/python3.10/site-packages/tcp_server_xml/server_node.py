import csv
import socket
import xml.etree.ElementTree as ET

def load_table(filename):
    table = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        headers = next(reader)  # Read the header row
        for row in reader:
            carrier = row[0]
            table[carrier] = {}
            for i, value in enumerate(row[1:]):
                station = headers[i+1]
                table[carrier][station] = int(value)
    return table

def get_value_from_table(table, station, carrier):
    if carrier in table and station in table[carrier]:
        return table[carrier][station]
    else:
        return None


def main():
    print('Hi from tcp_server_xml.')

    filename = 'procssing_times_table.csv'
    table = load_table(filename)

    host = socket.gethostname()
    host = "172.20.66.25"
    print(host)
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    i = 0
    print("Connection from: " + str(address))
    while True:
        i = i +1 
        data = conn.recv(1024).decode()
        print("msg_"+str(i)+"_:"+str(data).strip())
        if not data:
            continue
            conn.send(data.encode())  # send data to the client
        root = ET.fromstring(data)
        station_element = root.find("station")
        carrier_element = root.find("carrier")
        if carrier_element is not None and station_element is not None:
            station_number = f"Station#{int(station_element.text):02d}"
            carrier_number = f"Carrier#{int(carrier_element.text)}"
            #print(station_number)
            #print(carrier_number)
            data = get_value_from_table(table,station_number,carrier_number)
            data = str(data)
        else:
            data = "<id> element not found in XML."
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    main()
