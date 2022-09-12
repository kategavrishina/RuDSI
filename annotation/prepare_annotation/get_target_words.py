import argparse
import re
from ruwordnet import RuWordNet
import pandas as pd
from wiktionaryparser import WiktionaryParser
from smart_open import open
import zipfile

PATH_TO_ZIP = 'Freq2011.zip'

# ANNOT_FILE_PATH = 'semantic.csv.gz'
FREQ_DICT_PATH = 'freqrnc2011.csv'

ONE_SENSE_WORD_NUM = 10
FEW_SENSE_WORD_NUM = 10
MANY_SENSE_WORD_NUM = 10

wn = RuWordNet()
wp = WiktionaryParser()
wp.set_default_language('Russian')

with zipfile.ZipFile(PATH_TO_ZIP, 'r') as zip_ref:
    zip_ref.extractall('.')

def get_lemmas_count_rnc(filepath):
    with open(filepath, mode='rt') as f:
        rows = f.readlines()

    table = []
    for row in rows:
        row = row.strip().split(';')[:11]
        table.append(tuple(row))

    df = pd.DataFrame(table[1:], columns=table[0])
    df = df[df.Cat == 'S']

    grouped_df = df.groupby('Lemma').agg("count")
    grouped_df = grouped_df[['Cat']].sort_values(['Cat'], ascending=False).reset_index()
    grouped_df['Lemma'] = grouped_df['Lemma'].astype(str)
    grouped_df['Lemma'] = grouped_df['Lemma'].apply(lambda x: x.lower())
    lemmas_data = grouped_df[~grouped_df.Lemma.str.contains("[a-z0-9]")].rename({'Cat':'rnc_num_senses'}, axis=1)

    return lemmas_data

def fetch_with_catch_error(x):
    try:
        return len([1 for i in wp.fetch(x)])
    except AttributeError as E:
        print(x, E)

def ruwordnet_wiki_comparison(data):
    
    data['wiktionary_num_senses'] = data['Lemma'].apply(fetch_with_catch_error)
    data['ruwordnet_num_senses'] = data['Lemma'].apply(lambda x: len(wn.get_senses(x)))
    
    return data

def groups(num):
    if num == 1:
        return 1
    elif 2 <= num <= 4:
        return 2
    else:
        return 3

def main():
    parser = argparse.ArgumentParser(description='Arguments for get_target_words script')
    parser.add_argument('dataset', type=str, help='Path to annotated dictionary')
    parser.add_argument('--one', type=int, help='Number of one-sense words')
    parser.add_argument('--few', type=int, help='Number of few-sense words')
    parser.add_argument('--many', type=int, help='Number of many-sense words')
    
    args = parser.parse_args()
    ANNOT_FILE_PATH = args.dataset
    if args.one:
        ONE_SENSE_WORD_NUM = args.one
    if args.few:
        FEW_SENSE_WORD_NUM = args.few
    if args.many:
        MANY_SENSE_WORD_NUM = args.many
    
    freqrnc = pd.read_csv(FREQ_DICT_PATH, sep='\t')
    freqrnc = freqrnc[freqrnc.PoS == 's']

    lemmas = get_lemmas_count_rnc(ANNOT_FILE_PATH)

    freq_and_count = pd.merge(freqrnc, lemmas, on='Lemma', how='inner')

    most_freq_lemmas = freq_and_count.sort_values('Freq(ipm)')[-1000:]

    result = ruwordnet_wiki_comparison(most_freq_lemmas)
    result.reset_index(inplace=True, drop=True)

    result['Mean'] = result[['rnc_num_senses', 'wiktionary_num_senses', 'ruwordnet_num_senses']].mean(axis=1).round().astype('int')

    result = result.drop(['R', 'D', 'Doc'], axis=1).reset_index(drop=True)

    result['Group'] = result.Mean.apply(groups)

    one = result[result.Group == 1]
    few = result[result.Group == 2]
    many = result[result.Group == 3]

    target_words = pd.concat([one[-ONE_SENSE_WORD_NUM:], few[-FEW_SENSE_WORD_NUM:], many[-MANY_SENSE_WORD_NUM:]], ignore_index=True).sort_values(['Freq(ipm)'], ascending=False, ignore_index=True)

    target_words.to_csv('target_words.tsv', sep='\t', index=False)

if __name__ == '__main__':
    main()