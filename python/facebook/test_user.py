#!/usr/bin/env python
#-*- coding:utf8 -*-
"""
    create test account for facebook
    ~~~~~~~~~~~~~~~~~~
        
    :author: tell-k
    :copyright: tell-k. All Rights Reserved.
    :ref: http://developers.facebook.com/docs/test_users/
    :ref: http://facebook-docs.oklahome.net/archives/51976670.html
    :tool: http://www.koikikukan.com/tools/facebook/TestUsers/
""" 

import urllib
import cgi
import simplejson
import StringIO
from pit import Pit
from pprint import pprint

#set your app_id, CONSUMER_SECRET
conf = Pit.get('fb')
APP_ID = conf['app_id']
CONSUMER_SECRET = conf['consumer_secret']

#num of test user
TEST_USER_NUM = 50

def get_app_access_token(app_id, consumer_secret):
    """ 登録Facebookアプリ自体のアクセストークンを取得 """
    url = "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(dict(
        client_id=app_id,
        client_secret=consumer_secret,
        grant_type="client_credentials",
    ))
    response = cgi.parse_qs(urllib.urlopen(url).read())
    access_token = response["access_token"][-1]
    return access_token

def _create(app_id, app_token, installed, name):
    """ test user の取得"""
    base_url = "https://graph.facebook.com/" + app_id + "/accounts/test-users?"
    url = base_url + urllib.urlencode(dict(
                                installed=installed,
                                name=name,
                                method='post',
                                permissions='read_stream',
                                access_token=app_token,
                                ))
    res = urllib.urlopen(url).read() 
    return simplejson.load(StringIO.StringIO(res))

def get_all(app_id, app_token):
    """ test user の取得"""
    base_url = "https://graph.facebook.com/" + app_id + "/accounts/test-users?"
    url = base_url + urllib.urlencode(dict(
                                access_token=app_token,
                                ))
    res = urllib.urlopen(url).read() 
    return simplejson.load(StringIO.StringIO(res))

def get_user(user_id, app_token):
    """ test user の取得"""
    base_url = "https://graph.facebook.com/%s?"
    url = (base_url % user_id) + urllib.urlencode(dict(access_token=app_token))
    res = urllib.urlopen(url).read() 
    return simplejson.load(StringIO.StringIO(res))

def _make_friends(user_id, friend_id, access_token):
    base_url = "https://graph.facebook.com/%s/friends/%s?method=post&"
    url = (base_url % (user_id, friend_id)) + urllib.urlencode(dict(access_token=access_token))
    res = urllib.urlopen(url).read() 
    return simplejson.load(StringIO.StringIO(res))

def create(app_id, app_token, installed, name_prefix, user_num, test_users):
    for i in range(user_num):
        test_user = _create(APP_ID, app_token, installed, name_prefix + str(i))
        if not test_user:
            continue
        print 'create test user => ' + str(test_user)
        test_users.append(test_user)

def make_friends(test_users):
    friends = test_users[:]
    for user in test_users:
        for friend in friends:
            if user['id'] != friend['id']:
                print 'id:%s friend request to id:%s' % (user['id'], friend['id'])
                _make_friends(user['id'], friend['id'], user['access_token'])

if __name__ == '__main__':
    app_token = get_app_access_token(APP_ID, CONSUMER_SECRET)
    test_users = []
#    create(APP_ID, app_token, 'true', 'bucho_', TEST_USER_NUM, test_users)
#    make_friends(test_users)
    pprint(get_all(APP_ID, app_token))
