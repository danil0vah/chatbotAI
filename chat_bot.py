# -*- coding: utf-8 -*-
import random,json,pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model
nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()


model = load_model('chatbot_model.h5')

intents = json.loads(open('intent.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Вернем мешок слов(подробнее см.Wiki):0 или 1 для каждого слова в мешке, которое существует в предложении

def bow(sentence, words, show_details=True):
    # Токенизируем предложения/паттерны
    sentence_words = clean_up_sentence(sentence)
    # мешок слов предствален в виде матрицы из N слов
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # присваиваем 1, если текущее слово находится в словарной позиции
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # фильтруем предикты ниже порога  - ERROR_TRESHOLD
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # сортируем по вероятности
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

if __name__ == '__main__':
    
    while True:
        message = input('Вы:  ')
        res = chatbot_response(message)
        
        print("Бот: "+ res)


