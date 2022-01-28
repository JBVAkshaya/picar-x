from readerwriterlock import rwlock

class Bus:
    def __init__(self):
        self.lock = rwlock.RWLockWriteD()
        self._message = None
    
    def write(self, message):
        with self.lock.gen_wlock():
            self._message = message
    
    def read(self):
        with self.lock.gen_rlock():
            message = self._message
        return message