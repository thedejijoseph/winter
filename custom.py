import threading

class Thread(threading.Thread):
    def __init__(self, target=None, args=()):
        threading.Thread.__init__(self)
        self._target = target
        self._args = args

        self.kill = threading.Event()

    def kill_thread(self):
        self.kill.set()
