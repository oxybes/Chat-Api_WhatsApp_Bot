# WhatsApp Bot
Демо-Бот для работы с api https://chat-api.com/ru/swagger.html сайта https://chat-api.com

# Возможности:
- Вывод списка команд
- Вывод ID текущего чата
- Вывод текущего времени сервера, на котором работает бот.
- Вывод вашего имени
- Отправка файлов разных форматов (pdf, jpg, doc, mp3 и т.д.)
- Отправка заранее записанных голосовых сообщений
- Отправка гео-координат (локации)
- Создание конференции (группы)

Внимание: чтобы бот работал, телефон должен быть всегда подключен к интернету и не должен использоваться для Whatsapp Web. Удобнее всего заводить отдельное устройство для этих целей.

# Компиляция и тестирование бота
Для тестировани бота вам потребуется библиотека Flask инсталлируйте её с помощью
> pip install flask

Далее склонируйте репозиторий себе.
После чего перейдите в файл wabot.py и измените переменные APIUrl и token на ваши из личного кабинета
https://app.chat-api.com/instance/

К сожалению, WebHook  не позволяет указывать в качестве сслыки ip, поэтому для тестирования бота вам потребуется эмулировать запросы к WebHook. Для этого можно перейти по ссылке https://app.chat-api.com/testing, перейти во вкладку "Проверка WebHook"  и нажать на кнопку "Начать тестирование".

Сервер подключит свой WebHook. Переходим к себе в WhatsApp и пишем сообщения в чат. Теперь во вкладке "Проверка WebHook" будут отображаться JSON запросы, которые принял WebHook, когда мы посылали ему сообщения.

Копируем этот JSON и запускаем наш локальный сервер FLASK с помощью отладчика в редакторе кода или через команду
> flask run

Чтобы эмулировать запрос к серверу нам необходимо послать POST запрос с JSON, который мы скопировали на предыдущем этапе. Запрос отправляется на ваш localhost адрес, на котором запущен flask. Таким образом можно эмулировать действия WebHook и тестировать функционал бота.

# Функции
## send_request 
Служит для отправки запросов к API сайта
```python
 def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()
```
- **method** определяет, какой метод chatAPI должен быть вызван.
- **data** содержит необходимые для пересылки данные.


## send_message
Служит для отправки сообщений в чат WhatsApp
```python
 def send_message(self, chatID, text):
        data = {"chatID" : chatID,
                "body" : text}  
        answer = self.send_requests('sendMessage', data)
        return answer
```
- ChatID – Id чата, в который необходимо отправить сообщение
- Text – Текст сообщения

## show_chat_id
Служит для ответа на команду "chatId". Отправляет в чат WA id пользователя
```python
def show_chat_id(self,chatID):
        return self.send_message(chatID, f"Chat ID : {chatID}")
```
- ChatID – Id чата, в который необходимо отправить сообщение

## time
Служит для ответа на команду "time". Отправляет в чат WA текущее время сервера.
```python
def time(self, chatID):
        t = datetime.datetime.now()
        time = t.strftime('%d:%m:%Y')
        return self.send_message(chatID, time)
```
- ChatID – Id чата, в который необходимо отправить сообщение

## file 
Служит для ответа на команду "file". Отправляет в чат WA файл, который лежит на сервере по указанному формату
 ```python
def file(self, chatID, format):
        availableFiles = {'doc' : 'document.doc',
                        'gif' : 'gifka.gif',
                        'jpg' : 'jpgfile.jpg',
                        'png' : 'pngfile.png',
                        'pdf' : 'presentation.pdf',
                        'mp4' : 'video.mp4',
                        'mp3' : 'mp3file.mp3'}
        if format in availableFiles.keys():
            data = {
                        'chatId' : chatID,
                        'body': f'https://domain.com/Python/{availableFiles[format]}',                      
                        'filename' : availableFiles[format],
                        'caption' : f'Get your file {availableFiles[format]}'
                    }
            return self.send_requests('sendFile', data)
```
- chatID – Id чата, в который необходимо отправить сообщение
- format – формат файла, который необходимо отправить. Все отправляемые файлы хранятся на сервере.

Что представляет из себя *data*
- ChatID – Id чата, в который необходимо отправить сообщение
- Body – прямая ссылка до файла, который необходимо отправить
- Filename – имя файла
- Caption – текст, который будет отправлен вместе с файлом
Формируем запрос **send_requests** с параметром **“sendFile”**  и передаем в него* data*.

## ptt
Служит для отправки голосового сообщения в чат WA.
```python
def ptt(self, chatID):        
            data = {
            "audio" : 'https://domain.com/Python/ptt.ogg',
            "chatId" : chatID }
            return self.send_requests('sendAudio', data)
```
- ChatID – Id чата, в который необходимо отправить сообщение

Что представляет из себя *data*
- “audio”  – прямая ссылка на файл формата ogg
-  "chatID" – Id чата, в который необходимо отправить сообщение

Формируем запрос **send_requests** с параметром **“sendAudio”**  и передаем в него* data*.

## geo
Служит для отправки гео-локации в чат WA
def geo(self, chatID):
```python
        data = {
                "lat" : '51.51916',
                "lng" : '-0.139214',
                "address" :'Ваш адрес',
                "chatId" : chatID
        }
        answer = self.send_requests('sendLocation', data)
        return answer
```
- ChatID – Id чата, в который необходимо отправить сообщение

Что представляет из себя *data*
- "сhatID" – Id чата, в который необходимо отправить сообщение
- “lat” – заранее заданные координаты
- “lng” – координаты
- “address” – ваш адрес или любая необходимая вам строка.

Формируем запрос **send_requests** с параметром **“sendLocation”**  и передаем в него* data*.

## group
Служит для создания конференции, состоящей из бота и пользователя
```python
def group(self, author):
        phone = author.replace('@c.us', '')
        data = {
            "groupName"  :  'Group with the bot Python',
             "phones"  :  phone,
             "messageText"  :  'It is your group. Enjoy'
        }
        answer = self.send_requests('group', data)
        return answer
```
- author – тело json, посылаемое webhook, содержит информацию о том, кто отправил сообщение. 

Что представляет из себя *data*
- “groupName” – имя конференции после её создания
- “phones” – телефоны необходимых участников конференции, можно передавать массив из нескольких телефонов 
- “messageText” – Первое сообщение в конференции.

Формируем запрос **send_requests** с параметром **“group”**  и передаем в него* data*.

# Обработка входящих сообщений
Обработкой сообщений занимается функция 
```python
def processing(self):
        if self.dict_messages != []:
            for message in self.dict_messages:
                text = message['body'].split()
                if not message['fromMe']:
                    id  = message['chatId']
                    if text[0].lower() == 'hi':
                        return self.welcome(id)
                    elif text[0].lower() == 'time':
                        return self.time(id)
                    elif text[0].lower() == 'chatid':
                        return self.show_chat_id(id)
                    elif text[0].lower() == 'me':
                        return self.me(id, message['senderName'])
                    elif text[0].lower() == 'file':
                        return self.file(id, text[1])
                    elif text[0].lower() == 'ptt':
                        return self.ptt(id)
                    elif text[0].lower() == 'geo':
                        return self.geo(id)
                    elif text[0].lower() == 'group':
                        return self.group(message['author'])
                    else:
                        return self.welcome(id, True)
                else: return 'NoCommand'
```

Данная функция будет вызываться каждый раз, когда будем получать данные в наш webhook.

Данная проверка отсеивает данные, которые не содержат в себе сообщений. Так как к webhook может прийти запрос без сообщения.
```python
 if self.dict_messages != []:
```

В действительности нам может прийти несколько сообщений в одном запросе, и наш бот должен обработать их все. Для этого мы перебираем все словари, который содержит в себе лист dict_messages.

```python
for message in self.dict_messages:
                text = message['body'].split()
```
Тело *"body"* является текстом сообщения в json, который передается во входящем сообщении? поэтмоу его записываем в text. 

Далее мы делаем проверку, что входящее сообщение не от нас самих, посредством обращения к ключу ‘fromMe”, который содержит в себе True или False и проверяет от кого было сообщение.  Иначе бот уйдет в рекурсию

```python
 if not message['fromMe']:
```

А далее просто разбираем какая команда пришла и вызываем соответствующие функции 
```python
if text[0].lower() == 'hi':
                        return self.welcome(id)
                    elif text[0].lower() == 'time':
                        return self.time(id)
                    elif text[0].lower() == 'chatid':
                        return self.show_chat_id(id)
                    elif text[0].lower() == 'me':
                        return self.me(id, message['senderName'])
                    elif text[0].lower() == 'file':
                        return self.file(id, text[1])
                    elif text[0].lower() == 'ptt':
                        return self.ptt(id)
                    elif text[0].lower() == 'geo':
                        return self.geo(id)
                    elif text[0].lower() == 'group':
                        return self.group(message['author'])
                    else:
                        return self.welcome(id, True)
                else: return 'NoCommand'
```

# Flask 
Для обработки входящих запросов к нашему серверу используем данную функцию 
```python
@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        bot = WABot(request.json)
        return bot.processing()
```

Каждый раз, когда к нам приходит какой-либо POST запрос мы инициализируем бота, передав в него json данные и вызываем метод processing(). Тем самым бот может принимать и обрабатывать входящие сообщения.
