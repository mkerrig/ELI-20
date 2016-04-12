from __future__ import print_function
import logging, os, bz2
from gensim import corpora
from gensim.corpora import mmcorpus,MmCorpus
from gensim.models import LogEntropyModel, TfidfModel
from gensim.similarities import Similarity
from unidecode import unidecode
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
level=logging.INFO)

'''
This script downloads a dump of wikipedia and parses it into a Bag of Words
matrix,TF-IDF matrix, and Log-Entropy TF-IDF matrix, all in Market Matrix
Format. It then shards the Log-Entropy TF-IDF matrix and creates an index
to query for the most similar Wikipedia documents. It also gets a list of
titles for each document that do exist in the matrices because many get
filtered out as a result of gensim's preprocessing.

Takes quite awhile to run this whole thing, I personally haven't timed it
but I know that it will take at least 12 hours, so I would just let this run
somewhere for a bit.

Additionally you will need quite a bit of space to store all of this
the Wikipedia dump is ~14GB and then the three Matrices each take ~22-27GB
of space, so I would suggest having around 100GB of space to store all of this.
Once LSI is implemented one will not need to store all of these Matrices, but
until then your going to have to find the space to use this.


Useful notes:

Market Matrix format looks as follows:
[ vector-1 = [(word-id-1, metric-1), (word-id-2, metric-2), ... ,(word-id-n,
metric-n)], [vector-2], [vector-3], ... ,[vector-m] ]

Where vector-i is the ith document in the corpus, n = the highest word-id of
each document vector Market Matrix only contains the word-ids that actually
appear in the document , and then m = number of documents in the corpus


'''
wiki_link = 'https://dumps.wikimedia.org/enwiki/20150805\
/enwiki-20150805-pages-articles.xml.bz2'
wiki_file = '../data/enwiki-latest-pages-articles.xml.bz2'

# This download should take awhile, speed will depend on internet connection
os.system('wget '+ wiki_link + ' -O ' + wiki_file)

# Build wikicorpus and save the BOW matrix in MarketMatrix format took me
# approximately 8 hours on a 8GB machine with a dual core processor

wiki_corpus =corpora.wikicorpus.WikiCorpus(wiki_file)

print('Finished making the wikicorpus, saving BOW corpus\n')
corpora.mmcorpus.MmCorpus.serialize('../data/wiki_en_vocab200k', wiki_corpus)
print('Done saving BOW Corpus\n')

# Save the dicitonary, you will need it to convert future documents into
# BOW format

#wiki.dictionary.save("../data/wiki_dict.dict")
#print 'Saved dictionary'

print('Creating LogEntropy TF-IDF and regular TF-IDF matrices and models')
BOW_corpus = MmCorpus('../data/wiki_en_vocab200k') #Resurrect BOW corpus

#log_entropy = LogEntropyModel(BOW_corpus)
#log_entropy.save('../models/logEntropy.model') #already provided
log_entropy = LogEntropyModel.load('../models/logEntropy.model')
corpora.mmcorpus.MmCorpus.serialize('../data/log_entropy_matrix',
log_entropy[BOW_corpus])

print('Saved LogEntropy TF-IDF matrix')

#tfidf = TfidfModel(BOW_corpus)
#tfidf.save('../models/tfidf.model') #already provided
tfidf = TfidfModel.load('../models/tfidf.model')
corpora.mmcorpus.MmCorpus.serialize('../data/log_entropy_matrix',
tfidf[BOW_corpus])

print('Saved LogEntropy TF-IDF matrix')

print('Creating Similarity Index')
logent_corpus = MmCorpus('../data/log_entropy_matrix')
num_feat = len(wiki.dictionary.keys())
index = Similarity('../data/logEntropyShards/logEntropySimilarity',
logent_corpus, num_features=num_feat)

index.save('../data/logEntropyShards/logEntropySimilarityIndex')
print('Saved Shards and similarity index')

print('Getting list of titles...')
bz2_wiki = bz2.BZ2File(wiki_file, "r")
extract = corpora.wikicorpus.extract_pages(bz2_wiki)
i = 0
matches = open('../data/title_matches.txt','a')
for title,doc,z in extract:
	wiki_filt = corpora.wikicorpus.filter_wiki(doc)
	doc_token = corpora.wikicorpus.tokenize(wiki_filt)
	bowbow = diction.doc2bow(doc_token)
	if bowbow == BOW_corpus[i]:
		i+=1
		print(unidecode(title),file=matches)
		if i % 100000 == 0:
			print('match found:',unidecode(x))
matches.close()
print('Finished!')
