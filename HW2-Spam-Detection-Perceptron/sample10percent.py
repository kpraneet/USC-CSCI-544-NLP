import sys
import os
import random
import pickle


def main():
    spamlist = []
    hamlist = []
    explorepath = sys.argv[1]
    for root, dirs, files in os.walk(explorepath):
        for filename in files:
            if filename.endswith(".txt"):
                currentdirectory = os.path.dirname(os.path.abspath(os.path.join(root, filename)))
                previousdirectory = currentdirectory.split('/')
                if previousdirectory[-1] == 'spam' or filename.endswith("spam.txt"):
                    spamlist.append(filename)
                elif previousdirectory[-1] == 'ham' or filename.endswith("ham.txt"):
                    hamlist.append(filename)
    tenpercentspam = random.sample(spamlist, 750)
    tenpercentham = random.sample(hamlist, 955)
    filelist = tenpercentspam + tenpercentham
    with open("10percentsample.txt", "wb") as f:
        pickle.dump(filelist, f)

if __name__ == '__main__':
    main()
