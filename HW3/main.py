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
from google.appengine.api import urlfetch

url_app_2 = 'https://homework3-166620.appspot.com/oauth'
url_app_3 = 'https://www.googleapis.com/oauth2/v4/token'


class MainPage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html') 
        self.response.out.write(template.render(path, {}))        

class Guestbook(webapp2.RequestHandler):
    def post(self): #didn't change this
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')

class OauthHandler(webapp2.RequestHandler):
    def get(self):
        state=self.request.get("state")
        authorizationCode=self.request.get("code")

        self.response.write('The secret state is: '+state+'\n')
        self.response.write(authorizationCode)
        # data_to_post = {
            # 'message': repr(self.request.GET)
        # }
        # encoded_data = urllib.urlencode(data_to_post)
        # # Send encoded data to application-2
        # result = urlfetch.fetch(url_app_3, payload=encoded_data, method=urlfetch.POST)
    def post(self):
        code = self.request.get("code")
        data_to_post = {
          'code': code,
          'client_id': '241975773079-8im8k4jqvnusoqag4g2ocs1pvrf3u34b.apps.googleusercontent.com',
          'client_secret': '9imJ7fAOpdlWEQ6YkHuD7PSj',
          'redirect_uri': 'https://homework3-166620.appspot.com/oauth',
          'grant_type': 'authorization_code'
        }
        encoded_data = urllib.urlencode(data_to_post)
        # Send encoded application-2 response to application-3
        headers={'Content-Type':'application/x-www-form-urlencoded'}
        result = urlfetch.fetch(url_app_3, headers=headers, payload=encoded_data, method=urlfetch.POST)

        # Output response of application-3 to screen

        self.response.write(result.content)
        path = os.path.join(os.path.dirname(__file__), 'result.html') 
        self.response.out.write(template.render(path, {}))
        # logging.debug('The Contents of the GET request are:' + )
        
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/oauth',OauthHandler),
    ('/sign', Guestbook),
], debug=True)
