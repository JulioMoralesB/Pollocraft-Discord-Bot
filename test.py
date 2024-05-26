from mcstatus import JavaServer
server = JavaServer.lookup('minecraft.apollox10.com')
print('Requesting status...')
status = server.status()
query = server.query()


print(status)
print ("Total players: " + str(status.players.online))
players = '\n '.join(query.players.names)
print("Currently playing: " + players)
