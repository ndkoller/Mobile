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
import webapp2
import json

class Boat(ndb.Model):
    """Models an individual boat with id, name, type, length, at_seat ."""
    id = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    length = ndb.IntegerProperty(required=True)
    at_sea = ndb.BooleanProperty(required=True)

class Slip(ndb.Model):
    """Models a slip with id, number, current boat, arrival date, at_seat ."""
    id = ndb.StringProperty(required=True)
    number = ndb.IntegerProperty(required=True)
    """boat id"""
    current_boat = ndb.StringProperty()
    arrival_date = ndb.DateTimeProperty()
    """"departure_history":[{"departure_date":"11/4/2014","departed_boat":"123aaa"}...] 
    #Optional for 5% extra credit a list of the dates that previous boats departed the slip"""

class SlipHandler(webapp2.RequestHandler):
    def post(self):
        slip_data = json.loads(self.request.body)
        new_slip = Slip(id='',number=slip_data['number'],current_boat='',arrival_date=None)
        new_slip.put()
        slip_dict = new_slip.to_dict()
        slip_dict['self'] = '/Slip/' + new_slip.key.urlsafe() 
        slip_dict['id'] = new_slip.key.urlsafe()
        self.response.write(json.dumps(slip_dict))

    def get(self, id=None):
        if id:
            slip = ndb.Key(urlsafe=id).get();
            slip_d = slip.to_dict()
            slip_d['self'] = "/Slip/" + id
            self.response.write(json.dumps(slip_d))
            
    def patch(self, id=None):
        if id: 
            slip = ndb.Key(urlsafe=id).get();
            slip_d = slip.to_dict()
            slip_d['self'] = "/Slip/" + id
            self.response.write(json.dumps(slip_d))
    
    def put(self, id=None):
        if id:         
            slip = ndb.Key(urlsafe=id).get();
            slip_d = slip.to_dict()
            slip_d['self'] = "/Slip/" + id
            self.response.write(json.dumps(slip_d))
            
class BoatHandler(webapp2.RequestHandler):
    def post(self):
        boat_data = json.loads(self.request.body)
        new_boat = Boat(id='',name=boat_data['name'],type=boat_data['type'],length=boat_data['length'],at_sea=True)
        new_boat.put()
        boat_dict = new_boat.to_dict()
        boat_dict['self'] = '/Boat/' + new_boat.key.urlsafe() 
        boat_dict['id'] = new_boat.key.urlsafe()
        self.response.write(json.dumps(boat_dict))

    def get(self, id=None):
        if id:
            b = ndb.Key(urlsafe=id).get();
            b_d = b.to_dict()
            b_d['self'] = "/Boat/" + id
            self.response.write(json.dumps(b_d))
    
    def patch(self, id=None):
        if id:
            b = ndb.Key(urlsafe=id).get();
            b_d = b.to_dict()
            b_d['self'] = "/Boat/" + id
            self.response.write(json.dumps(b_d))
            
    def put(self, id=None):
        if id:
            b = ndb.Key(urlsafe=id).get();
            b_d = b.to_dict()
            b_d['self'] = "/Boat/" + id
            self.response.write(json.dumps(b_d))
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Working")

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Boat',BoatHandler),
    ('/Boat/(.*)',BoatHandler),
    ('/Slip',SlipHandler),
    ('/Slip/(.*)',SlipHandler)
], debug=True)
