import sys
import socket as mysoc

if len(sys.argv) != 6:
    #Check if correct system arguments
    print("invalid arguments, must provide hostnames.txt, RS hostname, RS port, TS hostname, TS port")
    sys.exit()

def initSockets():
    try:
        client_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C:] client socket created")
    except mysoc.error as err:
        print('{}\n'.format("socket open error", err))
    #setup RS
    rs_addr = sys.argv[2]
    rs_port = int(sys.argv[3])
    rs_server_binding = (rs_addr,rs_port)
    client_socket.connect(rs_server_binding)
    #setup TS
    ts_addr = sys.argv[4]
    ts_port = int(sys.argv[5])
    ts_server_binding = (ts_addr,ts_port)

    fOut = open("RESOLVED.txt", "w+")
    fHostnames = open(sys.argv[1], "r")
    fHostnamesList = fHostnames.readlines()
    connectToRS()

def connectToRS():
    print("connectToRS")
    for line in fHostnamesList:
        #Send each line to RS server
        print("[C:] sending:",line)
        client_socket.send(line.encode())
        #Check recieved data has A or NS
        ts_data_received = client_socket.recv(100)
        resolved_entry = ts_data_received.decode('utf-8')
        print("[C:] recieved", resolved_entry)
        splicedEntry = resolved_entry[len(resolved_entry-2):]
        splicedEntry.strip()
        #if A write to RESVOLVED.txt
        #if NS go to TS server


def connectToTS():
    print("connectToTS")
    #Pull TS address and port from system arguments

initSockets()
