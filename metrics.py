#!/usr/bin/python
''' Author: thalesfc@gmail.com - Thales Filizola Costa'''
import argparse
import math
import operator
from collections import defaultdict

parser = argparse.ArgumentParser(description="# Metrics")
parser.add_argument("path_papers", help="Path to papers file.")
parser.add_argument("path_classes", help="Path to classes file.")
parser.add_argument("metric", help="The given metric (MI, DICE, CHI2 or KLD).")


# loading terms
def load_terms(path, papers_classes):
    print "# Loading articles @", path
    Ei = defaultdict(int)
    Eci = defaultdict(lambda: defaultdict(int))
    with open(path) as f:
        count = 0
        for line in f:
            paper_set = set()

            for token in line.strip().split():
                term = unicode(token, 'utf-8')
                paper_set.add(term)

            # iterate in all terms that happens in that paper
            for term in paper_set:
                #setting Ei (frequency of term i in the base)
                Ei[term] += 1

                #iterate over all classes for this item
                for classe in papers_classes[count]:
                    Eci[classe][term] += 1

            count += 1
    E = count
    return E, Ei, Eci


def load_classes(path):
    print "# Loading classes @", path
    f = open(path)
    cset = set()
    papers_classes = []
    Ec = defaultdict(int)

    for line in f:
        pc = set()
        for classe in line.split(','):
            classe = classe.strip()
            cset.add(classe)
            pc.add(classe)
            for c in pc:
                Ec[c] += 1
        papers_classes.append(pc)
    return cset, papers_classes, Ec


def MI_function(E, Ei, Ec, Eci):
    '''
        E -> # of items
        Ei -> term freq
        Ec -> the frequency of the given class
        Eci -> term freq on class
    '''
    up = float(Eci)
    down = float(Ei) * float(Ec)
    return math.log(up / down)


def get_metric_func(name):
    print "# Score func:", name
    if name == 'MI':
        return MI_function
    # TODO include others


def get_classes_scores(fx, E, Ei, Ec, Eci):
    ''' function to calculate the score of all terms for all classes
        Ec -> {classe : class_freq}
    '''
    f = open('data/scores.dat', 'w')

    # TODO save scores for future work?
    # classe -> item -> metric_score
    #scores = defaultdict(lambda: defaultdict(float))
    #scores[classe][item] = fx(E, item_freq, class_freq, class_item_freq)
    #sorted_class = sorted(scores[classe].iteritems(), key=operator.itemgetter(1), reverse=True)
    # END

    count = 0

    # iterating through all classes and its freq
    for classe, class_freq in Ec.items():
        class_scores = defaultdict(int)
        print >> f, "{} ||".format(classe),
        count += 1
        print count
        for item, item_freq in Ei.items():
            class_item_freq = Eci[classe][item]

            # if the fiven term happened in the given classe
            if class_item_freq > 0:
                class_scores[item] = fx(E, item_freq, class_freq, class_item_freq)

        # compute the top words
        sorted_class = sorted(class_scores.iteritems(), key=operator.itemgetter(1), reverse=True)
        for i in xrange(20):
            classe, score = sorted_class[i]
            print >> f, "{}::{}".format(classe, score),

        f.write("\n")
        f.flush()


def main():
    args = parser.parse_args()
    print "# Args {}".format(args)

    # returns: cset = set of all classes
    # pcs: for all papers -> set of classes
    # pcs -> [set(), set() ... ]
    # Ec = TFc, i.e., the frequency of class c in the base
    cset, pcs, Ec = load_classes(args.path_classes)
    print "# number of classes: {}".format(len(cset))

    # E = number of articles
    # Ei = TFi, i.e., the frequency of term i in the base
    E, Ei, Eci = load_terms(args.path_papers, pcs)
    print "# E:{}".format(E)

    # switch between the metric functions
    score_func = get_metric_func(args.metric)

    # computes the score of all terms for classes
    get_classes_scores(score_func, E, Ei, Ec, Eci)


if __name__ == "__main__":
    print 10 * " #"
    i = main()
