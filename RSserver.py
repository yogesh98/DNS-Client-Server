import sys
import socket as mysoc

if len(sys.argv) != 2:
    #Check if correct system arguments
    print("invalid arguments, must provide DNS entries file")
    sys.exit()

def RSserver():

    fDNSRSnames = open(sys.argv[1], "r")
    fDNSRSList = fDNSRSnames.readlines()
    inputEntries = []
    for entry in fDNSRSList:
        print("[RS:] Storing: %s" % entry)
        inputEntries.append(entry.strip("\n"))

    try:
        rs_socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[RS:] RS socket created")
    except mysoc.error as err:
        print('{}\n'.format("RS socket open error",err))

    rs_server_binding=('', 50007)
    rs_socket.bind(rs_server_binding)
    rs_socket.listen(1)
    hostname = mysoc.gethostname()
    rs_host_ip = (mysoc.gethostbyname(hostname))
    csockid,addr=rs_socket.accept()

    while True:
        client_data = csockid.recv(100)
        if not client_data:
            break
        client_data = client_data.strip("\n")
        client_data = client_data.strip("\r")
        print("[RS:] recieved: %s" % client_data)
        print repr(client_data)

        for entry in inputEntries:
            splitEntry = entry.split(" ")
            entryHostname = splitEntry[0].strip("\n")
            entryHostname = splitEntry[0].strip("\r")
            entryHostname = splitEntry[0].strip()

            print("[RS:] hostname: ")
            print repr(entryHostname)
            entryCode = splitEntry[-1]
            entryCode.strip()
            if entryCode == 'NS':
                csockid.send(entry)
            if entryHostname == client_data:
                print("[RS:] Sending: %s" % entry)
                csockid.send(entry)

    rs_socket.close()
    exit()

RSserver()
