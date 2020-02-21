from threading import Thread

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.server import TServer

import pyrpc.rpc.pyrpc.pyrpc as server
import pyrpc.rpc.constants as constants
from pyrpc import __version__


class Handler(object):
    def ping(self):
        return

    def version(self):
        return __version__


class ServerThread(Thread):
    def __init__(self, port):
        super(ServerThread, self).__init__()
        self.daemon = True
        self.host = '0.0.0.0'
        self.port = port
        self.handler = None

    def run(self):
        self.handler = Handler()
        processor = server.Processor(self.handler)
        transport = TSocket.TServerSocket(self.host, self.port)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        rpc_server = TServer.TThreadPoolServer(processor, transport, tfactory,
                                               pfactory)
        rpc_server.setNumThreads(100)

        print('Starting the RPC at', self.host, ':', constants.PORT)
        rpc_server.serve()


class Server(object):
    def __init__(self, port):
        self.port = port

    def start(self):
        import time
        self.server_thread = ServerThread(self.port)
        self.server_thread.start()
        time.sleep(0.5)
        while True:
            cmd = input()
            if cmd == 'exit' or cmd == 'e':
                break


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Python RPC server')
    parser.add_argument('-p', '--port', type=int, default=constants.PORT,
                        help='Host Port')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    Server(args.port).start()
