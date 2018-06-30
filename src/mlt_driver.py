import sys
import csv
from datetime import datetime
import logging
import multiprocessing as mp
import time

from loaders import load_set,load_embds,load_dicts
from processors import process_playlist
from writers import output_submission,output_extra
from evaluators import get_perf_stats

l = mp.Lock()
manager = mp.Manager()
recs_list = manager.list()
perf_stats_list = manager.list()
pl_list = manager.list()    

if len(sys.argv) != 8:
    print("Usage:")
    print("    python driver.py set_info start end gap NUM_NEIGHBORS POP_THRESHOLD stats_only")
    print("    set_info: chlg | test1 | ... Specify the set to load.")
    print("    start end gap: e.g. 0 1000 50. Starting and ending index.")
    print("    NUM_NEIGHBORS, POP_THRESHOLD: e.g. 1000 30. Parameters for recs.")
    print("    stats_only: T | F. Only output one file with stats.")
    exit()

set_info = sys.argv[1]
if set_info == "chlg":
    set_type = "chlg"
    set_index = ''
elif set_info[:-1] == "test":
    set_type = "test"
    set_index = int(set_info[-1])
else:
    print("Error: Wrong set_info.")

start = int(sys.argv[2])
end = int(sys.argv[3])
tot = end - start
gap = int(sys.argv[4])
NUM_NEIGHBORS = int(sys.argv[5])
POP_THRESHOLD = int(sys.argv[6])
for_test_set = (set_type == "test")
if sys.argv[7] == 'T': stats_only = True
else: stats_only = False

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='logs/{0}.log'.format(set_info))

loaded_set = load_set("sets/",set_type,set_index)
embds,a2embd_id,embd_id2a = load_embds("embds/")
a2t,u2t,t2a,u2a,title2t = load_dicts("dicts/")
playlists = loaded_set["playlists"]
playlists = playlists[start:end]


def driver():
    with open("results/submission.csv",'w') as submission:
        sub_wrtr = csv.writer(submission,delimiter=';')
        sub_wrtr.writerow(["team_info,4027,main,jianzhiliu@g.ucla.edu"])
    # process, (evaluate,) write
    nthreads = 32
    logging.info("Start Multiprocessing {0}".format(nthreads))
    start_time = time.time()
    pool = mp.Pool(nthreads)
    if for_test_set:
        pool.map(job_test, playlists)
        write_test()
    else:
        pool.map(job, playlists)
        write()


def job(pl):
    logging.debug("Start new job.")
    recs = process_playlist(pl,a2t,t2a,title2t,embds,embd_id2a,a2embd_id,
                            NUM_NEIGHBORS,POP_THRESHOLD)
    l.acquire()
    pl_list.append(pl)
    recs_list.append(recs)
    l.release()
    
def write():
    logging.info("Start writing.")
    for pl,recs in zip(pl_list, recs_list):
        output_submission("results/",pl,recs,Warn=True)


def job_test(pl):
    logging.debug("Start new job.")
    recs = process_playlist(pl,a2t,t2a,title2t,embds,embd_id2a,a2embd_id,
                            NUM_NEIGHBORS,POP_THRESHOLD)  
    perf_stats = get_perf_stats(pl,recs,t2a)
    ###store the value
    l.acquire()
    pl_list.append(pl)
    recs_list.append(recs)
    perf_stats_list.append(perf_stats)
    l.release()

def write_test():
    logging.info("Start writing.")
    for pl,recs,perf_stats in zip(pl_list, recs_list,perf_stats_list):
        output_extra("results/",pl,recs,t2a,u2t,u2a,perf_stats,
                     for_test_set,stats_only)


if __name__ == '__main__':
    driver()
