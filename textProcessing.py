''' Author: thalesfc@gmail.com '''
from unidecode import unidecode
import string
from nltk import stem, corpus


def test_4_class(inp, outp, classes):
    fc = open(classes)
    fi = open(inp)
    fo = open(outp, 'w')
    count = 0
    for line in fc:
        inp_line = fi.readline()
        count += 1
        if len(line) == 1:
            print "Line", count, "removed."
        else:
            fo.write(inp_line)


def remove_1tab(f, out):
    for line in f:
        tokens = line.split('\t')
        out.write(tokens[1])
    print "# printing done"
    out.close()


def remove_authors(inp, outp):
    ''' Remove comment authors' name '''
    print "# removing comments"
    for c, l in enumerate(inp):
#       print '# ', c+1
        sline = l.strip()
        tokens = sline.split('::')
        for token in tokens:
            if len(token.split()) < 6:
#               print token
                pass
            else:
                outp.write(token)
        outp.write('\n')
    outp.close()


def remove_unidecode(inp, outp):
    ''' Remove accent and special characters
    + lower case '''
    print "# remove accents"
    for line in inp:
        uline = unicode(line, 'utf-8')
        udline = unidecode(uline)
        outp.write(udline.lower())
    outp.close()


def remove_punctuation(inp, outp):
    ''' Remove punctuation '''
    print "# removing punctuation ",
    print string.punctuation
    for line in inp:
        nopline = line.translate(None, string.punctuation)
        outp.write(nopline)
    outp.close()


def remove_stopwords(inp, outp):
    ''' remove stop-words '''
    print "# removing stopwords"

    # creating set of stopwords
    list_stopwords = corpus.stopwords.words()
    stopwords = set()
    for sw in list_stopwords:
        usw = unicode(sw, 'utf-8')
        stopwords.add(usw)

    for line in inp:
        sline = line.strip()
        tokens = sline.split()
        outlist = []

        for token in tokens:
            string = unicode(token, 'utf-8')
            if not string in stopwords:
                outlist.append(string)

        outp.write(' '.join(outlist))
        outp.write('\n')
    outp.close()


def lemmatisation(inp, outp):
    ''' Lemmatisation of strings '''
    print "# lemmatisation"
    wnl = stem.WordNetLemmatizer()
    for line in inp:
        sline = line.strip()
        tokens = sline.split()
        lemmas = []
        for token in tokens:
            lemma = wnl.lemmatize(token)
            lemmas.append(lemma)
        outp.write(' '.join(lemmas))
        outp.write('\n')
    outp.close()


def stemmize(inp, outp):
    ''' Stemming : snowball'''
    print "# stemming "
    stemmer = stem.snowball.EnglishStemmer(ignore_stopwords=False)
    for line in inp:
        sline = line.strip()
        tokens = sline.split()
        outlist = []
        for token in tokens:
            sttoken = stemmer.stem(token)
            outlist.append(sttoken)
        outp.write(' '.join(outlist))
        outp.write('\n')
    outp.close()


if __name__ == "__main__":

    inp = 'data/papers.txt'
    path_c = 'data/keywords.txt'
    temp1 = 'data/temp1.txt'
    temp2 = 'data/temp2.txt'
    temp3 = 'data/temp3.txt'
    temp4 = 'data/temp4.txt'
    temp5 = 'data/temp5.txt'
    temp6 = 'data/papers.dat'

    test_4_class(inp, temp1, path_c)
    remove_unidecode(open(temp1, 'r'), open(temp2, 'w'))
    remove_punctuation(open(temp2, 'r'), open(temp3, 'w'))
    remove_stopwords(open(temp3, 'r'), open(temp4, 'w'))
    lemmatisation(open(temp4, 'r'), open(temp5, 'w'))
    stemmize(open(temp5, 'r'), open(temp6, 'w'))
