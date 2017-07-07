# Uncomment below commented code for 10 percent sample
import sys
import os
import random
import json
from collections import defaultdict
# import pickle


def main():
    finalset = []
    tokendict = defaultdict(int)
    avgdict = defaultdict(float)
    spamlabely = 1
    hamlabely = -1
    bias = 0
    extfile = 0
    unknownfilecount = 0
    beta = 0.0
    counter = 1
    explorepath = sys.argv[1]

    # filelist = []
    # if os.path.isfile("10percentsample.txt"):
    #     with open("10percentsample.txt", "rb") as f:
    #         filelist = pickle.load(f)

    for root, dirs, files in os.walk(explorepath):
        for filename in files:
            # if filename.endswith(".txt") and filename in filelist:
            # Comment the line below while executing for 10 percent sample
            if filename.endswith(".txt"):
                contentdict = {}
                individualfiledict = {}
                filepath = os.path.abspath(os.path.join(root, filename))
                inputfile = open(filepath, "r", encoding="latin1")
                filecontent = inputfile.read().splitlines()
                for line in filecontent:
                    tokens = line.split(' ')
                    for individualtokens in tokens:
                        tokendict[individualtokens] = 0
                        avgdict[individualtokens] = 0.0
                        if individualtokens in contentdict.keys():
                            keyvalue = contentdict.get(individualtokens)
                            keyvalue += 1
                            contentdict[individualtokens] = keyvalue
                        else:
                            contentdict[individualtokens] = 1
                individualfiledict[filepath] = contentdict
                currentdirectory = os.path.dirname(os.path.abspath(os.path.join(root, filename)))
                previousdirectory = currentdirectory.split('/')
                if previousdirectory[-1] == 'spam' or filename.endswith("spam.txt"):
                    individualfiledict['spam'] = 1
                elif previousdirectory[-1] == 'ham' or filename.endswith("ham.txt"):
                    individualfiledict['ham'] = 1
                else:
                    extfile += 1
                finalset.append(individualfiledict)
    for i in range(0, 30):
        random.shuffle(finalset)
        for line in finalset:
            alpha = 0
            for dictkeys in line.keys():
                if type(line[dictkeys]) == dict:
                    xdictcontent=line[dictkeys]
                    for xvalues in xdictcontent.keys():
                        alpha += (xdictcontent.get(xvalues) * tokendict.get(xvalues))
            alpha += bias
            if "spam" in line.keys():
                if (spamlabely * alpha) <= 0:
                    bias += spamlabely
                    beta += (spamlabely * counter)
                    for dictkeys in line.keys():
                        if type(line[dictkeys]) == dict:
                            xdictcontent = line[dictkeys]
                            for xvalues in xdictcontent.keys():
                                updatedweight = tokendict.get(xvalues)
                                updatedweight += (spamlabely * xdictcontent.get(xvalues))
                                tokendict[xvalues] = updatedweight
                                avgupdatedweight = avgdict.get(xvalues)
                                avgupdatedweight += (spamlabely * xdictcontent.get(xvalues) * counter)
                                avgdict[xvalues] = avgupdatedweight
            elif "ham" in line.keys():
                if (hamlabely * alpha) <= 0:
                    bias += hamlabely
                    beta += (hamlabely * counter)
                    for dictkeys in line.keys():
                        if type(line[dictkeys]) == dict:
                            xdictcontent = line[dictkeys]
                            for xvalues in xdictcontent.keys():
                                updatedweight = tokendict.get(xvalues)
                                updatedweight += (hamlabely * xdictcontent.get(xvalues))
                                tokendict[xvalues] = updatedweight
                                avgupdatedweight = avgdict.get(xvalues)
                                avgupdatedweight += (hamlabely * xdictcontent.get(xvalues) * counter)
                                avgdict[xvalues] = avgupdatedweight
            else:
                unknownfilecount += 1
            counter += 1
    tempvar = bias - (beta / counter)
    beta = tempvar
    for avgweights in avgdict.keys():
        uweight = avgdict.get(avgweights)
        wweight = tokendict.get(avgweights)
        weightcounter = wweight - (uweight / counter)
        avgdict[avgweights] = weightcounter
    f = open("per_model.txt", "a", encoding="latin1")
    f.truncate(0)
    f.write(str(beta))
    f.write('\n')
    json.dump(avgdict, f)
    f.close()

if __name__ == '__main__':
    main()
