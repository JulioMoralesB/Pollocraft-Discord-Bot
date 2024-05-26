from mcstatus import JavaServer

def get_response(user_input: str) -> str:
    message: str = user_input.lower().replace(" ","")
    server = JavaServer.lookup('minecraft.apollox10.com')

    is_server_online = False

    try:
        status = server.status()
        query = server.query()
        current_players = '\n- '.join(query.players.names)
        is_server_online = True
    except TimeoutError as timeout:
        is_server_online = False

    if message == 'info':
        if is_server_online:
            return f'''
                \t- Estado: Online
                \n- IP: minecraft.apollox10.com
                \n- Versión: {str(status.version.name)}
                \n- Número de jugadores actuales: {status.players.online}
                \n- Lista de jugadores actuales: \n\t- {current_players}
                '''
        else:
            return '''
                    \t- Estado: Offline
                    \n- IP: minecraft.apollox10.com
                    \n- Versión: 1.20.4
                    '''

    if message == 'status' or message == 'estatus':
        return 'El servidor está online, puedes unirte a jugar.' if is_server_online else 'El servidor esta offline :c'
        
    if message == 'players' or message == 'jugadores':
        if is_server_online:
            players = status.players.online
            if players == 0:
                return 'Actualmente no hay jugadores online.'
            if players == 1:
                return 'Actualmente solo está 1 jugador conectado.'
            else:
                return f'Actualmente hay {players} jugadores conectados.'
            
        else:
            return 'El servidor esta offline, así que no deberían haber jugadores, en teoría...'
        
    
    if message == 'currentplayers' or message == 'jugadoresactuales':
        return 'Actualmente están jugando: \n\t- ' + current_players if is_server_online else 'El servidor esta offline, así que no deberían haber jugadores, en teoría...'
    
    if message == 'ip':
        return 'minecraft.apollox10.com'
    
    if message == 'version':
        return str(status.version.name) if is_server_online else "La versión debería ser 1.20.4, pero el servidor está actualmente desconectado. Esta info podría no estar actualizada."
    
    if message == 'help' or message == 'ayuda':
        return '''Comandos disponibles (no deben llevar las comillas, ""):
                \t- "?info" : Obtiene toda la información actual del servidor.
                \n- "?status" o "?estatus": Informa si el servidor está dispoinble o no.
                \n- "?players" o "?jugadores": Indica cuantos jugadores están conectados.
                \n- "?current players" o "?jugadores actuales": Muestra en una lista los jugadores que están conectados.
                \n- "?ip": Devuelve la IP del servidor.
                \n- "?version": Devuelve la versión actual del servidor.
                '''
    else:
        return 'null'