# chatbotAI
Простой бот для Telegram с примитивным ИИ
1. chat-bot.py - Для работы с нейросетью. Может запускаться и работать в терминале.
2. chatbot_model.h5 - Модель нейросети.
3. classes/words.pkl - Упакованные массивы классов и слов.
4. intent.json - Словарь намерений. Нужен для обучения нейросети.
5. interface.py - Бот, обернутый в интерфейс Tkinter. Может запускаться.
6. telegram.py - Для запуска бота в Telegram. Требуется ввести токен и установить библиотеку aiogram.
7. training.py - Для обучения нейросети и сохранения её модели.
  
  Для работы потребуются библиотеки tensorflow и nltk.
      
      pip install nltk
      pip install tensorflow
      
 Для запуска в Телеграм дополнительно потребуется aiogram.
      
      pip install aiogram
