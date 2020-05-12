import math

from bitarray import bitarray

#
# Bloom Filter ########
#


NUM_KEYS = 20
FALSE_POSITIVE_PROBABILITY = 0.05


class BloomFilter(object):

    def __init__(self, NUM_KEYS, FALSE_POSITIVE_PROBABILITY):
        self.size = int(-(NUM_KEYS * math.log(FALSE_POSITIVE_PROBABILITY)) / (math.log(2) ** 2))
        self.bloom_filter = bitarray(self.size)
        self.bloom_filter.setall(0)
        self.number_hash_functions = int((self.size/NUM_KEYS) * math.log(2))

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

if __name__ == '__main__':
    bloomfilter = BloomFilter(NUM_KEYS, FALSE_POSITIVE_PROBABILITY)

    bloomfilter.add('e621944d55b827774fa6f9813ddeacd9')
    print(bloomfilter.is_member('e621944d55b827774fa6f9813ddeacd9'))
