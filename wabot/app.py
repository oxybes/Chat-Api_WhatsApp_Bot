from flask import Flask, request, jsonify
from wabot import WABot
import json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        bot = WABot(request.json)
        return bot.processing()


    if request.method == 'GET':
        return 'get kek'

if(__name__) == '__main__':
    app.run()