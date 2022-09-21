from process import Process
from collections import namedtuple
Record = namedtuple('Record', ['process_runed', 'media_time', 'time_elapsed'])

def time_runner(init_time: int,step: int):
    time = init_time
    while True:
        yield time
        time += step


##########
# Parser #
##########
def get_line():
    _input: list = None
    while not _input or _input[0] == '#':
        _input = input()
        _input = '' if not _input else _input.split('#', 1)[0]
    return _input.split()
    
def parser_input():
    jobs_count = int(get_line()[0])
    Q = int(get_line()[0])
    E = [int(integ) for integ in get_line()]
    jobs = []

    for i in range(jobs_count):
        info = get_line()
        jobs.append(Process(i, *(map(int,info))))

    return jobs, jobs_count, Q, E
