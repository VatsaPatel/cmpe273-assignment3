import hashlib

from server_config import NODES

class NodeRing():

    def __init__(self, nodes):
        assert len(nodes) > 0
        self.nodes = nodes
    
    def get_node(self, key_hex):
        key = int(key_hex, 16)
        sha = hashlib.sha1(str(key).encode("utf-8"))
        temp = sha.hexdigest().encode("utf-8")
        hashval = int(hashlib.sha1(temp).hexdigest(), 16) % (10 ** 15)
        node_index = hashval % len(self.nodes)
        return self.nodes[node_index]


def test():
    ring = NodeRing(nodes=NODES)
    node = ring.get_node('9ad5794ec94345c4873c4e591788743a')
    print(node)
    print(ring.get_node('ed9440c442632621b608521b3f2650b8'))


test()
