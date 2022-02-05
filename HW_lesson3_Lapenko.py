import collections
import functools

import pandas as pd
import requests
import tracemalloc

# 1. Реалізувати LFU алгоритм для кешування.
# За базу берем існуючий декоратор.Написати для фетчування юерелів. Додати можливість указати максимум елементів в кеші.

def cache_lfu(max_limit=80):
    def internal(anyone_function):
        cache = {}
        freq_count = collections.Counter()

        @functools.wraps(anyone_function)
        def deco(*args, **kwargs):
            cache_key = args
            freq_count[cache_key] += 1
            try:
                result = cache[cache_key]
                deco.hits += 1
            except KeyError:
                result = anyone_function(*args, **kwargs)
                cache[cache_key] = result
                deco.misses += 1

            if len(cache) >= max_limit:
                for cache_key, _ in pd.nsmallest(pd.maxsize // 10,
                                                 freq_count.pd.iteritems(),
                                                 cache_key=pd.itemgetter(1)):
                    del cache[cache_key], freq_count[cache_key]
            return result

        def clear():
            cache.clear()
            freq_count.clear()
            deco.hits = deco.misses = 0

        deco.hits = deco.misses = 0
        deco.clear = clear
        return deco

    return internal


@cache_lfu()
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content

# 2. Створити декоратор для заміру пам'яті.

def fetch_url_1(url):
    res = requests.get(url)
    print(f'\nContent for "{url}":\t ', res.content[:100])

def profile_memo(f):
    def internal(url):
        tracemalloc.start()
        f(url)
        stat = tracemalloc.get_traced_memory()
        print("[ tracemalloc stats ]")
        print(f'Current memo: {stat[0]}, Peak memo: {stat[1]}')
    return internal

fetch_url_profiled = profile_memo(fetch_url_1)
fetch_url_profiled('https://google.com')
fetch_url_profiled('https://ithillel.ua')
fetch_url_profiled('https://lms.ithillel.ua')


