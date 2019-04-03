import socket
import logging
import threading

class ParseError(Exception):
    pass

resource_pool = {
        '/1': 'TONY STARK; IRON MAN',
        '/2': 'STEVE ROGERS; CAPTAIN AMERICA',
        '/3': 'THOR ODINSON',
        '/4': 'BRUCE BANNER; HULK',
        '/5': 'CLINT BARTON; HAWKEYE',
        '/6': 'NATASHA ROMANOFF; BLACK WIDOW'
        }

class Request:
    def __init__(self, stream):
        if not isinstance(stream, bytes):
            raise ParseError("'stream' must be of type 'bytes'")

        self.body = stream.decode()
        header, action, message = self.body.split("\n\n")

        self.headers = header.split("\n")
        self.method, self.uri = action.split(" ")
        self.message = message.strip()
    
    def get_response(self):
        resp = resource_pool.get(self.uri)
        return Response(self, resp)

class Response:
    def __init__(self, req, resp):
        header = req.headers
        
        if resp:
            status_code = '200'; reason = 'OK'
        else:
            status_code = '404'; reason = 'NOT FOUND'
        status = f"{status_code}; {reason}"

        message = f"{resp}\n-ALLFATHER, SIMNET"

        self.headers = '\n'.join(header)
        self.status = status
        self.message = message

        self.body = '\n\n'.join([self.headers, self.status, self.message])

def make_logger(server_name):
    logger = logging.getLogger(server_name)
    log_format = logging.Formatter('[%(name)s] %(asctime)s | %(message)s')
    
    f_handler = logging.FileHandler(f'logs\{server_name}.log')
    f_handler.setLevel(10); f_handler.setFormatter(log_format)

    c_handler = logging.StreamHandler()
    c_handler.setLevel(10); c_handler.setFormatter(log_format)
    
    logger.addHandler(f_handler); logger.addHandler(c_handler)
    logger.setLevel(10)
    return logger

def spurn_server(server_name, host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    logger = make_logger(server_name)
    logger.info(f"SERVER OPEN AT [{host}:{port}]")

    server.listen(3)
    # for i in range(3): # stay open for n connections
    while True:
        conn, addr = server.accept()
        logger.info(f'NEW CONNECTION FROM [{addr[0]}:{addr[1]}]')

        stream = conn.recv(1024);
        request = Request(stream)
        logger.info(f"REQUEST FOR RESOURCE {request.uri}")

        response = request.get_response()
        conn.send(bytes(response.body, 'utf-8'))

        logger.info("RESPONSE SENT; CLOSING CONNECTION")
        conn.close()

    logger.info("CLOSING SERVER")
    server.close()

def spurn(n):
    # n: number of servers to provision
    ports = list(range(3301, 3310))[:n]
    host = 'localhost'
    server_list = [(f'SERVER-{str(port)[2:]}', host, port) for port in ports]


    for server in server_list:
        server_name, host, port = server
        new_thread = threading.Thread(target=spurn_server, args=(server_name, host, port))
        new_thread.start()

if __name__ == '__main__':
    spurn(3)
