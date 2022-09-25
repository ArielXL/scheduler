from utils import parser_input
from policies import FCFS, STF, STCF, RR

def pprint_jobs(fifo, stf, stcf, rr):
    print('\n----------jobs------------\n')
    for i in range(N):
        print(f'pid:{fifo.finished[i].pid} fifo({fifo.finished[i].response_time}, {fifo.finished[i].turnaround_time}) ',end='')
        print(f'stf({stf.finished[i].response_time}, {stf.finished[i].turnaround_time}) ',end='')
        print(f'stcf({stcf.finished[i].response_time}, {stcf.finished[i].turnaround_time}) ',end='')
        print('rr[', end=' ')
        print(' '.join(f'{E[e]}=({rr.finished[e][i].response_time}, {rr.finished[e][i].turnaround_time})'
                        for e in range(len(E))),']')
    
def print_jobs(fifo, stf, stcf, rr):
    for i in range(N):
        print(f'{fifo.finished[i].response_time} {fifo.finished[i].turnaround_time}',end=' ')
        print(f'{stf.finished[i].response_time} {stf.finished[i].turnaround_time}',end=' ')
        print(f'{stcf.finished[i].response_time} {stcf.finished[i].turnaround_time}',end=' ')
        print(' '.join(f'{rr.finished[e][i].response_time} {rr.finished[e][i].turnaround_time}'
                        for e in range(len(E))))
    

def pprint_policies(fifo, stf, stcf, rr):
    print('\n----------Policies---------\n')
    print('    |rt_m | ta_m')
    print('----------------')
    print(fifo)
    print('----------------')
    print(stf)
    print('----------------')
    print(stcf)
    print('----------------')
    print(rr,'\n')

def print_policies(fifo, stf, stcf, rr):
    print('%.2f %.2f %.2f' % (fifo.ta_m, fifo.rt_m,fifo.total_time))
    print('%.2f %.2f %.2f' % (stf.ta_m, stf.rt_m, stf.total_time))
    print('%.2f %.2f %.2f' % (stcf.ta_m, stcf.rt_m, stcf.total_time))
    for i in range(len(rr.E)):
        print('%.2f %.2f %.2f' % (rr.ta_m[i], rr.rt_m[i], rr.total_time[i]))


if __name__ == "__main__":
    jobs, N, Q, E = parser_input()
    jobs_STF      = [e.clone() for e in jobs]
    jobs_STCF     = [e.clone() for e in jobs]
    jobs_RR       = [e.clone() for e in jobs]
    
    fifo = FCFS(jobs, None, Q).start()
    stf  = STF(jobs_STF, None, Q).start()
    stcf = STCF(jobs_STCF, None, Q).start()
    rr   = RR(jobs_RR, E, Q).start()


    print_jobs(fifo,stf,stcf,rr)
    print()
    print_policies(fifo,stf,stcf,rr)
    