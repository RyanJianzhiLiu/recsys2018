import json
import pickle as pkl
import numpy as np
import logging
logger = logging.getLogger(__name__)

### load challenge set or test set
def load_set(path,type,index=1):
    if type == "chlg":
        filepath = path + "challenge_set.json"
    elif type == "test":
        filepath = path + "test_set_{0}.json".format(index)
    else:
        print("Invalid set type.")
        return None
    with open(filepath) as json_file:
        js = json_file.read()
        set = json.loads(js)
    logger.info("Set Loaded ({0}{1}).".format(type,index))
    return set

### Load embeddings and two complementary dictionaries
def load_embds(path):
    # load embeddings
    # total number of artists: 295860
    embd_file_path = path + "artist_uri_embds"
    embds = {}; # key: embd_id, value: embd in np.array
    with open(embd_file_path,'r') as f:
        embds_txt = f.readlines()
    for embd_str in embds_txt:
        vec = []
        for num_str in embd_str[5:-2].split(','):
            vec.append(float(num_str))
        embds[vec[0]] = np.array(vec[1:])
    # load complementary dicts
    a2embd_id_path = path + "a2embd_id.pkl"
    embd_id2a_path = path + "embd_id2a.pkl"
    with open(a2embd_id_path) as f: a2embd_id = pkl.load(f)
    with open(embd_id2a_path) as f: embd_id2a = pkl.load(f)
    logger.info("Embeddings loaded.")
    return (embds, a2embd_id, embd_id2a)

### Load dictionaries
def load_dicts(dicts_path):
    a2t_path = dicts_path + "a2t_occ.json"
    u2t_path = dicts_path + "u2t.json"
    t2a_path = dicts_path + "t2a.json"
    u2a_path = dicts_path + "u2a.json"
    title2t_path = dicts_path + "title2t.json"
    logger.debug("Start Loading Dicts:")
    with open(a2t_path) as f: js = f.read(); a2t = json.loads(js)
    logger.debug("    1/5 Dicts Loaded.")
    with open(u2t_path) as f: js = f.read(); u2t = json.loads(js)
    logger.debug("    2/5 Dicts Loaded.")
    with open(t2a_path) as f: js = f.read(); t2a = json.loads(js)
    logger.debug("    3/5 Dicts Loaded.")
    with open(u2a_path) as f: js = f.read(); u2a = json.loads(js)
    logger.debug("    4/5 Dicts Loaded.")
    with open(title2t_path) as f: js = f.read(); title2t = json.loads(js)
    logger.debug("    5/5 Dicts Loaded.")
    logger.info("Dicts loaded.")
    return (a2t,u2t,t2a,u2a,title2t)
