
# Automated Algorithmnic Trading Of Cryptocurrencies Utilising Opinion Mining

AATCUOP is a 4th year college project that is an attempt to create an automated system for Bitcoin trading, utilizing sentiment analysis of Twitter to build a predictive model.

### Setup
1. Requires PyQt4, guide to install for Linux [here.](https://www.saltycrane.com/blog/2008/01/how-to-install-pyqt4-on-ubuntu-linux/) For mac, follow [here](https://robonobodojo.wordpress.com/2017/02/08/installing-pyqt4-on-mac-osx/) instead.
3. Install requirements from the Pipfile:
`$ pipenv install`
4. Download the NLTK corpora for Linux: 
`$ python` 
`>>> import nltk` 
`>>> nltk.download`
Then follow the prompts to finish installing.  
For Mac, simply follow the steps [here](http://nlpworkgroup.postach.io/post/install-nltk-for-python-2-7-on-mac-osx) if the above doesn't work.
5. Setup up tweepy:
You will need a twitter account and developer keys in order to make use of the twitter API. Follow the setup [here](https://dev.twitter.com/twitterkit/android/advanced-setup). Once the keys are got, update the keys in the tweepy_config.py file.
6. Select a cryptocurrency to predict:
Once the applications requirements are installed, you will need to configure the application with your desired cryptocurrency. By default it chooses Bitcoin. If you want to change this you will need to edit the cryptocurrency_config.py file.
7. Run:
`$ python main.py`

### Downloading sample data sets
You can download pre-made data sets for Bitcoin, Litecoin, and Ethereum [here](https://drive.google.com/drive/folders/1HNm2PQ5S0rT9aoI6KvhhNoTgQoOcyU9T). Once downloaded, place into the Features folder.

### References
[1] Colianni, Rosales, Signorotti. *Algorithmic Trading of Cryptocurrency Based on Twitter Sentiment Analysis* http://cs229.stanford.edu/proj2015/029_report.pdf.  
[2] Website with links to all documentation.
