import numpy as np
from collections import Counter

def clicks(predictions, targets):
    notfound = 51
    for p in predictions[0:500]:
        if p in targets: return predictions.index(p)/10
    return notfound

def r_precision(predictions, targets, t2a):
    ARTIST_MATCH_BONUS = 0.25

    # First, cap the number of predictions
    predictions = predictions[:500]
    target_set = set(targets)
    target_count = len(target_set)

    acount = Counter()
    amax = Counter()
    for track in targets:
        artist = t2a[track]
        if artist:
            amax[artist] = 1

    TP = 0
    for track in set(predictions[:target_count]):
    #for track in set(predictions):
        if track in target_set:
            TP += 1
        else:
            artist = t2a[track]
            if artist and amax[artist] > 0:
                if acount[artist] < amax[artist]:
                    TP += ARTIST_MATCH_BONUS
                    acount[artist] += 1
    rprec = float(TP) / target_count
    return rprec

def get_perf_stats(playlist,rec_uris,t2a):
    answer_uris = [ track['track_uri'] for track in playlist['answers'] ]
    rp = r_precision(rec_uris, answer_uris, t2a)
    clk = clicks(rec_uris, answer_uris)
    return (rp, clk)
### TODO: implement other metrics
