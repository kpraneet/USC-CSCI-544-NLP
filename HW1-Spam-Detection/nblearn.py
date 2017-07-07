import sys
import os
import json


def main():
    filecount = 0
    spamfilecount = 0
    hamfilecount = 0
    spam = {}
    ham = {}
    spamtokencount = 0
    hamtokencount = 0
    spamprobability = {}
    spamsmoothingprobability = {}
    hamprobability = {}
    hamsmoothingprobability = {}
    temp = 0
    tempvar = 0
    spamcount = 0
    hamcount = 0
    probabilityspam = 0.0
    probabilityham = 0.0
    explorepath = sys.argv[1]
    # print(explorepath)
    # if os.path.exists(explorepath):
    #     print('Path exists')
    # else:
    #     print('Path does not exist')
    for root, dirs, files in os.walk(explorepath):
        for filename in files:
            currentdirectory = os.path.dirname(os.path.abspath(os.path.join(root, filename)))
            previousdirectory = currentdirectory.split('/')
            # print(previousdirectory[-1])
            if previousdirectory[-1] == 'spam' or filename.endswith("spam.txt"):
                filepath = os.path.abspath(os.path.join(root, filename))
                # print(filepath)
                # print(filename)
                filecount += 1
                spamfilecount += 1
                inputfile = open(filepath, "r", encoding="latin1")
                filecontent = inputfile.read().splitlines()
                # print(filecontent)
                for line in filecontent:
                    tokens = line.split(' ')
                    # print(tokens)
                    for individualtoken in tokens:
                        if individualtoken in spam.keys():
                            keyvalue = spam.get(individualtoken)
                            keyvalue += 1
                            spam[individualtoken] = keyvalue
                        else:
                            spam[individualtoken] = 1
                            spamtokencount += 1
            elif previousdirectory[-1] == 'ham' or filename.endswith("ham.txt"):
                filepath = os.path.abspath(os.path.join(root, filename))
                # print(filepath)
                # print(filename)
                filecount += 1
                hamfilecount += 1
                inputfile = open(filepath, "r", encoding="latin1")
                filecontent = inputfile.read().splitlines()
                # print(filecontent)
                for line in filecontent:
                    tokens = line.split(' ')
                    # print(tokens)
                    for individualtoken in tokens:
                        if individualtoken in ham.keys():
                            keyvalue = ham.get(individualtoken)
                            keyvalue += 1
                            ham[individualtoken] = keyvalue
                        else:
                            ham[individualtoken] = 1
                            hamtokencount += 1
            else:
                filecount += 0
                # print('Unknown file')
    for spamkey in spam.keys():
        if spamkey not in ham.keys():
            ham[spamkey] = 0
    for hamkey in ham.keys():
        if hamkey not in spam.keys():
            spam[hamkey] = 0
    for keys in spam.keys():
        temp += 1
        spamcount += spam.get(keys)
    for keys in ham.keys():
        tempvar += 1
        hamcount += ham.get(keys)
    # if temp != tempvar:
    #     print('Spam and Ham count are different')
    # else:
    #     print('Spam and Ham count are same')
    totaluniquecount = temp
    for key in spam.keys():
        spamprobability[key] = float(spam.get(key) / spamcount)
    for key in ham.keys():
        hamprobability[key] = float(ham.get(key) / hamcount)
    for key in spam.keys():
        spamsmoothingprobability[key] = float((spam.get(key) + 1) / (spamcount + totaluniquecount))
    for key in ham.keys():
        hamsmoothingprobability[key] = float((ham.get(key) + 1) / (hamcount + totaluniquecount))
    probabilityspam = float(spamfilecount / filecount)
    probabilityham = float(hamfilecount / filecount)
    f = open("nbmodel.txt", "a")
    f.truncate(0)
    f.write(str(probabilityspam))
    f.write('\n')
    f.write(str(probabilityham))
    f.write('\n')
    json.dump(spamprobability, f)
    f.write('\n')
    json.dump(spamsmoothingprobability, f)
    f.write('\n')
    json.dump(hamprobability, f)
    f.write('\n')
    json.dump(hamsmoothingprobability, f)
    f.write('\n')
    f.close()
    # print(spam)
    # print(ham)
    # print(filecount)
    # print(spamfilecount)
    # print(hamfilecount)
    # print(spamcount)
    # print(hamcount)
    # print(totaluniquecount)
    # print(spamprobability)
    # print(spamsmoothingprobability)
    # print(hamprobability)
    # print(hamsmoothingprobability)
    # print(probabilityspam)
    # print(probabilityham)

if __name__ == '__main__':
    main()
