import urllib3
import random

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

http = urllib3.PoolManager()
response = http.request('GET', word_site)
txt = response.data.decode('utf-8')
WORDS = txt.splitlines()

count = 50
count = min(count, len(WORDS))
random_words = random.sample(WORDS, count)
print(random_words)