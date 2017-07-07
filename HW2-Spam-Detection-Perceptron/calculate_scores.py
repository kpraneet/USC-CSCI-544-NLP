def calculate(arg1, arg2):
    outputfilecalculate = arg1
    runflag = arg2
    phamnr = 0
    pspamnr = 0
    phamdr = 0
    pspamdr = 0
    rhamdr = 0
    rspamdr = 0
    if runflag == 0:
        print('Will not execute Calculate-scores.')
    else:
        outputfile = open(outputfilecalculate, "r", encoding="latin1")
        outputfilecontent = outputfile.read().splitlines()
        for line in outputfilecontent:
            splitcontent = line.split(' ')
            classification = splitcontent[0]
            filetype = splitcontent[1].split('.')[-2]
            if classification == 'ham' and filetype == 'ham':
                phamnr += 1
            if classification == 'spam' and filetype == 'spam':
                pspamnr += 1
            if classification == 'ham':
                phamdr += 1
            if classification == 'spam':
                pspamdr += 1
            if filetype == 'ham':
                rhamdr += 1
            if filetype == 'spam':
                rspamdr += 1
        print('Precision counts: ')
        print(phamnr, pspamnr, phamdr, pspamdr)
        print('Recall counts: ')
        print(phamnr, pspamnr, rhamdr, rspamdr)
        precisionham = phamnr / phamdr
        precisionspam = pspamnr / pspamdr
        print('Precision ham: ', precisionham)
        print('Precision spam: ', precisionspam)
        recallham = phamnr / rhamdr
        recallspam = pspamnr / rspamdr
        print('Recall ham: ', recallham)
        print('Recall spam: ', recallspam)
        fscoreham = (2 * precisionham * recallham) / (precisionham + recallham)
        fscorespam = (2 * precisionspam * recallspam) / (precisionspam + recallspam)
        print('F-score ham: ', fscoreham)
        print('F-score spam: ', fscorespam)
