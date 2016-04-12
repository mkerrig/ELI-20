import urllib
import slate
from pprint import pprint
import os
from gensim.corpora import wikicorpus,Dictionary
from gensim.models import LogEntropyModel
from os import listdir


def getArticles(query,subject='all',max_results=1,start=0):
	'''
	Get an article from arxiv.org by search term and return the names of the
	file(s) and and the title summaries of those articles

	Example:
	print getArticles('neural networks', max_results=2)

	Returns:

	([('neural networks1', 'http://arxiv.org/pdf/cs/0504056v1.pdf'),

	('neural networks2', 'http://arxiv.org/pdf/cs/0608073v1.pdf')],

	[('neural networks0','The principles of self-organizing the neural networks
	of optimal complexityis considered under the unrepresentative learning set.
	The method ofself-organizing the multi-layered neural networks is offered
	and used to trainthe logical neural networks which were applied to the
	medical diagnostics.'),

	('neural networks1', 'A review of works on associative neural networks
	accomplished during lastfour years in the Institute of Optical Neural
	Technologies RAS is given. Thepresentation is based on description of
	parametrical neural networks (PNN). For today PNN have record recognizing
	characteristics (storage capacity, noise immunity and speed of
	operation). Presentation of basic ideas and principles is accentuated.')])
	'''
	pdf_links = []
	title_key = 'default'
	titles_summaries = []
	base_url = 'http://export.arxiv.org/api/query?search_query='
	url = base_url + subject + ':' + query + '&start=' + str(start) + \
	'&max_results=' + str(max_results)

	data = urllib.urlopen(url).read()
	summary_read = False
	curr_summary = ''
	summary_cnt = 0
	for line in data.split('\n'):
		if '<summary>' in line or summary_read == True:
			summary_read = True
			if '</summary>' in line:
				summary_read = False
				curr_summary = curr_summary.replace('<summary>','')
				curr_summary = curr_summary.strip()
				boo = True
	                        title_key = query.replace('+','_')+str(summary_cnt)
        	                while boo:
                	                if os.path.isfile(title_key):
						summary_cnt+=1
                        	                title_key = query.replace('+','_')\
											+ str(summary_cnt)
                                	else:
                                        	boo = False

				titles_summaries.append((title_key, curr_summary))
				curr_summary = ''
				summary_cnt+=1
				continue
			curr_summary+=line
		if '<link title="pdf"' in line:
			index1 = line.index('href="')+6
			index2 = line.index('"',index1)
			boo = True
			title_key = query.replace('+','_')+str(summary_cnt)
			while boo:
				if os.path.isfile(title_key):
					summary_cnt+=1
					title_key = query.replace('+','_')+str(summary_cnt)
				else:
					boo = False
			pdf_links.append((title_key,line[index1:index2]+'.pdf'))

	return pdf_links,titles_summaries


def DownloadPdf(pdf_links,titles_summaries):
	'''
	This method downloads the PDF's to your local machine from the links
	provided by getArticles()

	Example:
	DownloadPdf(getArticles('neural networks', max_results=2))
	Will store the resulting PDF's in /data/articleData/pdfs/ and their
	accompanying summaries in articleData/title_summaries.txt
	'''

	for link in pdf_links:
		os.system('curl -o ../data/articleData/pdfs/'+link[0]+'.pdf '
		+ link[1])

	f = open('../data/articleData/title_summaries.txt','a')
	for summary in titles_summaries:
		f.write(summary[0]+' : '+summary[1]+'\n')
	f.close()

def Pdf2Vec(titles):
	'''
	Vectorizes a given PDF on your local filesystem to a Log Entropy TF-IDF
	vector to then query against your similarity index

	Returns:

	[document-logent-vec-1, document-logent-vec-2, ... ,document-logent-vec-N]
	where N is is the number of titles
	'''
	#TODO: Make it so you can give a model as an arguement to vecorize a given
	#document into any trained gensim model
	
	ret_lst = []
	logent = LogEntropyModel.load('../models/logEntropy.model')
	diction = Dictionary.load('../models/wiki_dict.dict')
        for title in titles:
		curr_file = open('../data/articleData/pdfs/'+title+'.pdf')
		doc = slate.PDF(curr_file)
		doc = ' '.join(doc)
		doc_tokens = wikicorpus.tokenize(doc)
		bow = diction.doc2bow(doc_tokens)
		bow_logent = logent[bow]
		ret_lst.append(bow_logent)
		curr_file.close()

	return ret_lst


def getCurrentTitles():
	'''
	Gets current titles of the PDFs in the /data/articleData/pdfs directory
	'''
	lst = os.listdir('../data/articleData/pdfs/')
	lst = [x.replace('.pdf','') for x in lst]
	return lst
print getArticles('neural networks', max_results=2)
