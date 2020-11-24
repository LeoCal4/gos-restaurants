"""
Background tasks entrypoint.
"""
from restaurants import create_app
from kombu import Connection
import threading
import logging

# First initialize application, disabling the rabbit producer
app = create_app(rabbit_producer_enabled=False)


def start_workers():
    """This function basically retrieves all workers from comm.workers package
    and starts a new daemon thread.
    """
    # retrieve all workers
    from restaurants.comm.workers import worker_list

    for worker in worker_list:
        with Connection(app.config['RABMQ_RABBITMQ_URL'], heartbeat=4) as conn:
            worker = worker(conn, logging)
            thread = threading.Thread(target=worker.run)
            thread.start()
            logging.info("Started new worker thread %s" % worker)


if __name__ == '__main__':
    _format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=_format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    start_workers()
    logging.info('All workers are started!')
