import sys
import csv
from datetime import datetime
import logging

from loaders import load_set,load_embds,load_dicts
from processors import process_playlist
from writers import output_submission,output_extra
from evaluators import get_perf_stats

def driver():
    if len(sys.argv) != 8:
        print("Usage:")
        print("    python driver.py set_info start end gap NUM_NEIGHBORS POP_THRESHOLD stats_only")
        print("    set_info: chlg | test1 | ... Specify the set to load.")
        print("    start end gap: e.g. 0 1000 50. Starting and ending index.")
        print("    NUM_NEIGHBORS, POP_THRESHOLD: e.g. 1000 30. Parameters for recs.")
        print("    stats_only: T | F. Only output one file with stats.")
        return
    set_info = sys.argv[1]
    if set_info == "chlg":
        set_type = "chlg"
        set_index = ''
    elif set_info[:-1] == "test":
        set_type = "test"
        set_index = int(set_info[-1])
    else:
        print("Error: Wrong set_info.")
        return
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

    start_time = datetime.now()
    loaded_set = load_set("sets/",set_type,set_index)
    embds,a2embd_id,embd_id2a = load_embds("embds/")
    a2t,u2t,t2a,u2a,title2t = load_dicts("dicts/")
    end_time = datetime.now()
    logging.info('Loading Duration: {}'.format(end_time - start_time))

    with open("results/submission.csv",'w') as submission:
        sub_wrtr = csv.writer(submission,delimiter=';')
        sub_wrtr.writerow(["team_info,4027,main,jianzhiliu@g.ucla.edu"])

    # process, (evaluate,) write
    playlists = loaded_set["playlists"]
    cnt = 0
    start_time = datetime.now()
    for pl in playlists[start:end]:
        recs = process_playlist(pl,a2t,t2a,title2t,embds,embd_id2a,a2embd_id,
                                NUM_NEIGHBORS,POP_THRESHOLD)
        #logging.debug('number of recs for {0}: {1}'.format(pl['pid'],len(recs)))
        if for_test_set:
            perf_stats = get_perf_stats(pl,recs,t2a)
            output_extra("results/",pl,recs,t2a,u2t,u2a,perf_stats,
                         for_test_set,stats_only)
            #output_submission("../results/",pl,recs,Warn=True)
        else: #for_chlg_set
            #output_extra("../results/",pl,recs,t2a,u2t,u2a,for_test_set,stats_only)
            output_submission("results/",pl,recs,Warn=True)
        cnt += 1
        if (cnt%gap == 0):
            end_time = datetime.now()
            logging.info("{0}/{1} playlists finished. Duration: {2}".format(cnt,tot,end_time-start_time))
            start_time = datetime.now()

    logging.info("Exit program.\n\n")

if __name__ == '__main__':
    driver()
