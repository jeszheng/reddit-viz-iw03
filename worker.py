import os
import redis
from rq import Worker, Queue, Connection

# -----------------------------------------------------------------------------#
# worker.py
# -----------------------------------------------------------------------------#
# File that runs the worker dyno for the background computations on each
# new dataset query.
# -----------------------------------------------------------------------------#

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
