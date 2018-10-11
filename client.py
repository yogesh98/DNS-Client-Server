import sys
import socket as mysoc

if len(sys.argv) != 3:
    #Check if correct system arguments
    print("invalid arguments, must provide hostnames.txt, RS hostname")
    sys.exit()

def initSockets():

    #init rs socket
    try:
        rs_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C:] RS socket created")
    except mysoc.error as err:
        print('{}\n'.format("RS socket open error", err))

    #init ts socket
    try:
        ts_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C:] TS socket created")
    except mysoc.error as err:
        print('{}\n'.format("TS socket open error", err))

    #setup RS
    rs_addr = sys.argv[2]
    rs_port = 50007
    rs_server_binding = (rs_addr,rs_port)
    rs_socket.connect(rs_server_binding)

    fOut = open("RESOLVED.txt", "w+")
    fHostnames = open(sys.argv[1], "r")
    fHostnamesList = fHostnames.readlines()

    tsConnected = False

    for line in fHostnamesList:
        #Send each line to RS server
        print("[C:] sending:",line)
        rs_socket.send(line.encode('utf-8'))
        #received data from RS
        rs_data_received = rs_socket.recv(100)
        rs_resolved_entry = ts_data_received.decode('utf-8')
        print("[C:] recieved", rs_resolved_entry)
        #split string to determine A or NS
        splicedEntry = rs_resolved_entry[len(resolved_entry-2):]
        splicedEntry.strip()
        #if A write to RESVOLVED.txt
        if splicedEntry == 'A':
            print("[C:] Writing to RESOLVED:",rs_resolved_entry)
            fOut.write("%s\n" % rs_resolved_entry)
        #otherwise NS, go to TS server from resolved entry string
        elif splicedEntry == 'NS':
            #split on space, take s[0] as TS hostname
            splitResolved = resolved_entry.split(" ")
            if tsConnected == False
                #setup TS
                ts_addr = splitResolved[0].trim()
                ts_port = 50008
                ts_server_binding = (ts_addr,ts_port)
                ts_socket.connect(ts_server_binding)
                tsConnected = True

            ts_socket.send(line.encode('utf-8'))
            ts_data_received = ts_socket.recv(100)
            ts_resolved_entry = ts_data_received.decode('utf-8')
            #If error is not found, write to RESOLVED.txt
            if ts_resolved_entry.find("Error:") == -1:
                fOut.write("%s\n" % ts_resolved_entry)
            else:
                print(ts_resolved_entry)
    rs_socket.close()
    exit()

initSockets()
