# Automated Algorithmnic Trading Of Cryptocurrencies Utilising Opinion Mining

AATCUOP is an attempt to create an automated system for Bitcoin trading, implementing the techniques described in Colianni et al. to build a predictive model based on Twitter sentiment analysis [1].

### Setup
1. Install requirements:
`$ pip install -r requirements.txt`
2. Download the NLTK corpora: 
`$ python` 
`>>> import nltk` 
`>>> nltk.download`
3. Setup up tweepy:
How to setup [here](https://dev.twitter.com/twitterkit/android/advanced-setup).
4. Run:
`$ python main.py`

### Downloading the data set
You can download the data [here](https://drive.google.com/drive/folders/1HNm2PQ5S0rT9aoI6KvhhNoTgQoOcyU9T).

### References
[1] Colianni, Rosales, Signorotti. *Algorithmic Trading of Cryptocurrency Based on Twitter Sentiment Analysis* http://cs229.stanford.edu/proj2015/029_report.pdf. Web. 20 September 2016.
