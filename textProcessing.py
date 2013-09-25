from unidecode import unidecode
import string
from nltk import stem, corpus

def check_file(f):
	count = 0
	for line in f:
		count += 1
		tokens = line.split('\t')
		if len(tokens) != 2:
			print count, len(tokens)
	print "# checking done"

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
#		print '# ', c+1
		sline = l.strip()
		tokens = sline.split('::')
		for token in tokens:
			if len(token.split()) < 6:
#				print token
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
	path1 = '/Users/thalesfc/Downloads/description.csv'
	path2 = '/Users/thalesfc/Downloads/description_notab.csv'
	path3 = '/Users/thalesfc/Downloads/description_nocoment.csv'
	path4 = '/Users/thalesfc/Downloads/description_unidecode.csv'
	path5 = '/Users/thalesfc/Downloads/description_nopunct.csv'
	path6 = '/Users/thalesfc/Downloads/description_stopwords.csv'
	path7 = '/Users/thalesfc/Downloads/description_lemma.csv'
	path8 = '/Users/thalesfc/Downloads/description_stem.csv'

	path8 = '/Users/thalesfc/Downloads/description_final.csv'

	check_file(open(path1, 'r'))
	remove_1tab(open(path1, 'r'), open(path2, 'w'))
	remove_authors(open(path2, 'r'), open(path3, 'w'))
	remove_unidecode(open(path3, 'r'), open(path4, 'w'))
	remove_punctuation(open(path4, 'r'), open(path5, 'w'))
	remove_stopwords(open(path5, 'r'), open(path6, 'w'))
	lemmatisation(open(path6, 'r'), open(path7, 'w'))
	stemmize(open(path7, 'r'), open(path8, 'w'))
