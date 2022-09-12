#! /bin/env python3
# coding: utf-8

import sys
import csv
from smart_open import open
import json
import os
from nltk.tokenize import wordpunct_tokenize
from leven import levenshtein

jsondir = sys.argv[1]
grouping = sys.argv[2]
dureldir = sys.argv[3]

# Skip usages where the target word ends with a dot
NOABBR = False

json_files = os.listdir(jsondir)

if not os.path.exists(dureldir):
    os.makedirs(dureldir)

for filename in json_files:
    with open(os.path.join(jsondir, filename), 'r', encoding='utf-8') as f:
        usages = json.load(f)

    print(f"{len(usages)} usages total in the JSON file", file=sys.stderr)
    lemma = os.path.basename(filename).split("_")[1]
    pos = "NN"
    date = os.path.basename(filename).split("_")[0].split("-")[0]
    outfile = open(os.path.join(dureldir, filename.replace("json.", "tsv.")), "a", encoding="utf-8")

    outfile.write(
        "lemma\tpos\tdate\tgrouping\tidentifier\tdescription\tcontext\tindexes_target_token\tindexes_target_sentence\n"
    )

    writer = csv.writer(outfile, delimiter="\t", quoting=csv.QUOTE_MINIMAL, dialect="unix")

    seen = set()
    discarded_count = 0
    abbr_count = 0
    too_short_count = 0
    counter = 0

    for sentence in usages:
        description = ""
        context = sentence[1].strip()
        if context in seen:
            discarded_count += 1
            continue
        seen.add(context)
        if NOABBR:
            if f" {lemma}." in context.lower() or context.lower().startswith(f"{lemma}. "):
                abbr_count += 1
                continue
        tokenized_context = wordpunct_tokenize(context)
        if len(context.split()) <= 5:
            too_short_count += 1
            continue
        # First we are looking for the 100% match:
        target_token = None
        for token in tokenized_context:
            if token == lemma:
                target_token = token
        # if no 100% match is found, let's look for similar words:
        if not target_token:
            current_candidate = (None, 100)
            for token in tokenized_context:
                # We are interested only in tokens starting with the same character as lemma
                if token.lower()[0] != lemma.lower()[0]:
                    continue
                distance = levenshtein(token, lemma)
                if distance < current_candidate[1]:
                    current_candidate = (token, distance)
            target_token = current_candidate[0]

        if target_token:
            target = context.find(target_token)
            indexes_target_token = f"{target}:{target + len(target_token)}"
        else:
            indexes_target_token = "0:0"
        indexes_target_sentence = f"0:{len(context)}"
        identifier = f"{grouping}_{lemma}_{counter}"
        writer.writerow(
            [
                lemma,
                pos,
                date,
                grouping,
                identifier,
                description,
                context,
                indexes_target_token,
                indexes_target_sentence,
            ]
        )
        counter += 1

    if discarded_count:
        print(f"{discarded_count} duplicates discarded", file=sys.stderr)

    if abbr_count:
        print(f"{abbr_count} abbreviations discarded", file=sys.stderr)

    if too_short_count:
        print(f"{too_short_count} short sentences discarded", file=sys.stderr)
