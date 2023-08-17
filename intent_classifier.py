import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression

class IntentClassifier:
    def __init__(self):
        fields = ["Expressions", "Intent"]
        self.data = pd.read_csv("C:\\Users\\ACER\\Documents\\GitHub\\Ami\\data.csv", sep=",", header=None, names=fields,encoding= 'unicode_escape')
        
        self.train() #It will train whenever an instance is made

    def train(self):
        X_train, y_train= self.data['Expressions'], self.data['Intent']
        self.count_vect = CountVectorizer()
        X_train_counts = self.count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts) #Calculates tf-idf for the text
        self.clf = LogisticRegression().fit(X_train_tfidf, y_train)
    
    def predict(self, text):
        return self.clf.predict(self.count_vect.transform([text]))[0]
        


