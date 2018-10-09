import socket as mysoc

def RSserver():
    try:
        rs_socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S:] RS socket created")
    except mysoc.error as err:
        print('{}\n'.format("RS socket open error",err))

    rs_server_binding('', 50007)
    rs_socket.bind(server_binding)
    rs_socket.listen(1)
    hostname = mysoc.gethostname()
    print("[RS:] Server hostname:",hostname)
    rs_host_ip = (mysoc.gethostbyname(host))
    print("[RS:] IP is",rs_host_ip)
    csockid,addr=ss.accept()
    print("[RS:] connection request from ",addr)

    # TODO: store read-in file into array of strings
    # TODO: on acess - split on (" ") which separates string into array
    # TODO: check first s_received[0] with s_table[0] for every string and check match  

    #Read data from DNSRS and store in data structure
    #Receive data from client
    #   if hostname found in data structure return resolved entry
    #   else forward data from client to TS server


RSserver()
