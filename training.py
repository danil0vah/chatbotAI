# -*- coding: utf-8 -*-
import random, json, pickle
import numpy as np

import nltk
#подгружаем nltk для работы с предложениями и словами
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD


lemmatizer = WordNetLemmatizer()

intents = json.load(open('intent.json', encoding='utf-8'))


words = []
classes = []
documents = []
ignore_letters = ['.', ',', '?', '!'] #список игнорируемых символов

#перебираем намерения
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern, language='russian')
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
#лемматиризуем слова            
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

#сохраним для последующей работы в chat_bot
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

#подготавливаем данные к обучению
#Все данные представляем в виде векторов со значениями 0 или 1 т.к с такими данными модели работать проще
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
        print(word)
        print(bag)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])


    
random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1]) 

#инициализируем модель и собираем её
model = Sequential()

model.add(Dense(128, input_shape=(len(train_x[0]),), activation = 'relu')) 
model.add(Dropout(0.5)) 
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation = 'softmax'))

# оптимизируем стохастическим градиентным спуском
sgd = SGD(lr=0.01, decay=1e-6, momentum = 0.9, nesterov=True)

#компилируем модель
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#обучаем модель
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

#сохраняем модель
model.save('chatbot_model.h5', hist)

print("Готово")
