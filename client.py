import sys
import socket as mysoc

if len(sys.argv) != 2:
    #Check if correct system arguments
    print("invalid arguments, must provide file with hostnames")
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

    rs_addr = mysoc.gethostbyname(mysoc.gethostname())
    rs_port = 50007
    rs_server_binding = (rs_addr,rs_port)
    rs_socket.connect(rs_server_binding)

    fOut = open("RESOLVED.txt", "w+")
    fHostnames = open(sys.argv[1], "r")
    fHostnamesList = fHostnames.readlines()

    tsConnected = False

    for line in fHostnamesList:
        #Send each line to RS server
        stripLine = line.rstrip()
        print("[C:] sending:", stripLine)
        rs_socket.send(line)
        #received data from RS
        rs_data = rs_socket.recv(100).strip()
        print("[C:] recieved", rs_data)
        #split string to determine A or NS
        splicedEntry = rs_data[:-2]
        print("%s\n" %splicedEntry)
        #if A write to RESVOLVED.txt
        if splicedEntry == 'A':
            print("[C:] Writing to RESOLVED:",rs_data)
            fOut.write("%s\n" % rs_data)
        #otherwise NS, go to TS server from resolved entry string
        elif splicedEntry == 'NS':
            #split on space, take s[0] as TS hostname
            splitResolved = resolved_entry.split(" ")
            if tsConnected == False:
                #setup TS
                ts_addr = splitResolved[0].strip()
                ts_port = 50008
                ts_server_binding = (ts_addr,ts_port)
                ts_socket.connect(ts_server_binding)
                tsConnected = True

            ts_socket.send(line)
            ts_data_received = ts_socket.recv(100)
            #If error is not found, write to RESOLVED.txt
            if ts_resolved_entry.find("Error:") == -1:
                fOut.write("%s\n" % ts_resolved_entry)
            else:
                print(ts_resolved_entry)
    rs_socket.close()
    exit()

initSockets()
