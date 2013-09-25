#!/usr/bin/python
import argparse
import numpy
import math
from collections import defaultdict

parser = argparse.ArgumentParser(description="# Statistical Test")
parser.add_argument("path", help="path to test-results files")
parser.add_argument("n", type=int, help="number of folds")
parser.add_argument("algo1", help="algorithm 1")
parser.add_argument("-a", "--algo2", help="algorithm 2")

MAX_POS = 1002

def load_data(path, name, fold):
    print "# Loading", path, name
    print "\n", 35 * "=", "\n"
    data = numpy.zeros((fold, MAX_POS), dtype=numpy.float)
    Qdata = numpy.zeros(fold, dtype=numpy.int)
    for i in xrange(fold):
        f = open(path + '/fold_' + str(i) + "-" + name)
        temp = f.readline()
        Q = int(temp.strip().split()[1])
        Qdata[i] = Q
        #print "# fold: ", i, "- Q:", Q
        for line in f:
            line = line.strip()
            spos, snum_hits = line.split()
            rank_i = int(spos)
            n_hits = int(snum_hits)
            data[i, rank_i] = n_hits
    return Qdata, data


def calculate_mrr(Qdata, data1, fold):
    data = numpy.zeros((fold), dtype=numpy.float)
    for i in xrange(fold):
        Q = Qdata[i]
        print "# fold: ", i, "- Q:", Q
        acc = 0.0
        for pos in xrange(MAX_POS):
            rank_i = pos
            n_hits = data1[i, pos]

            ## accumulating MRR
            ## we have all hit for the ith position
            ## so we perform 1/ranki * n_hits
            acc += (float(n_hits) / float(rank_i + 1))
            #print "acc", acc, " - n_hits", n_hits, " - rank_i", rank_i

        MRR = acc / Q
        print "MRR: ", MRR, " - acc: ", acc, " - Q: ", Q
        data[i] = MRR
        print "\n", 35 * "=", "\n"
    return data


def mmr(path, name, fold):
    print "# Loading", path, name
    print "\n", 35 * "=", "\n"
    data = numpy.zeros((fold), dtype=numpy.float)
    for i in xrange(fold):
        f = open(path + '/fold_' + str(i) + "-" + name)
        temp = f.readline()
        Q = int(temp.strip().split()[1])
        print "# fold: ", i, "- Q:", Q
        count = 0
        acc = 0.0
        for line in f:
            count += 1
            line = line.strip()
            spos, snum_hits = line.split()
            rank_i = int(spos)
            n_hits = int(snum_hits)

            ## accumulating MRR
            ## we have all hit for the ith position
            ## so we perform 1/ranki * n_hits
            acc += (float(n_hits) / float(rank_i + 1))
            #print "acc", acc, " - n_hits", n_hits, " - rank_i", rank_i

        MRR = acc / Q
        print "MRR: ", MRR, " - acc: ", acc, " - Q: ", Q
        data[i] = MRR
        print "\n", 35 * "=", "\n"
    return data


def get_t(x, y):
    dic = defaultdict(dict)
    dic[95][4] = 2.776
    dic[90][4] = 2.132

    dic[95][9] = 2.262
    dic[90][9] = 1.833

    return dic[x][y - 1]


CONFIDENCE = 95


def test_t(data, n_folds):
    print 35 * "-"
    print "test t"
    x = numpy.mean(data)
    t = get_t(CONFIDENCE, n_folds)
    stddev = numpy.std(data, dtype=numpy.float64)
    print  "t: ", t
    print "std: ", stddev
    t_dist = stddev * t / math.sqrt(n_folds)
    print 35 * "-"
    return x, t_dist


def main():
    print "# Mean Reciprocal rank"
    args = parser.parse_args()
    print "# Args {}".format(args)
    Qdata1, data1 = load_data(args.path, args.algo1, args.n)
    data_mrr = calculate_mrr(Qdata1, data1, args.n)
    #data_mrr = mmr(args.path, args.algo1, args.n)
    if args.algo2:
        _, data2 = load_data(args.path, args.algo2, args.n)
        d2 = calculate_mrr(Qdata1, data2, args.n)
        print "MRR x fold: ", data_mrr
        print "MRR x fold: ", d2
        data_mrr -= d2
    print "MRR x fold: ", data_mrr
    MRR, error = test_t(data_mrr, args.n)
    print ">>> MRR: ", MRR, "+-", error
    print
    print '&{0:.4f} $\\pm$'.format(MRR),
    print '{0:.4f}'.format(error)
    print
    #print MRR, error

if __name__ == "__main__":
    main()
