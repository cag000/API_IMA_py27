import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property 
from flask import Flask, request
from flask_restplus import Api
import json,re,pymysql
from elasticsearch import Elasticsearch
from configparser import ConfigParser
from datetime import datetime
from dateutil import tz
from calendar import monthrange
from main_isa import isa
from main_ipdsc import ipdsc

__author__      = "Kenzila"
__contributor__ = "Syahrul Al-Rasyid"

app = Flask(__name__)
api = Api(app)

@app.route('/ipd/onlinenews')
def ipd_onlinenews():
    return ipdsc().ipdsc_onlinenews()

@app.route('/ipd/facebook')
def ipd_facebook():
    return ipdsc().ipdsc_facebook

@app.route('/ipd/twitter')
def ipd_twitter():
    return ipdsc().ipdsc_twitter()
    
@app.route('/akun/twitter')
def akun_twitter():
    conek = pymysql.connect(
        host    = parser.get('database','sc_bintaro_tw_host'),
        user    = parser.get('database','sc_bintaro_tw_user'),
        password    = parser.get('database','sc_bintaro_tw_pass'),
        db  = parser.get('database','sc_bintaro_tw_db'),
        charset = 'utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    jsons = {'ket':'twitter_from_SC'}
    cursor = conek.cursor()
    queri = "SELECT `user_id`,`name`,`screen_name`,`add_date` FROM `twitter_account_track` ORDER BY `twitter_account_track`.`screen_name` ASC"
    cursor.execute(queri)
    data = cursor.fetchall()
    da_list = []
    for a in data:
        date = a['add_date']
        da_list.append( {'user_id': a['user_id'],
                         'screen_name': a['screen_name'],
                         'name' : a['name'],
                         'add_date' : str(date)})
    jsons['list'] = da_list
    print da_list.__len__()
    result = json.dumps(jsons)
    return result

@app.route('/akun/facebook')
def akun_facebook():
    conek   = pymysql.connect(
        host    = parser.get('database','sc_ph_fb_host'),
        user    = parser.get('database','sc_ph_fb_user'),
        password    = parser.get('database','sc_ph_fb_pass'),
        db  = parser.get('database','sc_ph_fb_db'),
        charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor
    )
    jsons   = {'ket' : 'facebook_from_SC'}
    cursor  = conek.cursor()
    queri   = "SELECT `fb_id`,`name`,`add_date` FROM `facebook_page_track` ORDER BY `facebook_page_track`.`name` ASC"
    cursor.execute(queri)
    data    = cursor.fetchall()
    da_list = []
    for a in data:
        date = a['add_date']
        da_list.append({'user_id' : a['fb_id'],
                        'name'  : a['name'],
                        'add_date'  : str(date)})
    jsons['list'] = da_list
    print da_list.__len__()
    result = json.dumps(jsons)
    return result

@app.route('/isa/onlinenews')
def isa_onlinenews():
    return isa().isa_onlinenews()
    
@app.route('/isa/facebook')
def isa_facebook():
    return isa().isa_facebook()

@app.route('/isa/twitter')
def isa_twitter():
   return isa().isa_twitter()

@app.route('/isa/onlinenews/news_req')
def isa_onlinenews_news_req():
    return isa().isa_onlinenews_req()

@app.route('/testing')
def isa_testing():
   return "null"

if __name__ == '__main__':
    # app.run(host='192.168.20.92',port=5002)
    app.run(port=5002, debug=True)