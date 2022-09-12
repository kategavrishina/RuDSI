import sys
import pandas as pd
import os

dureldir = sys.argv[1]
sent_per_word = sys.argv[2]
resultdir = sys.argv[3]

durel_files = os.listdir(dureldir)

if not os.path.exists(resultdir):
    os.makedirs(resultdir)

for filename in durel_files:
    examples = pd.read_csv(os.path.join(dureldir, filename), sep='\t', header=0, compression='gzip', encoding='utf-8')
    print('In file', filename, len(examples), 'examples found')
    result = examples.sample(int(sent_per_word))
    path = os.path.join(resultdir, filename)
    result.to_csv(path.replace('example', 'sample').split('.gz')[0], sep='\t', line_terminator='\n', index=False)
