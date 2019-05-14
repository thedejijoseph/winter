import router
import server
import client

router.start()
server.spurn_servers(3)
client.spurn_clients(6)
