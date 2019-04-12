import socket
import threading


# to obey the WET princinple
import servers
logger = servers.make_logger('ROUTER-00')


def decode(stream):
    # input is byte stream
    body = stream.decode()
    headers, action, message = body.split('\n\n')

    addr, *_ = headers.split('\n')
    host, port = addr.split(':')
    endpoint_addr = (host, int(port))
    
    # listen for kill switch request
    message = message.rstrip()
    if message == 'ENDGAME':
        kill_switch = 1

    return endpoint_addr

def client_handler(conn, addr):
    logger.info(f"NEW CLIENT [{addr[0]}:{addr[1]}]")
    # new connection is open in new thread, wait for message
    stream = conn.recv(1024)

    logger.info(f"CLIENT [{addr[0]}:{addr[1]}] | PACKET RECEIVED")
    forwarding_addr = decode(stream)

    forward_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    forward_conn.connect(forwarding_addr)
    
    forward_conn.send(stream)
    logger.info(f"CLIENT [{addr[0]}:{addr[1]} | PACKET FORWARDED")

    forward_conn_resp = forward_conn.recv(1024)
    logger.info(f"CLIENT [{addr[0]}:{addr[1]}] | RELAY PACKET RECEIVED")

    conn.send(forward_conn_resp)
    logger.info(f"CLIENT [{addr[0]}:{addr[1]}] | RELAY PACKET FORWARDED")

    # closing connection and calling the return statement should close current
    # thread handling this request and return control to the main thread
    logger.info(f"CLOSING CONNECTION WITH CLIENT [{addr[0]}:{addr[1]}]")
    conn.close()

    return

kill_switch = 0
threads = []

def kill_server():
    # wait for or kill each open thread individually
    # and close server 

    # implement later
    pass

def start():
    # just to flex shii, how about using select to handle IO
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 3333))
    server.listen(5)

    logger.info("ROUTER IS UP AND OPEN FOR CONNECTIONS")

    while True:
        # check kill switch first
        if kill_switch == 1:
            break

        # else; listen for new connections
        conn, addr = server.accept()
        new_cc = threading.Thread(target=client_handler, args=(conn, addr,))
        new_cc.start()

    # kill switch has been flipped, server is no longer listening for connections
    logger.info("CLOSING SERVER")
    server.close()

if __name__ == '__main__':
    start()
