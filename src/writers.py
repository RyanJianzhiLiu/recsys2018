import numpy as np
import csv
import logging
logger = logging.getLogger(__name__)

### generate submission.csv
def output_submission(path,playlist,rec_uris,Warn=True):
    pid = playlist['pid']
    num_recs = len(rec_uris)
    if Warn and (num_recs != 500):
        logger.warning("Playlist {0} got {1}/500 recs.".format(pid,num_recs))
    with open(path+"submission.csv",'a') as submission:
        sub_wrtr = csv.writer(submission, delimiter=',')
        sub_wrtr.writerow([pid] + rec_uris)

### generate extra_info.csv with more information
def output_extra(path,playlist,rec_uris,t2a,u2t,u2a,perf_stats,
                 for_test_set=False,stats_only=False):
    with open(path+"perf_stats.csv",'a') as perf:
        perf_wrtr = csv.writer(perf, delimiter=';')
        perf_wrtr.writerow([playlist['pid'],str(perf_stats)])
    if stats_only: return

    pid = playlist['pid']
    try: name = playlist['name']
    except: name = 'N/A'
    num_seeds = playlist['num_samples']
    num_anss = playlist['num_tracks'] - num_seeds
    with open(path+"{0}.csv".format(pid),'w') as extra:
        # Write basic info
        extra_wrtr = csv.writer(extra, delimiter=',')
        extra_wrtr.writerow(["------------------------------"])
        extra_wrtr.writerow([str(pid), name.encode('utf-8')])
        if for_test_set:
            extra_wrtr.writerow(['perf_stats:',str(perf_stats)])
        # Write seeds
        extra_wrtr.writerow(["--------------------"])
        extra_wrtr.writerow(["Seeds: ({0})".format(num_seeds)])
        for track in playlist['tracks']:
            track_name = track['track_name'].encode('utf-8')
            artist_name = track['artist_name'].encode('utf-8')
            extra_wrtr.writerow([track_name, artist_name])
        # Write answers (test_set only)
        if for_test_set:
            extra_wrtr.writerow(["--------------------"])
            extra_wrtr.writerow(["Answers: ({0})".format(num_anss)])
            for track in playlist['answers']:
                track_name = track['track_name'].encode('utf-8')
                artist_name = track['artist_name'].encode('utf-8')
                extra_wrtr.writerow([track_name, artist_name])
        # Write recommendations
        extra_wrtr.writerow(["--------------------"])
        extra_wrtr.writerow(["Recommendations: ({0})".format(len(rec_uris))])
        rec_a_uris = [ t2a[t_uri] for t_uri in rec_uris ]
        for track_uri, artist_uri in zip(rec_uris, rec_a_uris):
            track_name = u2t[track_uri].encode('utf-8')
            artist_name = u2a[artist_uri].encode('utf-8')
            extra_wrtr.writerow([track_name, artist_name])
        extra_wrtr.writerow(["End of playlist {0}".format(pid)])
        extra_wrtr.writerow(["------------------------------"])
