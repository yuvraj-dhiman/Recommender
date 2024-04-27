import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans

class Model():
    def __init__(self, n_components, min_df, beta, gamma, score_indexes, clickthrough):
        self.n_components = n_components
        self.min_df = min_df
        self.transform_matrix = None
        self.vocab = None
        self.idf = None
        self.gamma = gamma
        self.beta = beta 
        self.score_indexes = score_indexes
        self.clickthrough = clickthrough


    def is_trained(self):
        return self.transform_matrix == None 

    def article_vectorizer(self, corpus):
        tfidf = TfidfVectorizer(min_df=self.min_df)
        raw_vectors = tfidf.fit_transform(list(map(lambda a: a.data_text, corpus)))
        self.vocab = tfidf.get_feature_names_out()
        self.idf = np.log(len(corpus) / np.count_nonzero(raw_vectors.toarray(), axis=0))
        svd = TruncatedSVD(n_components=self.n_components)
        self.transform_matrix = svd.fit_transform(raw_vectors.T)

    def train(self, corpus, users):
        self.article_vectorizer(corpus)
        self.user_clustering(users)

    def vectorize(self, a):
        tf = CountVectorizer(vocabulary=self.vocab).fit_transform([a.data_text]).toarray()
        v = (tf.T[:, 0] * self.idf) @ self.transform_matrix
        return v.T
    
    def score(self, uvec, a):
        dist = np.linalg.norm(self.vectorize(a) - uvec)
        score = np.exp(-self.gamma*a.age())/(1+dist)
        return score
    
    def cluster_user(self, user, users):
        users.insert(0, user)
        data = [user.prefs for user in users]
        identified_clusters = self.kmeans.fit_predict(data)
        print("Clustered")
        return self.kmeans.cluster_centers_[identified_clusters[0]]

    def recommend(self, user, corpus, users):
        args = np.argsort(list(map(lambda a: self.score(user.prefs, a), corpus)))[::-1]
        content_based = corpus[args[self.score_indexes]]
        print(args[self.score_indexes])
        print("Found content based")
        averagevec = self.cluster_user(user, users)
        args = np.argsort(list(map(lambda a: self.score(averagevec, a), corpus)))[::-1]
        collaborative = corpus[args[self.score_indexes]]
        print(args[self.score_indexes])
        print("Found collaborative")
        return content_based, collaborative

    def new_user_prefs(self, user, article, rating):
        return (self.beta * user.n * user.prefs + (rating + self.clickthrough) * self.vectorize(article)) / (self.beta * user.n + 1)

    def user_clustering(self, users):
        data = [user.prefs for user in users]
        n = len(data)
        nb = int(np.sqrt(n))
        wcss = np.zeros(nb)
        epsilon = 1e-5
        cluster_num = nb

        for i in range(1, nb):
            kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=n, n_init=10, random_state=0)
            kmeans.fit(data)
            wcss[i] = (kmeans.inertia_)
            derivative = np.abs(wcss[i]-wcss[i-1])
            if (derivative < epsilon):
                cluster_num = i
                break
        kmeans = KMeans(n_clusters=cluster_num, init='k-means++', max_iter=n, n_init=10, random_state=0)
        kmeans.fit(data)
        self.kmeans = kmeans

