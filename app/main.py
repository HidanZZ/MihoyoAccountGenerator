import logging
import threading

from flask import Flask, render_template
from app.service.generate import generate_account,test
import asyncio
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', port=5000)


@app.route('/getAccount', methods=['GET'])
def get_account():
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    return asyncio.get_event_loop().run_until_complete(generate_account())


@app.route('/test', methods=['GET'])
def t():
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    return asyncio.get_event_loop().run_until_complete(test())
