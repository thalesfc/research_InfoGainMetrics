#!/usr/bin/python
''' Author: thalesfc@gmail.com - Thales Filizola Costa'''
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="# Metrics")
parser.add_argument("path_papers", help="Path to papers file.")
parser.add_argument("path_classes", help="Path to classes file.")


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

    # TODO compute the scores given E, Ei, Ec and Eci

if __name__ == "__main__":
    print 10 * " #"
    main()
