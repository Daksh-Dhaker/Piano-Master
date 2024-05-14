import socket
import pickle
import struct


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "20.189.122.137"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)
        # self.client_number = int((self.client.getsockname())[1])
        self.client_number = pickle.loads(self.recv_one_message())
        print(self.client_number)

    def send(self, data):
        temp = data
        data = pickle.dumps(data)
        self.send_one_message(data)
        ans = None
        if temp != "DISCONNECTED":
            try:
                ans = pickle.loads(self.recv_one_message())
            except Exception as e:
                print(e)

        return ans

    def send_bin(self, data):
        print(len(data))
        self.send_one_message(data)

    def send_one_message(self, data):
        length = len(data)
        self.client.sendall(struct.pack("!I", length))
        self.client.sendall(data)

    def recv_one_message(self):
        lengthbuf = self.recvall(4)
        if lengthbuf:
            (length,) = struct.unpack("!I", lengthbuf)
            return self.recvall(length)
        else:
            return None

    def recvall(self, count):
        buf = b""
        while count:
            newbuf = self.client.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def getP(self):
        return self.p
