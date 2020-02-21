import multiprocessing as mp

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


class ServerProc(mp.Process):
    def __init__(self, port):
        super(ServerProc, self).__init__()
        self.daemon = True
        self.host = '0.0.0.0'
        self.port = port

    def run(self):
        handler = Handler()
        processor = server.Processor(handler)
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
        self.server_proc = ServerProc(self.port)
        self.server_proc.start()
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
