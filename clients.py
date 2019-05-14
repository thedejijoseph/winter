import socket
import threading
import random
import servers

server_list = [('localhost', port) for port in range(3301, 3304)]
resource_list = [1, 2, 3, 4, 5, 6]


def encode_request(endpoint, uri):
    endpoint = f"{endpoint[0]}:{endpoint[1]}"
    header = "\n".join([endpoint, 'close'])
    action = f"get /{uri}"
    message = ""

    request = "\n\n".join([header, action, message])
    return request

def decode_response(stream):
    resp = stream.decode()
    header, status, message = resp.split('\n\n')
    return message

def client_bot(bot_id):
    logger = servers.make_logger(f"CLIENT-{bot_id}")
    logger.info(f"BOT {bot_id} SPURNED")

    for i in range(3):
        endpoint = random.choice(server_list)
        uri = random.choice(resource_list)
        request = encode_request(endpoint, uri)

        logger.info(f"CONNECTING TO {endpoint}")
        conn, port = make_conn('localhost', 3333) # router address

        conn.send(bytes(request, 'utf-8'))
        logger.info(f"REQUEST SENT FOR RESOURCE {uri}")

        response = conn.recv(1024)
        message = decode_response(response)
        logger.info(f"RESPONSE RECEIVED | {message}")

    logger.info("CLOSING CONNECTION")
    conn.close()

    return

def make_conn(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, int(port)))
    return client, port

def make_client(host, port):
    return make_conn(host, port)

#if __name__ == "__main__":
    # spurn x number of client bots
for i in range(3):
    bot = threading.Thread(target=client_bot, args=(i,))
    bot.start()
