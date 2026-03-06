python3 -c "
import hashlib, time

datos = b'data de prueba' * 10000
algoritmos = ['md5', 'sha1', 'sha256', 'sha512']

for algo in algoritmos:
    start = time.time()
    for _ in range(10000):
        hashlib.new(algo, datos).hexdigest()
    elapsed = (time.time() - start) * 1000
    print(f'{algo.upper():10} -> {elapsed:.0f} ms para 10,000 hashes')
"
