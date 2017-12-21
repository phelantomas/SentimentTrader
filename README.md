# Automated Algorithmnic Trading Of Cryptocurrencies Utilising Opinion Mining

AATCUOP is an attempt to create an automated system for Bitcoin trading, implementing the techniques described in Colianni et al. to build a predictive model based on Twitter sentiment analysis [1].

### Setup
1. Create a new virtual environment
`$ virtualenv -p python3 venv`
`$ source venv/bin/activate`
`$ pip install -r requirements.txt`
2. Download the NLTK corpora: 
`$ python` 
`>>> import nltk` 
`>>> nltk.download`

### Instructions
python collect_tweets.py -o raw_tweets.txt
python process_tweets.py -i raw_tweets.txt -o processed_tweets.txt

### Downloading the data set
You can download the data [here](https://drive.google.com/open?id=0BzqCBdvJ6j-nUzRZckRJUVJwY00).

### References
[1] Colianni, Rosales, Signorotti. *Algorithmic Trading of Cryptocurrency Based on Twitter Sentiment Analysis* http://cs229.stanford.edu/proj2015/029_report.pdf. Web. 20 September 2016.
