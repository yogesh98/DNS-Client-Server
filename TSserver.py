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
        inputEntries.append(entry.strip("\n"))

    try:
        ts_socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("TS socket open error",err))

    ts_server_binding=('', 52328)
    ts_socket.bind(ts_server_binding)
    ts_socket.listen(1)
    hostname = mysoc.gethostname()
    ts_host_ip = (mysoc.gethostbyname(hostname))
    csockid,addr=ts_socket.accept()

    while True:
        client_data = csockid.recv(100)
        foundEntry = False
        if not client_data:
            break
        client_data = client_data.strip("\n")
        client_data = client_data.strip("\r")
        print("[TS:] Recieved: %s" % client_data)

        for entry in inputEntries:
            splitEntry = entry.split(" ")
            entryHostname = splitEntry[0].strip("\n")
            entryHostname = splitEntry[0].strip("\r")
            entryHostname = splitEntry[0].strip()

            if entryHostname == client_data:
                foundEntry = True
                print("[TS:] Sending: %s" % entry)
                csockid.send(entry)
                break
        if foundEntry == False:
            print("[TS:] Sending Error")
            error = client_data+" - Error:HOST NOT FOUND"
            csockid.send(error)


    ts_socket.close()
    exit()

TSserver()
