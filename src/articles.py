import numpy as np
import time
import database
import nltk.tokenize as nltkt
import nltk.corpus as nltkc
import nltk.stem as nltks

class Article:
    def __init__(self, a=None):
        if a != None:
            a.nlp()
            self.title = a.title
            self.text = a.text
            self.summary = a.summary
            self.pubDate = time.mktime(a.publish_date.timetuple()) if a.publish_date else time.time()
            self.link = a.canonical_link
            self.hash = a.link_hash
            self.author = ", ".join(a.authors)
            self.preprocess()
    
    def save(self):
        return database.insert_into(
            "articles",
            ("title", "text", "summary", "pubDate", "link", "hash", "author", "data_text"),
            (self.title, self.text, self.summary, self.pubDate, self.link, 
             self.hash, self.author, self.data_text) 
        )
    
    def age(self):
        return (time.time() - self.pubDate) / 86400
   
    def rating_from_interaction(self, int_time):
        # https://psyarxiv.com/xynwg/
        mu = 250
        std = 10
        num_words = len(self.text.split())
        wpm = num_words/(int_time/60)
        demean_wpm = wpm-mu
        if demean_wpm > 2*std:
            return 0 # not read
        return sorted((-1, demean_wpm/(2*std) + 0.5, 1))[1]

    def preprocess(self):
        self.data_text  = self.text.lower()
        #Tokenize
        word_tokens_summary = nltkt.word_tokenize(self.data_text)
        #Lemmetize
        lemmatizer = nltks.WordNetLemmatizer()
        lemmatized_output_sum = ' '.join([lemmatizer.lemmatize(w) for w in word_tokens_summary])
        #Stopwords
        stop_words = set(nltkc.stopwords.words('english'))
        word_tokens_summary = nltkt.word_tokenize(lemmatized_output_sum)
        filtered_sentence_sum = [w for w in word_tokens_summary if not w.lower() in stop_words]
        self.data_text = " ".join(filtered_sentence_sum)

    def from_row(self, row):
        self.title = row[0]
        self.pubDate = row[1]
        self.text = row[2]
        self.data_text = row[3]
        self.summary = row[4]
        self.author = row[5]
        self.link = row[6]
        self.hash = row[7]

def get_article(linkhash):
    rows = database.exec_select("SELECT * FROM articles WHERE hash=?", (linkhash,))
    a = Article()
    a.from_row(rows[0])
    return a

def get_all_articles():
    curr = database.get_cursor()
    rows = curr.execute("SELECT * FROM articles").fetchall()
    def f(row):
        a = Article()
        a.from_row(row)
        return a
    return np.array([f(row) for row in rows])

