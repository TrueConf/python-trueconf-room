import trueconf_room
from trueconf_room.methods import Methods
from trueconf_room.consts import EVENT, METHOD_RESPONSE
import trueconf_room.consts as C
import config

room = trueconf_room.open_session(ip = config.IP, port = config.PORT, pin = config.PIN, debug = config.DEBUG)
methods = Methods(room)

@room.handler({})
def on_all(response):
    print(f'    @@@ {response}')

if __name__ == '__main__':
    room.run()
