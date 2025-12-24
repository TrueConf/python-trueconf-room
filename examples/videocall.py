import trueconf_room
from trueconf_room.methods import Methods
from trueconf_room.consts import EVENT, METHOD_RESPONSE
import trueconf_room.consts as C
import config

room = trueconf_room.open_session(ip = config.IP, port = config.PORT, pin = config.PIN, debug = config.DEBUG)
methods = Methods(room)

@room.handler(EVENT[C.EV_appStateChanged])
@room.handler(METHOD_RESPONSE[C.M_getAppState])
def on_state_change(response):
    print(f'    Application state is {response["appState"]}')

    if response["appState"] == 5:
        print("\nDone! We are in the conference!\n")

@room.handler(EVENT[C.EV_rejectReceived])
def on_reject(response):
    print('Reject received')
    print(f'    Cause: {response["cause"]}')
    print(f'           {C.CAUSE[response["cause"]]}')

if __name__ == '__main__':
    print("Calling...")
    methods.call("\c\demo_conf")
    room.run()
