from flask import Flask, render_template
from app.service.generate import generate_account
import asyncio
import os
app = Flask(__name__)


@app.route('/')
def hello_world():

    return render_template('index.html',port=os.getenv('PORT'))


@app.route('/getAccount')
def get_account():
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    return asyncio.get_event_loop().run_until_complete(generate_account())


