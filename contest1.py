import enet

def main():
    if enet.initialize() != 0:
        print("Failed to initialize ENet.")
        return

    address = enet.Address("localhost", 1234)
    client = enet.Host(None, 1)

    server_peer = client.connect(address, 1, 0)
    if server_peer.state != enet.PeerState.CONNECTED:
        print("Failed to connect to server.")
        return

    print("Connected to server.")

    while True:
        event = client.service(1000)
        if event.type == enet.EVENT_TYPE.CONNECT:
            print("Connected to server.")
        elif event.type == enet.EVENT_TYPE.DISCONNECT:
            print("Disconnected from server.")
            break
        elif event.type == enet.EVENT_TYPE.RECEIVE:
            print("Received message from server:", event.packet.data)

if __name__ == "__main__":
    main()
