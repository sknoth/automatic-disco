# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 08:07:20 2018

@author: Imran Shokat SE
"""
#I have created a raw code just to get the results for specif task.
import xlrd
import re
import string
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
stop_words = stopwords.words('swedish')

workbook = xlrd.open_workbook('F:/Software Technology/Semester 3/Adaptive and Semantic Web/Final Project/diabetes_august_2017.xlsx')
sheet = workbook.sheet_by_index(0)

tweet_list=[]
for row in range(5, sheet.nrows-68):
    tweet_list.append(sheet.row(row)[5].value)

##Remove the URL, Links from the text of tweets
def remove_links(tweet):
    myregex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(myregex, tweet)
    for link in links:
        tweet = tweet.replace(link[0], '')
    return tweet
#Remove @ and # from the text of tweets
def remove_punctuations(tweet):
    myprefixes = ['RT','@','#',"\\U"]
    for value in  string.punctuation:
        if value not in myprefixes :
            tweet = tweet.replace(value,' ')
    finalText = []
    for word in tweet.split():
        word = word.strip()
        if word:
            if word[0] not in myprefixes:
                finalText.append(word)
    return ' '.join(finalText)

cleaned_list=[]
for tweet in tweet_list:
    cleaned_list.append(remove_punctuations(remove_links(tweet)))
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]
data_words_nostops = remove_stopwords(cleaned_list)

wrdCloud=''
#strr=[]
for row in data_words_nostops:
#    strr.append(",".join(row))
    wrdCloud+=" ".join(row)
texts=""
for row in data_words_nostops:
    texts+=','
    texts+= ','.join(row)
# spacy for lemmatization
from spacy.lang.sv import Swedish
nlp = Swedish()
doc_lemmatized = nlp(texts)
##print('Tags', [(t.text) for t in doc_lemmatized])
ftext=[]
for wrd in doc_lemmatized:
    coma = ','
    if(wrd.text!=','):
        ftext.append(wrd.text)
#    words = " ".join(re.findall("[a-z\såäö]+", line[1]))
#    topic_words.append(words.split())

#RQ2 implementation start here     
retweeted=[]
for row in tweet_list:
    if row.startswith('RT'):
        retweeted.append(row)
createFile= open("F:/Software Technology/Semester 3/Adaptive and Semantic Web/Final Project/ReTweeted_Tweets.text","w+", encoding='utf-8') #for saving one by one file
createFile.write(str(retweeted))
createFile.close()
#import json
#with open('F:/Software Technology/Semester 4/Topic Results/Final Results/ReTweeted_Tweets.json', 'w') as tfile:
#    json.dump(retweeted, tfile)
#282 are retweeted 
import collections
values=[item for item, count in collections.Counter(retweeted).items() if count >=1] #count 1 will show the entries which tweeted once, 2 mean two time, upto so on. We have to chage it manually

#1 tweet, 8 times =RT @Finwire: Novo Nordisk nya diabetesläkemedel lyckades nå uppsatta mål #novonordisk #diabetes  https://t.co/7GFr1a3wzY
#1 tweet, 7 times= RT @barndiabetes: #svt tar upp Elin och kampanjen #TYP-1 https://t.co/4nyuAtvbHO #botadiabetes #typ1 #välgörenhet #stödforskningen #barndia…
#..............
#2 tweets, 6 times:
# RT @barndiabetes: Hjälp Barndiabetesfonden via Christian och Johan Holmudd! Skänk en gåva eller sprid vidare denna länk. https://t.co/lVMu5…
# RT @Expressen: Diabetessjuke Anton, 17, har varit försvunnen ett dygn – polisen vädjar om hjälp.https://t.co/bpgEpVIcit https://t.co/3zcOQ…
#......
#3 tweets, 5 times:
#RT @ellinorakeson: Min äldsta, men fortfarande väldigt lilla, systerson Linus har blivit diagnosticerad med diabetes, så nu är han InsuLinu…
#RT @nutritionsfakta: Kostråd till familjer kring fett, mer frukt, grönt o fibrer ger lägre LDL o blodtryck, samt ökad insulinkänslighet.ht…
#RT @forteforskning: Patienter med typ 2-diabetes som diagnosticeras genom screening har bättre överlevnad @umeauniversitet https://t.co/7tp…
#......
#8 tweets, 4 times:

#.....
#10 tweets, 3 times:
#.....
#24 tweets, 2 times:
#.....
#103 tweets, 1 time

#RQ3 implementation start here 
linkedTweets=[]
links=[]
for row in tweet_list:
    if(re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', row)):
        linkedTweets.append(row)
        links.append(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', row))

createFile= open("F:/Software Technology/Semester 3/Adaptive and Semantic Web/Final Project/Tweets_contains_links.txt","w+", encoding='utf-8') #for saving one by one file
createFile.write(str(linkedTweets))
createFile.close()
#572 links total
#check duplicate links
linksdupli=[item for item, count in collections.Counter(linkedTweets).items() if count ==2] #count 3, 4 upto so on





