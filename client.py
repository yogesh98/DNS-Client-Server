import sys
import socket as mysoc

def initSockets():

    #init rs socket
    try:
        rs_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("RS socket open error", err))

    #init ts socket
    try:
        ts_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("TS socket open error", err))

    rs_addr = mysoc.gethostbyname(mysoc.gethostname())
    rs_port = 51237
    rs_server_binding = (rs_addr,rs_port)
    rs_socket.connect(rs_server_binding)

    #Open necessary files
    fOut = open("RESOLVED.txt", "w+")
    fHostnames = open("PROJ1-HNS.txt", "r")
    fHostnamesList = fHostnames.readlines()

    tsConnected = False

    for line in fHostnamesList:
        #Send each line to RS server
        stripLine = line.rstrip()
        print("[C:] sending to RS:", stripLine)
        rs_socket.send(line)
        #received data from RS
        rs_data = rs_socket.recv(100).strip()
        print("[C:] Recieved from RS:", rs_data)
        #split string to determine A or NS
        splicedEntry = rs_data[len(rs_data)-2:].strip()
        #if A write to RESVOLVED.txt
        if splicedEntry == 'A':
            fOut.write("%s\n" % rs_data)
        #otherwise NS, go to TS server from resolved entry string
        elif splicedEntry == 'NS':
            #split on space, take s[0] as TS hostname
            splitResolved = rs_data.split(" ")
            if tsConnected == False:
                #setup TS
                ts_addr = splitResolved[0].strip()
                ts_port = 52328
                ts_server_binding = (ts_addr,ts_port)
                ts_socket.connect(ts_server_binding)
                tsConnected = True
            print("Sending to TS:",line)
            ts_socket.send(line)
            ts_data_received = ts_socket.recv(100)
            #write to RESOLVED.txt
            print("Writing:", ts_data_received)
            fOut.write("%s\n" % ts_data_received)

    rs_socket.close()
    exit()

initSockets()
