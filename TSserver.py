import sys
import socket as mysoc

if len(sys.argv) != 2:
    #Check if correct system arguments
    print("invalid arguments, must provide DNS entries file")
    sys.exit()

def TSserver():

    fDNSTSnames = open(sys.argv[1], "r")
    fDNSTSList = fDNSTSnames.readlines()
    inputEntries = []
    for entry in fDNSTSList:
        print("[TS:] Storing: ",entry)
        inputEntries.append(entry)

    try:
        ts_socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[TS:] TS socket created")
    except mysoc.error as err:
        print('{}\n'.format("TS socket open error",err))

    ts_server_binding=('', 50007)
    ts_socket.bind(ts_server_binding)
    ts_socket.listen(1)
    hostname = mysoc.gethostname()
    print("[TS:] Server hostname:",hostname)
    ts_host_ip = (mysoc.gethostbyname(hostname))
    print("[TS:] IP is",ts_host_ip)
    csockid,addr=ts_socket.accept()
    print("[TS:] connection request from ",addr)

    found = False
    while True:
        client_data = csockid.recv(100).decode('utf-8')
        #if not data:
            #break
        for entry in inputEntries:
            splitEntry = entry.split(" ")
            entryHostname = splitEntry[0]
            if entryHostname == client_data:
                csockid.send(entry.encode('utf-8'))
                found = True
        if not found:
            csockid.send("%s - Error:HOST NOT FOUND" %client_data)
    rs_socket.close()
    exit()

TSserver()
