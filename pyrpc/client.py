import time

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.transport import TSocket

from pyrpc import __version__
import pyrpc.rpc.pyrpc.pyrpc as server
import pyrpc.rpc.constants as constants


class Client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._connect_to_server()

    def _connect_to_server(self):
        tsocket = TSocket.TSocket(self.host, self.port)
        transport = TTransport.TBufferedTransport(tsocket)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self._client = server.Client(protocol)
        transport.open()
        begin = time.time()
        self._client.ping()
        response_time = int((time.time() - begin) * 1000)
        print(f'Connect to server. Response time {response_time}ms.')
        if self._client.version() != __version__:
            raise Exception('Version mismatch! Update project.')


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Python RPC client')
    parser.add_argument('-i', '--ip', type=str, default='127.0.0.1',
                        help='Host IP')
    parser.add_argument('-p', '--port', type=int, default=constants.PORT,
                        help='Host Port')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    Client(args.ip, args.port)
