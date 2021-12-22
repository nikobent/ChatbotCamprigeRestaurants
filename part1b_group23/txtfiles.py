import os
import json
import re

def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]


StartingPath = 'data'

txt = open("act.txt","a+")

for file in mylistdir(StartingPath):
    if os.path.isdir(os.path.join(StartingPath, file)):
        path1 = os.path.join(StartingPath, file)
        """ we discover the directory,
        then for each file we open the 2 json documents
        and print what we need to print
        continue for every file until done"""


    with open(path1 + '/label.json') as f:
        data2 = json.load(f)

    for i in range(0, len(data2['turns'])):
        result = re.split(r"\(",data2['turns'][i]['semantics']['cam'])
        txt.write(result[0].lower() +" , "+ data2['turns'][i]['transcription'].lower())
        txt.write("\n")

txt.close()
"""here we are gonna seperate train and test set, 
so we use the same for every case(baselines, machinelearning)"""
data = pd.read_csv('act.txt', header = None)
df = data.sample(frac=1).reset_index(drop=True)
train, test = md.train_test_split(df, train_size = 0.85)


