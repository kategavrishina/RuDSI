#! /bin/env python3
# coding: utf-8

import sys
import pandas as pd
from smart_open import open
import json
import os
from tqdm import tqdm

targetlistfile = sys.argv[1]
corpusfile = sys.argv[2]
directory = sys.argv[3]
identifier = sys.argv[4]

targets = {}

with open(targetlistfile, "r", encoding='utf-8') as f:
    lines = f.readlines()[1:]

for line in lines:
    word = line.strip().split("\t")[0]
    targets[word.strip() + "_S"] = []

print(f"{len(targets)} target words to extract", file=sys.stderr)

corpus = pd.read_csv(corpusfile, encoding='utf-8', compression='gzip', index_col="ID", keep_default_na=False)

for idx, lemmas, raw in corpus[["LEMMAS", "RAW"]].itertuples():
    text = raw.strip()
    language = None
    split_lemmas = lemmas.split()
    bag_of_lemmas = set([w for w in split_lemmas])
    for target in targets:
        if target in bag_of_lemmas:
            targets[target].append([split_lemmas, text])

if not os.path.exists(directory):
    os.makedirs(directory)

for target in tqdm(targets):
    print(f"{target}: {len(targets[target])} examples found", file=sys.stderr)
    outfilename = f"{identifier}_{target}.json.gz"
    with open(os.path.join(directory, outfilename), "w") as f:
        out = json.dumps(targets[target], ensure_ascii=False, indent=4)
        f.write(out)
