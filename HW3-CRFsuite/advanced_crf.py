import sys
import os
import pycrfsuite
# import re
import hw3_corpus_tool as inputtool


def sent2features(utterance):
    speakerlist = []
    finallist = []
    for featureutterance in utterance:
        tokenlist = []
        poslist = []
        xfilelist = []
        speakerlist.append(featureutterance.speaker)
        if len(speakerlist) > 1 and speakerlist[-2] == speakerlist[len(speakerlist)-1]:
            # print('Same')
            speaker = 'Same'
        else:
            # print('Different')
            speaker = 'Different'
        if len(speakerlist) == 1:
            # print('First')
            first = 'New'
        else:
            # print('Not first')
            first = 'Unchanged'
        if not featureutterance.pos:
            tokenlist.append('token_NONE')
            poslist.append('pos_NONE')
            xfilelist.append('speaker_' + speaker)
            xfilelist.append('conversation_' + first)
            # xfilelist.append(featureutterance.speaker)
            for token in tokenlist:
                xfilelist.append(token)
            for pos in poslist:
                xfilelist.append(pos)
            # for x in range(0, len(tokenlist)):
                # xfilelist.append(tokenlist[x])
                # xfilelist.append(poslist[x])
        else:
            for x in featureutterance.pos:
                tokenlist.append('token_' + x.token)
                poslist.append('pos_' + x.pos)
            xfilelist.append('speaker_' + speaker)
            xfilelist.append('conversation_' + first)
            # xfilelist.append(featureutterance.speaker)
            for token in tokenlist:
                xfilelist.append(token)
            for pos in poslist:
                xfilelist.append(pos)
            # for x in range(0, len(tokenlist)):
            #     xfilelist.append(tokenlist[x])
            #     xfilelist.append(poslist[x])
        # textvar = featureutterance.text.lower()
        # var = re.sub('[^a-zA-Z0-9.,?! ]', '', textvar)
        # xfilelist.append(var)
        # xfilelist.append(featureutterance.act_tag)
        # xfilelist.append('bias')
        individualtext = featureutterance.text.lower()
        for var in individualtext.split():
            xfilelist.append('text_' + var)
        finallist.append(xfilelist)
    return finallist


def sent2labels(utterance):
    finallist = []
    for labelutterance in utterance:
        finallist.append(labelutterance.act_tag)
    return finallist


def main():
    inputdir = sys.argv[1]
    testdir = sys.argv[2]
    outputfile = sys.argv[3]
    x_list = []
    y_list = []
    for root, dirs, files in os.walk(inputdir):
        for filename in files:
            if filename.endswith(".csv"):
                filepath = os.path.abspath(os.path.join(root, filename))
                utterances = inputtool.get_utterances_from_filename(filepath)
                x_train = sent2features(utterances)
                y_train = sent2labels(utterances)
                for x in x_train:
                    x_list.append(x)
                for y in y_train:
                    y_list.append(y)
    trainer = pycrfsuite.Trainer(verbose=False)
    trainer.append(x_list, y_list)
    trainer.set_params({
        'c1': 1,
        'c2': 1e-3,
        'max_iterations': 70,
        'feature.possible_states': True,
        'feature.possible_transitions': True
    })
    trainer.train('advanced.crfsuite')
    # print(len(trainer.logparser.iterations), trainer.logparser.iterations[-1])
    tagger = pycrfsuite.Tagger()
    tagger.open('advanced.crfsuite')
    f = open(outputfile, "a")
    f.truncate(0)
    for root, dirs, files in os.walk(testdir):
        for filename in files:
            if filename.endswith(".csv"):
                filepath = os.path.abspath(os.path.join(root, filename))
                utterances = inputtool.get_utterances_from_filename(filepath)
                x_tag = sent2features(utterances)
                outputlist = tagger.tag(x_tag)
                f.write('Filename="')
                f.write(filename)
                f.write('"')
                f.write('\n')
                for y in outputlist:
                    f.write(y)
                    f.write('\n')
                f.write('\n')
    f.close()


if __name__ == '__main__':
    main()
