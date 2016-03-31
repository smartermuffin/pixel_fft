from threading import Lock

class RingBuffer:
    """ class that implements a not-yet-full buffer """
    def __init__(self,size_max):
        self.max = size_max
        self.data = []
        self.lock = Lock()

    class __Full:
        """ class that implements a full buffer """
        def append(self, x):
            self.lock.acquire(True)
            """ Append an element overwriting the oldest one. """
            self.data[self.cur] = x
            self.cur = (self.cur+1) % self.max
            self.lock.release()
        def get(self):
            """ return list of elements in correct order """
            self.lock.acquire(True)
            x= self.data[self.cur:]+self.data[:self.cur]
            self.lock.release()
            return x

    def append(self,x):
        """append an element at the end of the buffer"""
        self.lock.acquire(True)
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self.__Full
        self.lock.release()
   
    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        self.lock.acquire(True)
        x= list(self.data)
        self.lock.release()
        return x

