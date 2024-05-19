import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import pipeline
from collections import defaultdict
from data import Data
import spacy
import requests

nltk.download('punkt')
nltk.download('stopwords')

BANNED = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']

nlp = spacy.load('en_core_web_md')

classification = pipeline('sentiment-analysis')

Data = Data()
Data = {key.lower(): value for key, value in Data.items()}
elements_with_emotions = []

def Clean_Text(Text):
    words = word_tokenize(Text)
    stop_words = set(stopwords.words('english'))
    cleaned_words = [word.lower() for word in words if word.lower() not in stop_words 
                     and word.isalpha() and word.lower() not in BANNED]
    return cleaned_words

def similarity(word1, word2):
    return nlp(word1).similarity(nlp(word2))

def Get_Synonyms(word):
    api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'.format(word)
    response = requests.get(api_url, headers={'X-Api-Key': ''})
    try:
        if response.status_code == requests.codes.ok:
            data = response.json()
            synonyms = data.get('synonyms', [])
            return synonyms
    except Exception as e:
        print(f"Error getting synonyms: {e}")

def Similarity(word1, word2):
    return similarity(word1, word2)

def Probability(Text):
    words = Clean_Text(Text)
    emotions = []
    flag = False
    for word in words:
        if word.lower() in Data or word.lower() in elements_with_emotions:
            emotions.append(Data[word.lower()])
        else:
            synonyms = Get_Synonyms(word)
            if synonyms:
                for synonym in synonyms:
                    if synonym.lower() in Data:
                        flag = True
                        try:
                            emotions.append(Data[synonym.lower()])
                            Data[synonym.lower()] = Data[synonym.lower()]
                            elements_with_emotions.append({word, emotion})
                        except Exception as e:
                            print(f"Error adding synonym to data: {e}")
            else:
                for key in Data:
                    if Similarity(word, key) > 0.7:
                        emotions.append(Data[key])
                        flag = True
                        elements_with_emotions.append({word, emotion})

    if not flag:
        emotions.append('Neutral')
    total = len(emotions)
    if total == 0:
        return 'No emotions detected.'
    prob = defaultdict(int)
    for emotion in emotions:
        prob[emotion] += 1
    for emotion in prob:
        prob[emotion] /= total
        prob[emotion] *= 100
        prob[emotion] = round(prob[emotion], 2)
    return dict(prob)

def P_or_N(Text):
    try:
        results = classification(Text)
        if not results:
            return "UNKNOWN"
        elif len(results) == 1:
            return results[0]['label']
        else:
            return max(results, key=lambda x: x['score'])['label']
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "UNKNOWN"