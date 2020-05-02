from bitarray import bitarray

#
# Bloom Filter ########
#  Calculation with n=500 & p=0.01
#  Then k=7 & m=4797
#

class BloomFilter(object):

    def __init__(self, size=4797):
        self.size = size
        self.bloom_filter = bitarray(self.size)
        self.bloom_filter.setall(0)
        self.number_hash_functions = 7

    def _hash_djb2(self, s):
        hash_temp = 5381
        for x in s:
            hash_temp = ((hash_temp << 5) + hash_temp) + ord(x)
        return hash_temp % self.size

    def _hash(self, item, K):
        return self._hash_djb2(str(K) + item)

    def add(self, item):
        for i in range(self.number_hash_functions):
            self.bloom_filter[self._hash(item, i)] = 1

    def is_member(self, item):
        for i in range(self.number_hash_functions):
            if self.bloom_filter[self._hash(item, i)] == 1:
                return True
        return False

bloom_filter = BloomFilter()
# base_ip = "192.168.1."
# bloom_filter.add(base_ip + str(1))
#
# for i in range(1, 100):
#     if not bloom_filter.is_member(base_ip + str(i)):
#         print(base_ip + str(i))

bloom_filter.add('e621944d55b827774fa6f9813ddeacd9')
print(bloom_filter.is_member('e621944d55b827774fa6f9813ddeacd9'))