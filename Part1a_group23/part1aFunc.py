import json
import os

def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period. We used this since we had problems using the code on mac"""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]
    
"""function that saves everything into a txt,
the seperate function"""
def partb():
    txt = open("EveryTranscript.txt","a+")
    StartingPaths = ["dstc2_traindev/data", "dstc2_test/data"]  # work for both train and test


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
                        txt.write("session id: " + data1['session-id'])
                        txt.write(data2['task-information']['goal']['text'] + "\n")
                        txt.write("\n")
                    txt.write("system: " + data1['turns'][i]['output']['transcript']+"\n")
                    txt.write("user: " + data2['turns'][i]['transcription']+"\n")
                txt.write("\n")
    txt.close()