import sys
import socket as mysoc

if len(sys.argv) != 2:
    #Check if correct system arguments
    print("invalid arguments, must provide DNS entries file")
    sys.exit()

def TSserver():
    try:
        rs_socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S:] TS socket created")
    except mysoc.error as err:
        print('{}\n'.format("TS socket open error",err))

    ts_server_binding=('', 50008)
    ts_socket.bind(ts_server_binding)
    ts_socket.listen(1)
    hostname = mysoc.gethostname()
    print("[TS:] Server hostname:",hostname)
    ts_host_ip = (mysoc.gethostbyname(hostname))
    print("[TS:] IP is",ts_host_ip)
    csockid,addr=ts_socket.accept()
    print("[TS:] connection request from ",addr)

    fDNSTSnames = open(sys.argv[1], "r")
    fDNSTSList = fDNSTSnames.readlines()
    inputEntries = []
    for entry in fDNSTSList:
        print("Storing: ",entry)
        inputEntries.append(entry)
    entryFound = False
    while True:
        client_data_received = csockid.recv(100).decode()
        if not data:
            break
        for entry in inputEntries:
            splitEntry = entry.split(" ")
            entryHostname = splitEntry[0].trim()
            if entryHostname == client_data_received:
                csockid.send(entryHostname.encode('utf-8'))
                entryFound = True
        if !entryFound:
            csockid.send("%s + - Error:HOST NOT FOUND" % client_data_received)


    rs_socket.close()
    exit()
