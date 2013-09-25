import os
import sys
import logging

############ HEADERS
MODE = 'PAPERS'
#MODE = 'KEYWORDS'

PRINT = 32
##################


logging.basicConfig(filename="stat_base_teste.log", fileMODE="w", level=logging.INFO, format="[ %(asctime)s ] %(levelname)s : %(message)s")

urls = ["http://www.informatik.uni-trier.de/~ley/db/conf/infovis/index.html"]
names = ["IEEE Symposium on Information Visualization (INFOVIS)"]

count = 0
if MODE == 'PAPERS':
        f = open('papers.txt', 'w')
elif MODE == 'KEYWORDS':
        f = open('keywords.txt', 'w')
print >> sys.stderr, "# Priting to:", f.name

for i_url, url in enumerate(urls):
    logging.info("[Conference-Anchor {}] {} ({})".format(i_url, names[i_url], url))
    editions = os.listdir("files/cnf_{}".format(i_url))
    logging.info("[Conference-Anchor {}][# Editions] {} ".format(i_url, len(editions)))
    for i_edition, edition in enumerate(editions):
        logging.info("[Conference {}][Edition-Anchor {}] {}".format(i_url, i_edition, edition))
        papers = open("files/cnf_{}/edition_{}/papers.txt".format(i_url, i_edition))
        logging.info("[Conference {}][Edition {}][# Papers] {}".format(i_url, i_edition, sum(1 for line in open("files/cnf_{}/edition_{}/papers.txt".format(i_url, i_edition)))))
        for i_pap, pap in enumerate(papers):
            if os.path.exists("files/cnf_{}/edition_{}/pdf_{}.txt".format(i_url, i_edition, i_pap)) and os.path.exists("files/cnf_{}/edition_{}/keywords_{}.txt".format(i_url, i_edition, i_pap)):

                if MODE == 'PAPERS':
                    super_file = open("files/cnf_{}/edition_{}/pdf_{}.txt".format(i_url, i_edition, i_pap)).read()
                elif MODE == 'KEYWORDS':
                    super_file = open("files/cnf_{}/edition_{}/keywords_{}.txt".format(i_url, i_edition, i_pap)).read()

                ffile = super_file.replace('\n', ' ')
                print >> f, ffile
                count += 1
                if count == PRINT:
                        print "##############", count
                        print super_file
                #logging.info("[Conference {}][Edition {}][Paper-Anchor {}] {}".format(i_url,i_edition, i_pap, pap.rstrip()))

print >> sys.stderr, "# of pdfs", count
