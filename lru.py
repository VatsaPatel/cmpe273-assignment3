from collections import OrderedDict


class LRUCache(object):

    def __init__(self, max_length=5):
        self.cache = OrderedDict()
        self.length = max_length

    def __setitem__(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            self.cache[key] = value
            if len(self.cache) > self.length:
                self.cache.popitem(last=False)

    def __getitem__(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        else:
            return 0

    def __delitem__(self, key):
        del self.cache[key]

#
cache = None
#
def set_LRU_cache_size(i):
    global cache
    cache = LRUCache(i)

def lru_cache(func):
    def LRUwrapper(obj, key, payload):
        if func.__name__ == 'get':
            temp = cache[key]
            if temp:
                return temp
            else:
                return func(obj, key, payload)

        elif func.__name__ == 'put':
            cache[key]=payload
            return func(obj, key, payload)

        elif func.__name__ == 'delete':
            if cache[key]:
                del cache[key]
            return func(obj, key, payload)

    return LRUwrapper


def test():
    cache[1] = 2
    cache[2] = 3
    cache[3] = 4
    cache[4] = 5
    cache[1] = 2

    @lru_cache
    def get(key, value):
        return 'GET server'

    @lru_cache
    def put(key,value):
        return 'PUT to server'

    @lru_cache
    def delete(key, value):
        return 'del server'

    print(put(4, 5))

    print(get(4, 4))

    print(delete(4, 4))

    print(cache.cache)

# main()
