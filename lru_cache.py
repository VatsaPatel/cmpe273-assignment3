from collections import OrderedDict


class LRUCache(object):
    length = 5
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

    def update_length(self,i):
        self.length = i

#
cache = LRUCache(5)
#
def set_LRU_cache_size(i):
    global cache
    cache = LRUCache(i)

def lru_cache(cache_size):
    def decorator(func):
        cache.update_length(cache_size)
        def LRUwrapper(*args, **kw):
            if func.__name__ == 'get_request':
                obj = args[0]
                key=args[1]
                payload = args[2]
                temp = cache[key]

                if temp:
                    return temp
                else:
                    return func(obj, key, payload)

            elif func.__name__ == 'put':
                obj = args[0]
                key = args[1]
                payload = args[2]

                cache[key]=payload
                return func(obj, key, payload)

            elif func.__name__ == 'delete':
                obj = args[0]
                key = args[1]
                payload = args[2]

                if cache[key]:
                    del cache[key]
                return func(obj, key, payload)

            else:
                key = args[0]
                temp = cache[key]

                if temp:
                    print(f"[cache-hit] {func.__name__}({key}) -> {temp}")
                    return temp
                else:
                    y = func(key)
                    cache[key] = y
                    print(f"[cache-missed] {func.__name__}({key}) -> {y}")
                    return y


            return func(*args, **kw)
        return LRUwrapper
    return decorator

if __name__ == '__main__':
    def test():
        cache[1] = 2
        cache[2] = 3
        cache[3] = 4
        cache[4] = 5
        cache[1] = 2

        @lru_cache(5)
        def get(key, value):
            return 'GET server'

        @lru_cache(5)
        def put(key,value):
            return 'PUT to server'

        @lru_cache(5)
        def delete(key, value):
            return 'del server'

        print(put(4, 5))

        print(get(4, 4))

        print(delete(4, 4))

        print(cache.cache)

    test()
