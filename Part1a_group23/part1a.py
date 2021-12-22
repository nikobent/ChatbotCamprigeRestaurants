import json
import os
import part1aFunc as Func #for partb

"""for creating the document with all transcriptions
delete the #"""
Func.partb()

StartingPaths = ["dstc2_traindev/data","dstc2_test/data"] #work for both train and test

def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period. We used this since we had problems using the code on mac"""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]
    
for p in StartingPaths:
    # discovering the directory of data
    for file in mylistdir(p):
        path1 = os.path.join(p, file)
        """ we discover the directory,
        then for each file we open the 2 json documents
        and print what we need to print
        continue for every file until done"""

        for fl in mylistdir(path1):
            path2 = os.path.join(path1, fl)
            with open(path2 + '/log.json') as f:
                data1 = json.load(f)

            with open(path2 + '/label.json') as f:
                data2 = json.load(f)

            for i in range(0, len(data1['turns'])):
                if i == 0:
                    print("session id: " + data1['session-id'])
                    print(data2['task-information']['goal']['text'])
                    print("\n")
                print("system: " + data1['turns'][i]['output']['transcript'])
                print("user: " + data2['turns'][i]['transcription'])
            print("\n")
            input("Press Enter to continue") 

