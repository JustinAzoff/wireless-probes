import time
import urllib, sys
import signal
import logging

from wirelessprobe.util import make_stats

logger = logging.getLogger(__name__)

class Timeout(Exception):
    pass

class FileDownloader:
    def __init__(self):
        self.log = []
        self.blocks_seen = 0

    def progress_callback(self, blocks, block_size, total_size):
        #blocks->data downloaded so far (first argument of your callback)
        #block_size -> size of each block
        #total-size -> size of the file
        #implement code to calculate the percentage downloaded e.g
        now = time.time()
        if now - self.last > 1:
            speed = self.blocks_seen * block_size / 1024 #speed in KB/s
            pct = 100*blocks/(total_size/block_size)
            logger.debug("dowload progress pct=%d, speed=%d", pct, speed)
            self.log.append(speed)
            self.blocks_seen = 0
            self.last = now
        else:
            self.blocks_seen +=1

    def handle_timeout(self, signum, frame):
        raise Timeout()

    def download(self, site, timeout):
        old = signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(timeout)

        start = time.time()
        self.last = start
        (file, headers) = urllib.urlretrieve(site, "/dev/null", self.progress_callback)
        end = time.time()

        signal.signal(signal.SIGALRM, old)
        signal.alarm(0)
        return end - start

def do_download(url, timeout):
    hit_timeout = False
    elapsed = None
    d = FileDownloader()
    exception=None
    try :
        elapsed = d.download(url, timeout)
    except Timeout:
        hit_timeout=True
        elapsed = timeout
    except Exception, e:
        exception=str(e)

    stats = make_stats(d.log)
    stats["timeout"] = hit_timeout
    stats["elapsed"] = elapsed
    stats['exception'] = exception
    return stats

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) !=2:
        print "Usage: download.py <url> "
        sys.exit(1)

    d = FileDownloader()
    site = sys.argv[1]
    print do_download(site, 3)
