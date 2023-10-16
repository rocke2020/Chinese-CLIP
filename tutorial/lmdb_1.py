from pathlib import Path
import pandas as pd
import numpy as np
from pandas import DataFrame
import os, sys, shutil, logging, json
import re, random, math
from icecream import ic
ic.configureOutput(includeContext=True, argToStringFunction=lambda _: str(_))
ic.lineWrapWidth = 120
sys.path.append(os.path.abspath('.'))
from collections import defaultdict
from utils.log_util import logger
from utils.file_util import FileUtil
from tqdm import tqdm
import lmdb
import base64


SEED = 0
random.seed(SEED)
np.random.seed(SEED)


examples_dir = Path("examples")
lmdb_img = os.path.join(examples_dir, "imgs")


def write():
    """  """
    env_img = lmdb.open(lmdb_img, map_size=1024**4)
    txn_img = env_img.begin(write=True)    
    write_idx = 0
    for txt_file in examples_dir.glob("*.txt"):
        b64 = FileUtil.read_text(txt_file)[0]
        txn_img.put(key="{}".format(write_idx).encode('utf-8'), value=b64.encode("utf-8"))
        txn_img.commit()
        txn_img = env_img.begin(write=True)
    txn_img.put(key=b'num_images',
            value="{}".format(write_idx).encode('utf-8'))
    txn_img.commit()
    env_img.close()


def read(img_idx=0):
    """ TODO error write  """
    env_img = lmdb.open(lmdb_img, map_size=1024**4)
    b64 = search(env_img, img_idx)
    b = base64.b64decode(b64.decode("utf-8"))
    out_file = examples_dir / f"pokemon.{img_idx}.png"
    with open(out_file, "wb") as f:
        f.write(b)
    env_img.close()

def search(env, sid):
    txn = env.begin()
    name = txn.get(str(sid).encode('utf-8'))
    return name


def initialize():
    env = lmdb.open("students")
    return env


def insert(env, sid, name):
    txn = env.begin(write = True)
    txn.put(str(sid), name)
    txn.commit()


def delete(env, sid):
    txn = env.begin(write = True)
    txn.delete(str(sid))
    txn.commit()


def update(env, sid, name):
    txn = env.begin(write = True)
    txn.put(str(sid), name)
    txn.commit()


def display(env):
    txn = env.begin()
    cur = txn.cursor()
    for key, value in cur:
        print (key, value)


def demo():
    """  """
    pass
    env = initialize()
    print("Insert 3 records.")
    insert(env, 1, "Alice")
    insert(env, 2, "Bob")
    insert(env, 3, "Peter")
    display(env)

    print("Delete the record where sid = 1.")
    delete(env, 1)
    display(env)

    print("Update the record where sid = 3.")
    update(env, 3, "Mark")
    display(env)

    print("Get the name of student whose sid = 3.")
    name = search(env, 3)
    print(name)

    env.close()
    os.system("rm -r students")


# write()
read()