### build test set
import sys
import os
import json
import random

### randomly pick out one playlist from each slice
def sampling_MPD(path,quick):
    print("Extracting sample from MPD...")
    test_set = {}
    slice_index = 0;
    selected_playlists = [random.randrange(1000) for i in range(1000)]
    test_set["playlists"] = []
    filenames = os.listdir(path)
    for filename in sorted(filenames):
        if filename.startswith("mpd.slice.") and filename.endswith(".json"):
            fullpath = os.sep.join((path, filename))
            f = open(fullpath)
            js = f.read()
            f.close()
            mpd_slice = json.loads(js)
            ls_index = selected_playlists[slice_index]
            playlist = mpd_slice['playlists'][ls_index]
            test_set["playlists"].append(playlist)
            slice_index += 1
            if quick and (slice_index == 30): break
    return test_set

### modify a MPD playlist into a test_set playlist
### split "tracks" into new "tracks" and "answers"
def modify_MPD_playlist(playlist,title_only):
    if title_only:
        playlist["num_samples"] = 0
        playlist["answers"] = playlist.pop("tracks")
        playlist["tracks"] = []
        return
    num_tracks = playlist["num_tracks"]
    if num_tracks < 10:
        num_seeds = 1
    elif num_tracks < 25:
        num_seeds = 5
    elif num_tracks < 50:
        num_seeds = 10
    elif num_tracks < 200:
        num_seeds = 25
    else:
        num_seeds = 100
    playlist["num_samples"] = num_seeds
    selected_tracks = random.sample(range(num_tracks),num_seeds)
    selected_tracks = sorted(selected_tracks, reverse=True)
    playlist["seeds"] = []
    for track_index in selected_tracks:
        seed = playlist["tracks"].pop(track_index)
        playlist["seeds"].append(seed)
    playlist["answers"] = playlist.pop("tracks")
    playlist["tracks"] = playlist.pop("seeds")

def store_test_set(test_set,index,path):
    with open(path+"test_set_{0}.json".format(index), 'w') as outfile:
        json.dump(test_set, outfile)
    print("test_set_{0} stored.".format(index))

def build_test_set(index,MPD_path,storing_path,quick,title_only):
    test_set = sampling_MPD(MPD_path,quick)
    print("Modifying MPD sample...")
    for playlist in test_set["playlists"]:
        modify_MPD_playlist(playlist,title_only)
    store_test_set(test_set,index,storing_path)

def main():
    if len(sys.argv) != 5:
        print("Usage: python build_test_set.py index title-only(T|F) MPD_path storing_path")
        return
    index = sys.argv[1]
    if sys.argv[2] == 'T': title_only = True
    else: title_only = False
    MPD_path = sys.argv[3]
    storing_path = sys.argv[4]
    if index == '0': quick = True
    else: quick = False
    build_test_set(index,MPD_path,storing_path,quick,title_only)


if __name__ == '__main__':
    main()
