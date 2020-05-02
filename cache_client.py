import sys
import socket

from node_ring import NodeRing
from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE

from bloomfilter import BloomFilter
import lru

# set_LRU_cache_size(3)
lru.set_LRU_cache_size(3)
bloomFilter = BloomFilter()

BUFFER_SIZE = 1024

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)       

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()

    @lru.lru_cache
    def put(self, key, payload):
        bloomFilter.add(key)
        return self.send(payload)

    @lru.lru_cache
    def get(self,key,payload):
        if bloomFilter.is_member(key):
            return self.send(payload)

    @lru.lru_cache
    def delete(self, key, payload):
        if bloomFilter.is_member(key):
            return self.send(payload)


def process(udp_clients):
    hash_codes = set()
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        ring = NodeRing(NODES)
        server_index = NODES.index(ring.get_node(key))
        response = udp_clients[server_index].put(key,data_bytes)
        hash_codes.add(response.decode())
        print(response)

    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    # print(lru.cache.cache)
    
    # TODO: PART I
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        ring = NodeRing(NODES)
        server_index = NODES.index(ring.get_node(key))
        response = udp_clients[server_index].get(hc,data_bytes)
        print(response)

    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_DELETE(hc)
        ring = NodeRing(NODES)
        server_index = NODES.index(ring.get_node(key))
        response = udp_clients[server_index].delete(key,data_bytes)
        print(response)


if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)
