import zmq

def listen():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://0.0.0.0:5555")
    socket.subscribe("")

    while True:
        event = socket.recv()
        print(event)


if __name__ == "__main__":
    listen()
