# ELI-20

ELI-20 (short hand for "Explain it to me like I'm 20) is a concept-simplifying resource mapping tool for assisted self-education. The idea is to project complex research articles into less complex spaces so that one may get the base information that they need to understand a given article. I use Wikipedia as a base resource because it is all encompassing, and is generally a good starting point for then translating into even less complex spaces such as college text books. Currently this project is basically just an MVP however I plan on making it a full scale open source educational resource for people to use at scale. So a walkthrough of whats going on under the hood is as follows:

###Step 1:

Upload a research article in PDF form to the web app, the web app frontend saves the article locally and the translates the article into a Log-Entropy TF-IDF vector.

###Step 2:

Take the Log-Entropy TF-IDF vector, and query it against a gensim Similairty index of Wikipedia (This is a sharded form of the Wikipedia corpus in Log-Entropy form). This returns the top 10 most relevant Wikipedia articles. These articles (hopefully/usually from my experience) are the more basic concepts needed to understand the original article so for example if given an article about Growing Neural Gas, it will possibley return pages about Self-Organizing Maps, Neural Networks, Neural gas, Matrices, Unsupervised Learning, Clustering Algorithms etc. 

###Step 3: 

Take those Wikipedia articles and query it against resources such as college text books to further return the most relevant pages or documents from those corpi.

###Step 4:

Repeat Step 3 with the returned results from every given step and keep projecting into less and less spaces until a given user is comfortable with the reading material at which point the user works their way up the material until they have a full understanding of whats going on in the original article.


You will need to download the following libraries:
Gensim, unidecode,  and slate (pdf parsing) 

I also recommend accelerating ATLAS/BLAS with fortran bindings to speed up making all the corpus data.


