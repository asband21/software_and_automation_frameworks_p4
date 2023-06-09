import re
import csv
import socket
import xml.etree.ElementTree as ET
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

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

def extract_number_from_string(string):
    match = re.search(r'\d+', string)
    if match:
        return match.group()
    else:
        return "0"
def filter_ascii(input_string):
    filtered_string = ""
    for char in input_string:
        if 31 < ord(char) < 128:
            filtered_string += char
    return filtered_string

def main(args=None):
    rclpy.init(args=args)
    node_pud = rclpy.create_node("node_pud")
    pud = node_pud.create_publisher(String, "log_forbrik",10)
    print('Hi from tcp_server_xml.')

    filename = 'procssing_times_table.csv'
    table = load_table(filename)

    host = socket.gethostname()
    host = "172.20.66.25"
    print(host)
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    sokkit_zie = 1024*2
    server_socket.listen(sokkit_zie)
    conn, address = server_socket.accept()  # accept new connection
    i = 0
    print("Connection from:" + str(address))
    while True:
        i = i +1 
        #data = conn.recv(sokkit_zie).decode('ascii')
        data = conn.recv(sokkit_zie).decode()
        data = filter_ascii(data)
        print("\nmsg_"+str(i)+"_["+str(data)+"]")
        if not data:
            break
            #conn.send("<prut>ff</prut>".encode())  # send data to the client
            #conn.send(data.encode())  # send data to the client
            #continue
        try:
            root = ET.fromstring(data)
        except:
            print("kunne ikke læse som xml")
            continue
        station_element = root.find("sta")
        carrier_element = root.find("pro")
        tid_element = root.find("date")

        #station_element = root.find("station")
        #carrier_element = root.find("carrier")
        if carrier_element is not None and station_element is not None:

            station_number = f"Station#{int(extract_number_from_string(station_element.text)):02d}"
            carrier_number = f"Carrier#{int(carrier_element.text)}"
            #print(station_number)
            #print(carrier_number)
            data = get_value_from_table(table,station_number,carrier_number)
            data = str(data)
            msg = String()
            msg.data = f"{station_number} {carrier_number} time:{tid_element.text} prossingsen_time:{data}" 
            pud.publish(msg)
            print(f"{station_number} {carrier_number} time:{tid_element.text} prossingsen_time:{data}")
        else:
            data = "<error>element not found in XML.</error>"
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    main()
