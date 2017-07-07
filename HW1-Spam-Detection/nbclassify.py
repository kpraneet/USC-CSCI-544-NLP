import sys
import os
import json
import math


def main():
    nbmodel = open("nbmodel.txt", "r")
    nbmodelcontent = nbmodel.read().splitlines()
    probabilityspam = float(nbmodelcontent[0])
    probabilityham = float(nbmodelcontent[1])
    spamprobability = json.loads(nbmodelcontent[2])
    spamsmoothingprobability = json.loads(nbmodelcontent[3])
    hamprobability = json.loads(nbmodelcontent[4])
    hamsmoothingprobability = json.loads(nbmodelcontent[5])
    # print(probabilityspam)
    # print(probabilityham)
    # print(spamprobability)
    # print(spamsmoothingprobability)
    # print(hamprobability)
    # print(hamsmoothingprobability)
    explorepath = sys.argv[1]
    # print(explorepath)
    # if os.path.exists(explorepath):
    #     print('Path exists')
    # else:
    #     print('Path does not exist')
    f = open("nboutput.txt", "a")
    f.truncate(0)
    for root, dirs, files in os.walk(explorepath):
        for filename in files:
            spamsmoothingflag = 0
            hamsmoothingflag = 0
            messagespam = 0.0 + probabilityspam
            messageham = 0.0 + probabilityham
            if filename.endswith(".txt"):
                filepath = os.path.abspath(os.path.join(root, filename))
                #print(filepath)
                #print(filename)
                inputfile = open(filepath, "r", encoding="latin1")
                filecontent = inputfile.read().splitlines()
                # print(filecontent)
                for line in filecontent:
                    tokens = line.split(' ')
                    # print(tokens)
                    for individualtoken in tokens:
                        if individualtoken in spamprobability.keys():
                            if spamprobability.get(individualtoken) == 0.0:
                                spamsmoothingflag = 1
                        if individualtoken in hamprobability.keys():
                            if hamprobability.get(individualtoken) == 0.0:
                                hamsmoothingflag = 1
                    for individualtoken in tokens:
                        if individualtoken in spamprobability.keys():
                            if spamsmoothingflag == 0:
                                messagespam += math.log(spamprobability.get(individualtoken))
                            else:
                                messagespam += math.log(spamsmoothingprobability.get(individualtoken))
                        if individualtoken in hamprobability.keys():
                            if hamsmoothingflag == 0:
                                messageham += math.log(hamprobability.get(individualtoken))
                            else:
                                messageham += math.log((hamsmoothingprobability.get(individualtoken)))
                if messageham >= messagespam:
                    f.write('ham ')
                    f.write(filepath)
                    f.write('\n')
                else:
                    f.write('spam ')
                    f.write(filepath)
                    f.write('\n')
    f.close()

if __name__ == '__main__':
    main()
