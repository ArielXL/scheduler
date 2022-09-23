from utils import Record,time_runner
from process import Process
from collections import deque
from random import choice

class PolicyRunner:
    def __init__(self, jobs: list, E: int, Q: int=10):
        self.total_time    = 0
        self.current_proc = None
        
        self.jobs = jobs
        self.jobs.sort(key=lambda item: item.arrival_t, reverse=True)
        self.jobs_orig = [p.clone() for p in jobs]
        self.pending = []
        self.finished = []
        self.Q = Q
        self.E = E

        self.rt_m = 0
        self.ta_m = 0
        self.METHOD = 'NONE'
    
    def new_jobs_at(self, time=0):
        time = time - (time % self.Q)
        while len(self.jobs) and self.jobs[-1].arrival_t <= time:
            self.pending.append(self.jobs.pop())

    def meta_info_setter(self):
        self.finished.sort(key=lambda it: it.pid)
        self.rt_m = sum(e.response_time for e in self.finished)/len(self.finished)
        self.ta_m = sum(e.turnaround_time for e in self.finished)/len(self.finished)
        
    def __str__(self):
        return '%s| %3.2f|%3.2f' % (self.METHOD,self.rt_m,self.ta_m) 
    
    __repr__ = __str__
    
    def initialize(self):
        pass

    def choose_next(self):
        pass
    
    def start(self) -> Record:
        pass

#FIFO
class FCFS(PolicyRunner):
    def initialize(self):
        self.METHOD='FIFO'
        self.pending = deque([])

    def choose_next(self, bef_job=None,time=0) -> Process:
        if bef_job != None and not bef_job.is_done():
            return bef_job
        return None if len(self.pending) == 0 else self.pending[0]

    def end_process(self):
        self.finished.append(self.current_proc)
        return self.pending.popleft().pid

    def start(self) -> Record:
        self.initialize()

        for t in time_runner(0, 1): 
            if t % self.Q == 0:
                self.new_jobs_at(time=t)
    
            if len(self.jobs) == 0 and len(self.pending) == 0:
                break
            elif len(self.pending) == 0:
                continue
                
            self.current_proc = self.choose_next(self.current_proc, t)
            ended = self.current_proc.run(t)
            
            if ended:
                self.end_process()
        
        self.total_time = t
        self.meta_info_setter()
        return self


class STF(PolicyRunner):
    def initialize(self):
        self.METHOD='STF '
        self.pending = deque([])
        self.jobs.sort(key=lambda item: item.arrival_t, reverse=True)

    def choose_next(self, bef_job=None,time=0) -> Process:
        if bef_job != None and not bef_job.is_done():
            return bef_job
        return None if len(self.pending) == 0 else self.get_min(time)
    
    def get_min(self, time):
        _min_t = min(j.elapse for j in self.pending)
        for j in self.pending:
            if j.elapse == _min_t:
                break
        return j

    def end_process(self):
        self.finished.append(self.current_proc)
        self.pending.remove(self.current_proc)

    def start(self) -> Record:
        self.initialize()

        for t in time_runner(0, 1): 
            if t % self.Q == 0:
                self.new_jobs_at(time=t)
    
            if len(self.jobs) == 0 and len(self.pending) == 0:
                break
            elif len(self.pending) == 0:
                continue

            self.current_proc = self.choose_next(self.current_proc, t)
            ended = self.current_proc.run(t)
            
            if ended:
                self.end_process()
        
        self.total_time = t
        self.meta_info_setter()
        return self


class STCF(PolicyRunner):
    def initialize(self):
        self.METHOD='STCF'
        self.pending = []
        self.jobs.sort(key=lambda item: item.arrival_t, reverse=True)

    def choose_next(self, bef_job=None,time=0) -> Process:
        return None if len(self.pending) == 0 else self.get_min(time)
    
    def get_min(self, time):
        _min_t = min(j.left() for j in self.pending)
        for j in self.pending:
            if j.left() == _min_t:
                break
        return j

    def end_process(self):
        self.finished.append(self.current_proc)
        self.pending.remove(self.current_proc)

    def start(self) -> Record:
        self.initialize()

        for t in time_runner(0, 1): 
            if t % self.Q == 0:
                self.new_jobs_at(time=t)
    
            if len(self.jobs) == 0 and len(self.pending) == 0:
                break
            elif len(self.pending) == 0:
                continue

            self.current_proc = self.choose_next(self.current_proc, t)
            ended = self.current_proc.run(t)
            
            if ended:
                self.end_process()
        
        self.total_time = t
        self.meta_info_setter()
        return self


class RR(PolicyRunner):
    def __init__(self, jobs: list, E: int, Q: int=10):
        self.total_time = 0
        
        self.Ei = 0
        self.current_proc = None
        
        self.jobs = None
        jobs.sort(key=lambda item: item.arrival_t, reverse=True)
        self.jobs_orig = [p.clone() for p in jobs]
        self.pending = []
        self.finished = [[] for _ in E]
        self.Q = Q
        self.E = E

        self.total_time = [0 for _ in E]
        self.rt_m = [0 for _ in E]
        self.ta_m = [0 for _ in E]
        self.METHOD = 'RR-E'
    
    def restore_jobs(self):
        self.jobs = [p.clone() for p in self.jobs_orig]
        
    def meta_info_setter(self):
        self.finished[self.Ei].sort(key=lambda it: it.pid)
        self.rt_m[self.Ei] = sum(e.response_time for e in self.finished[self.Ei])/len(self.finished)
        self.ta_m[self.Ei] = sum(e.turnaround_time for e in self.finished[self.Ei])/len(self.finished)
  
    def __str__(self):
        s = f'|RR-E            \n'
        for i in range(len(self.E)):
            s += '%4d| %.2f|%.2f%s' % (self.E[i],self.rt_m[i],self.ta_m[i],' ' if i == len(self.E)-1 else '\n')
        return s

    __repr__ = __str__
    
    def start(self):
        for i in range(len(self.E)):
            self.Ei = i
            self.start_at(i)
        return self

    def initialize(self):
        self.pending = []
        self.restore_jobs()

    def choose_next(self, bef_job=None,time=0) -> Process:
        if bef_job != None and not bef_job.is_done() and time % self.E[self.Ei]:
            return bef_job
        return None if len(self.pending) == 0 else self.get_rand(bef_job)
    
    def get_rand(self, bef_job):
        if bef_job not in self.pending:
            return self.pending[0]
        index = (self.pending.index(bef_job) + 1) % len(self.pending)
        return self.pending[index]

    def end_process(self):
        self.finished[self.Ei].append(self.current_proc)
        self.pending.remove(self.current_proc)

    def start_at(self, Ei) -> Record:
        self.initialize()

        for t in time_runner(0, 1): 
            if t % self.Q == 0:
                self.new_jobs_at(time=t)
    
            if len(self.jobs) == 0 and len(self.pending) == 0:
                break
            elif len(self.pending) == 0:
                continue

            self.current_proc = self.choose_next(self.current_proc, t)
            ended = self.current_proc.run(t)
            
            if ended:
                self.end_process()
        
        self.total_time[self.Ei] = t
        self.meta_info_setter()
        return self
