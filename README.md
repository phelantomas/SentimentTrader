
  
# Automated Algorithmnic Trading Of Cryptocurrencies Utilising Opinion Mining

AATCUOP is a 4th year college project that is an attempt to create an automated system for Bitcoin trading, utilizing sentiment analysis of Twitter to build a predictive model.

### Setup
1. Clone the repository: `$ git clone https://github.com/phelantomas/CollegeProject.git`
2. `$ cd CollegeProject`
3. Requires PyQt4, guide to install for Linux:
	2.1. `$ sudo apt-get install python-qt4`
For mac:
	2.2. `$ brew install cartr/qt4/pyqt`
4. Install requirements from the requirements.txt file:
`$ sudo pip install -r requirements.txt`
	4.1. For Mac `$ easy_install pandas`
5. Download the NLTK corpora for Linux and Mac: 
`$ python` 
`>>> import nltk` 
`>>> nltk.download`
Then follow the prompts to finish installing.  
For Mac, simply follow the steps [here](http://nlpworkgroup.postach.io/post/install-nltk-for-python-2-7-on-mac-osx) if the above doesn't work.
6. Setup up tweepy:
You will need a twitter account and developer keys in order to make use of the twitter API. Follow the setup [here](https://dev.twitter.com/twitterkit/android/advanced-setup). Once the keys are got, update the keys in the tweepy_config.py file.
7. Select a cryptocurrency to predict:
Once the applications requirements are installed, you will need to configure the application with your desired cryptocurrency. By default it chooses Bitcoin. If you want to change this you will need to edit the cryptocurrency_config.py file.
8. Run: `$ python main.py`

### Downloading sample data sets
You can download pre-made data sets for Bitcoin, Litecoin, and Ethereum [here](https://drive.google.com/drive/folders/1HNm2PQ5S0rT9aoI6KvhhNoTgQoOcyU9T). Once downloaded, place into the Features folder.

### References
[1] Colianni, Rosales, Signorotti. *Algorithmic Trading of Cryptocurrency Based on Twitter Sentiment Analysis* http://cs229.stanford.edu/proj2015/029_report.pdf.  
[2] Website with links to all documentation [here](http://glasnost.itcarlow.ie/~softeng4/C00192548/index.html).
