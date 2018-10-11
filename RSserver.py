import sys
import socket as mysoc

if len(sys.argv) != 2:
    #Check if correct system arguments
    print("invalid arguments, must provide DNS entries file")
    sys.exit()

def split( str ):
    

def RSserver():

    fDNSRSnames = open(sys.argv[1], "r")
    fDNSRSList = fDNSRSnames.readlines()
    inputEntries = []
    for entry in fDNSRSList:
        print("[RS:] Storing: ",entry)
        inputEntries.append(entry)

    try:
        rs_socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[RS:] RS socket created")
    except mysoc.error as err:
        print('{}\n'.format("RS socket open error",err))

    rs_server_binding=('', 50007)
    rs_socket.bind(rs_server_binding)
    rs_socket.listen(1)
    hostname = mysoc.gethostname()
    print("[RS:] Server hostname:",hostname)
    rs_host_ip = (mysoc.gethostbyname(hostname))
    print("[RS:] IP is",rs_host_ip)
    csockid,addr=rs_socket.accept()
    print("[RS:] connection request from ",addr)

    while True:
        client_data_received = csockid.recv(100).decode('utf-8')
        #if not data:
            #break
        for entry in inputEntries:
            print("[RS:] entry is %s" % entry)
            splitEntry = entry.split("  ")
            print("[RS:] entry 1 is %s" % splitEntry[0])
            print("[RS:] entry 2 is %s" % splitEntry[1])
            print("[RS:] entry 3 is %s" % splitEntry[2])
            entryHostname = splitEntry[0]
            entryCode = splitEntry[2]
            if entryCode == 'NS':
                csockid.send(entryHostname.encode('utf-8'))
            elif entryHostname == client_data_received:
                csockid.send(entryHostname.encode('utf-8'))

    rs_socket.close()
    exit()

RSserver()
