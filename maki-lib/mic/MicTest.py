import Mic
import sys

HOST='localhost'
PORT=2000

def received_data(data):
    pass

if sys.argv[1] == 'rx':
    rx = Mic.MicReceiver(received_data)
    rx.listen(HOST, PORT)
elif sys.argv[1] == 'tx':
    tx = Mic.MicTransmitter()
    if tx.start(HOST, PORT):
        input('Press any key to stop.')
        print('Stopping connection.')
        tx.stop()
    else:
        print('Connection refused.')

