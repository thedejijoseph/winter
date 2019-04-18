import servers
import router
import clients

servers.spurn_servers(3)
router.start()
clients.spurn_bots(3)