
class Process:
    def __init__(self, pid, arrival_t, elapse, *rest_args):
        self.rest_args = rest_args
        self.arrival_t = arrival_t
        self.elapse = elapse
        self.pid = pid

        self.time_runned = 0
        self.turnaround_time = 0
        self.response_time = 0

    def __str__(self):
        return f'PID:{self.pid} (rt: {self.response_time}, ta: {self.turnaround_time})'
    
    __repr__ = __str__
    
    def clone(self):
        return Process(self.pid, self.arrival_t, self.elapse, self.rest_args[:])

    def is_done(self):
        return self.elapse == self.time_runned

    def left(self):
        return self.elapse - self.time_runned

    def run(self, now, time = 1):
        if self.is_done():
            return True
        if self.time_runned == 0:
            self.response_time = now - self.arrival_t
        self.time_runned += time
        if self.is_done():
            self.turnaround_time = now + time - self.arrival_t
            return True
        return False
