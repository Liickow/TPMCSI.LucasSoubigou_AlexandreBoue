from oscpy.server import OSCThreadServer
import socket
import sys
import time

address = ('localhost', 6006)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def dump(address, *values):
    print(u'{}: {}'.format(
        address.decode('utf8'),
        ', '.join(
            '{}'.format(
                v.decode(options.encoding or 'utf8')
                if isinstance(v, bytes)
                else v
            )
            for v in values if values
        )
    ))


global accel
global brake
global left
global right
right = 0

def callbackX(*x):
    if(x[0] > 0.20) :
        data = b'P_ACCELERATE'
        client_socket.sendto(data, address)

    elif (x[0] < -0.40) :
        data = b'P_BRAKE'
        client_socket.sendto(data, address)
    else:
        data = b'R_ACCELERATE'
        client_socket.sendto(data, address)
        data = b'R_BRAKE'
        client_socket.sendto(data, address)
    

def callbackY(*y):
    if(y[0] > 0.20) :
        right = y[0]
    elif (y[0] < -0.20) :
        right = y[0]
    else :
        right = 0

def callbackTouch(*touch):
    timeStart = time.time()
    if touch :
        if(timeStart - time.time() < 1) :
            data = b'FIRE'
            client_socket.sendto(data, address)

        data = b'R_RIGHT'
        client_socket.sendto(data, address)
        data = b'R_LEFT'
        client_socket.sendto(data, address)
        data = b'R_ACCELERATE'
        client_socket.sendto(data, address)
        data = b'R_BRAKE'
        client_socket.sendto(data, address)
        timeStart = time.time()


osc = OSCThreadServer(default_handler=dump)  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='0.0.0.0', port=8000, default=True)

osc.bind(b'/multisense/pad/x', callbackX)
osc.bind(b'/multisense/pad/y', callbackY)
osc.bind(b'/multisense/pad/touchUP', callbackTouch)

while True:

    if(left):
        data = b'P_LEFT'
        client_socket.sendto(data, address)
    else:
        data = b'R_LEFT'
        client_socket.sendto(data, address)
    if(right):
        data = b'P_RIGHT'
        client_socket.sendto(data, address)
    else:
        data = b'R_RIGHT'
        client_socket.sendto(data, address)
    if(accel):
        data = b'P_ACCELERATE'
        client_socket.sendto(data, address)
    else:
        data = b'R_ACCELEARTE'
        client_socket.sendto(data, address)
    if(brake):
        data = b'P_BRAKE'
        client_socket.sendto(data, address)
    else:
        data = b'R_BRAKE'
        client_socket.sendto(data, address)


    time.sleep(0.016)
osc.stop()  # Stop the default socket