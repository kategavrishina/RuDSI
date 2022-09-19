## Target words:

1. The total number of senses was extracted for each word in three distinct resources:
- [Russian National Corpus (RNC)](https://ruscorpora.ru); in particular, the RNC semantic markup which includes parts of speech and semantic classes for a large number of lexemes;
- [Wiktionary](http://www.wiktionary.org), web-based free dictionary;
- and RuWordNet [1], a thesaurus of the Russian language created in the format of English WordNet.
2. All non-noun words were discarded from this set.
3. Eight most frequent words (according to the dictionary by Lyshevskaya, Sharov [2]) were selected in each of three groups: words with one sense, words with 2-4 senses, words with five or more senses.
4. The final number of senses was calculated as the average between RNC, Wiktionary and RuWordNet for each target word.


## Scripts

Package installation:
`pip install -r requirements.txt`

1. Extracting target words
   
   CMD command: `python get_target_words.py [the RNC semantic markup] --one [number of words with one sense] --few [number of words with 2-4 senses] --many [number of words with five or more senses]`
   
   Example: `python get_target_words.py semantic.csv.gz --one 8 --few 8 --many 8`

2. Extracting sentences with target words from RNC
   
   CMD command: `python get_sentences.py [path to the list of target words] [path to the corpus] [path to the final directory] [prefix for files]`
   
   Example: `python get_sentences.py target_words.tsv corpus.csv.gz word_examples example`
   
3. Converting to DUREL format
   
   CMD command: `python json2durel.py [path to the directory with json files] [grouping id] [path to the final directory with durel files]`
   
   Example: `python json2durel.py word_examples 22 durel_files`
   
4. Sentence sampling for the project
   
   CMD command: `python durel_sample.py [path to the directory with durel files] [number of sentences per word] [path to the final directory]`
   
   Example: `python durel_sample.py durel_files 35 durel_sample`


[1] Loukachevitch N. V., Lashevich G., Gerasimova A. A., Ivanov V. V., Dobrov B. V. Creating Russian WordNet by Conversion // In Proceedings of Conference on Computatilnal linguistics and Intellectual technologies Dialog-2016, 2016. pp.405-415

[2] Lyashevskaya O., Sharov S. The frequency dictionary of modern Russian language //Azbukovnik, Moscow. – 2009.
