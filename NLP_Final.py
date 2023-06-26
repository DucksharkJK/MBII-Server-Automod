# Semantic Analysis Script

import string

import numpy as np
import pandas as pd

import spacy

import pkg_resources
from symspellpy import SymSpell, Verbosity

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# Create our list of punctuation marks
punctuations = string.punctuation

# Create our list of stopwords
nlp = spacy.load('en_core_web_sm', exclude=["parser", "ner"])
stop_words = spacy.lang.en.stop_words.STOP_WORDS

df_moviebattles = pd.read_csv("TestData_sm.csv")

# Adding words to check
vector_data = {u"sith": np.random.uniform(-1, 1, (300,)),
               u"jedi": np.random.uniform(-1, 1, (300,)),
               u"lmao": np.random.uniform(-1, 1, (300,)),
               u"lol": np.random.uniform(-1, 1, (300,)),
               u"rofl": np.random.uniform(-1, 1, (300,)),
               u"rtv": np.random.uniform(-1, 1, (300,))}
vocab = nlp.vocab  # Get the vocab from the model
for word, vector in vector_data.items():
    vocab.set_vector(word, vector)

# Creating our tokenizer function
def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = nlp(sentence)

    # Lemmatizing each token and converting each token into lowercase
    mytokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens]

    # Removing stop words
    mytokens = [word for word in mytokens if word not in stop_words and word not in punctuations]

    print(mytokens)
    # return preprocessed list of tokens
    return mytokens

# Custom transformer using spaCy
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        # Cleaning Text
        return [clean_text(str(text)) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}

# Basic function to clean the text
def clean_text(text):
    # Removing spaces and converting text into lowercase
    return text.strip().lower()

bow_vector = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range=(1,1))

tfidf_vector = TfidfVectorizer(tokenizer = spacy_tokenizer)

X = df_moviebattles['Chats'] # the text we want to analyze
ylabels = df_moviebattles['Slurs_Racism'] # the labelled answers we want to test against

X_train, X_test, y_train, y_test = train_test_split(X, ylabels, test_size=0.4, random_state=42)

# Logistic Regression Classifier
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()

# Create pipeline using Bag of Words
pipe = Pipeline([("cleaner", predictors()),
                 ('vectorizer', bow_vector),
                 ('classifier', classifier)])

# model generation
pipe.fit(X_train,y_train)

from sklearn import metrics
# Predicting with a test dataset
predicted = pipe.predict(X_test)

# Model Accuracy
print("Logistic Regression Accuracy:",metrics.accuracy_score(y_test, predicted))
print("Logistic Regression Precision:",metrics.precision_score(y_test, predicted))
print("Logistic Regression Recall:",metrics.recall_score(y_test, predicted))

print("NLP Pipeline online.")

def autocorrect(input_text):    
    result = sym_spell.word_segmentation(input_text)
    return pipe.predict([result.corrected_string])[0]

def text_analysis(input_list):
    output_list = []

    for sentence in input_list:
        sentence_score = []
        sentence_score.append(max([autocorrect(sentence), autocorrect("".join(sentence.split())), pipe.predict([sentence])[0]]))

        output_list.append(sentence_score[0])

    print(output_list)

list_of_inputs = ["fuck you jedi nigger", 
                    "shut the fuck up you fucking retard", 
                    "get rekt you goddamn idiot faggot",
                    "you fucking n1ggers need to shut up",
                    "Ihatealltheniggerswhoonlyplayjedi", 
                    "fuck this game dude holy fucking shit",
                    "these fagg0ts need to learn to shut up",
                    "This retard sith needs to learn to push those clones",
                    "The jews are the f4gg0ts of the earth",
                    "fuckn1gg3rs",
                    "f u c k n i g g e r s",
                    "these f4gs need to jump off a bridge",
                    "kill all the n1gg3rs"]

text_analysis(list_of_inputs)

# print(pipe.predict(list_of_inputs))