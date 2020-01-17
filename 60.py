'''
https://www.pythonsheets.com/notes/python-asyncio.html
'''

import asyncio
import socket
import time

async def get(path):
    loop = asyncio.get_running_loop()
    sock = socket.socket()
    sock.setblocking(False)
    await loop.sock_connect(sock, ('localhost', 5000))
    data = ('GET %s HTTP/1.0\r\n\r\n' % path).encode()
    await loop.sock_sendall(sock, data)

    buf = []
    while True:
        chunk = await loop.sock_recv(sock, 1000)
        if not chunk:
            break
        buf.append(chunk)

    return (b''.join(buf)).decode().split('\n')[0]

async def main():
    start = time.time()
    task1 = asyncio.create_task(get('/foo'))
    task2 = asyncio.create_task(get('/bar'))
    group = asyncio.gather(task1, task2)
    await group
    for data in group.result():
        print(data)
    print('took %.2f seconds' % (time.time() - start))
asyncio.run(main())
