import sys
import os
import json
import calculate_scores


def main():
    explorepath = sys.argv[1]
    outputfile = sys.argv[2]
    permodel = open("per_model.txt", "r", encoding="latin1")
    permodelcontent = permodel.read().splitlines()
    bias = float(permodelcontent[0])
    tokendict = json.loads(permodelcontent[1])
    f = open(outputfile, "a", encoding="latin1")
    f.truncate(0)
    for root, dirs, files in os.walk(explorepath):
        for filename in files:
            if filename.endswith(".txt"):
                filepath = os.path.abspath(os.path.join(root, filename))
                inputfile = open(filepath, "r", encoding="latin1")
                filecontent = inputfile.read().splitlines()
                alpha = 0
                for line in filecontent:
                    tokens = line.split(' ')
                    for individualtoken in tokens:
                        if individualtoken in tokendict.keys():
                            alpha += tokendict.get(individualtoken)
                alpha += bias
                if alpha > 0:
                    f.write('spam ')
                    f.write(filepath)
                    f.write('\n')
                else:
                    f.write('ham ')
                    f.write(filepath)
                    f.write('\n')
    f.close()
    calculate_scores.calculate(outputfile, 0)

if __name__ == '__main__':
    main()
