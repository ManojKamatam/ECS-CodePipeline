import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 30
keepalive = 2

# Logging
errorlog = "-"
loglevel = "debug"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Server hooks
def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def on_exit(server):
    server.log.info("Server is shutting down")
