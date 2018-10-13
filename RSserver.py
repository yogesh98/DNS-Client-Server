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
        inputEntries.append(entry.strip("\n"))

    try:
        rs_socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("RS socket open error",err))

    rs_server_binding=('', 51237)
    rs_socket.bind(rs_server_binding)
    rs_socket.listen(1)
    hostname = mysoc.gethostname()
    rs_host_ip = (mysoc.gethostbyname(hostname))
    csockid,addr=rs_socket.accept()

    while True:
        client_data = csockid.recv(100)
        foundEntry = False
        if not client_data:
            break
        client_data = client_data.strip("\n")
        client_data = client_data.strip("\r")
        print("[RS:] Recieved: %s" % client_data)

        for entry in inputEntries:
            splitEntry = entry.split(" ")
            entryHostname = splitEntry[0].strip("\n")
            entryHostname = splitEntry[0].strip("\r")
            entryHostname = splitEntry[0].strip()
            flag = splitEntry[-1]
            flag = flag.strip()

            print("Hostname: %s Flag: %s" %(entryHostname, flag))

            if entryHostname == client_data:
                foundEntry = True
                print("[RS:] Sending: %s" % entry)
                csockid.send(entry)
                break
            if flag == 'NS':
                print("PRINT")
                if foundEntry == False:
                    print("[RS:] Sending NS")
                    csockid.send(entry)

    rs_socket.close()
    exit()

RSserver()
