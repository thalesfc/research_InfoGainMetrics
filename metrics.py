#!/usr/bin/python
''' Author: thalesfc@gmail.com - Thales Filizola Costa'''
import argparse

parser = argparse.ArgumentParser(description="# Metrics")
parser.add_argument("path_papers", help="Path to papers file.")
parser.add_argument("path_keywordss", help="Path to keywords file.")


# loading terms
def load_terms(path):
    print "# Loading articles @", path
    with open(path) as f:
        count = 0
        for line in f:
            paper_set = set()
            count += 1

            for token in line.strip().split():
                term = unicode(token, 'utf-8')
                paper_set.add(term.lower())

            print paper_set
            break
    E = count
    return E


def main():
    args = parser.parse_args()
    print "# Args {}".format(args)

    E = load_terms(args.path_papers)
    print "# E:{}".format(E)

if __name__ == "__main__":
    print 10 * " #"
    main()
