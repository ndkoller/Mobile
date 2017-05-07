#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template #also added
import logging
import webapp2
import json
import os #added
import urllib
import urllib2
from google.appengine.api import urlfetch

REDIRECT_URI = 'https://homework3-166620.appspot.com/oauth'
LOGIN_URI = 'https://accounts.google.com/o/oauth2/v2/auth'
url_app_3 = 'https://www.googleapis.com/oauth2/v4/token'
CLIENT_ID = '13754932464-urc4rdrkndi7306ckncm8jffmcp41stg.apps.googleusercontent.com'
CLIENT_SECRET = 'bwr2MNDmp7EmOLC646L-yyJw'
STATE = 'MyBigSecret123'

class MainPage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html') 
        self.response.out.write(template.render(path, {}))    

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        
        url = 'https://accounts.google.com/o/oauth2/auth'
        values = {
            'response_type':'code',
            'state': STATE,
            'client_id':CLIENT_ID,
            'redirect_uri':REDIRECT_URI,
            'scope':'email',
            'access_type':'offline',
            'validate_certificate': 'true'
        }
        data = urllib.urlencode(values)
        address = url + '?' + data
        self.redirect(address)
        
class OauthHandler(webapp2.RequestHandler):
    def get(self):
        state=self.request.get("state")
        code=self.request.get("code")
        #POST to use authorizationCode to get access token
        data_to_post = {
          'code': code,
          'client_id': CLIENT_ID,
          'client_secret': CLIENT_SECRET,
          'redirect_uri': REDIRECT_URI,
          'grant_type': 'authorization_code'
        }
        encoded_data = urllib.urlencode(data_to_post)
        # Send encoded application-2 response to application-3
        headers={'Content-Type':'application/x-www-form-urlencoded'}
        result = urlfetch.fetch(url_app_3, headers=headers, payload=encoded_data, method=urlfetch.POST)
        json_result=json.loads(result.content)
        accessToken=json_result['access_token']
        token_type=json_result['token_type']
        # Output response of application-3 to screen
        
        url='https://www.googleapis.com/plus/v1/people/me'
        values = {
            'Authorization': token_type +' '+accessToken
        }
        data = urllib.urlencode(values)
        address = url + '?' + data
        final_result=urllib2.urlopen(address).read()
        parse_result=json.loads(final_result.content)
        self.response.write(parse_result)
        
        path = os.path.join(os.path.dirname(__file__), 'result.html') 
        self.response.out.write(template.render(path, {}))
        self.response.write(result.content)
        self.response.write(parse_result)
        # logging.debug('The Contents of the GET request are:' + )
        
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/oauth',OauthHandler),
    ('/login',LoginHandler)
], debug=True)