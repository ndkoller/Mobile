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
    arrival_date = ndb.StringProperty()
    """"departure_history":[{"departure_date":"11/4/2014","departed_boat":"123aaa"}...] 
    #Optional for 5% extra credit a list of the dates that previous boats departed the slip"""

class Arrival(ndb.Model):
    sid = ndb.StringProperty()
    bid = ndb.StringProperty()
    arrival_date = ndb.StringProperty()

class Departure(ndb.Model):
    sid = ndb.StringProperty()
    bid = ndb.StringProperty()


class ArrivalHandler(webapp2.RequestHandler):
    def put(self,bid=None,sid=None):
        """Boat Arrival"""
        """if bid and sid:"""
        try:
            slip_data = json.loads(self.request.body)
            boat = ndb.Key(urlsafe=bid).get()
            slip = ndb.Key(urlsafe=sid).get()
            if slip_data['arrival_date']:
                slip.arrival_date = slip_data['arrival_date']
            slip_qry = Slip.query().filter(Slip.id == sid).fetch()
            slip_dict = [a.to_dict() for a in slip_qry]
            curr_boat = slip_dict[0]
            if curr_boat['current_boat'] != "":
                self.response.set_status(403)
                return
            boat_dict = boat.to_dict()
            slip_dict = slip.to_dict()
            boat_dict['at_sea'] = False
            slip_dict['current_boat'] = '/Boat/' + bid
            boat.at_sea = False
            boat.put()
            slip.current_boat = '/Boat/' + bid
            slip.put()
            self.response.write(json.dumps(boat_dict))
            self.response.write(json.dumps(slip_dict))
        except:
            self.response.set_status(403)
        
        

class DepartureHandler(webapp2.RequestHandler):
    def put(self,bid=None,sid=None):
        """Boat Departure"""
        """if bid and sid:"""
        boat = ndb.Key(urlsafe=bid).get()
        slip = ndb.Key(urlsafe=sid).get()
        boat_dict = boat.to_dict()
        slip_dict = slip.to_dict()
        boat_dict['at_sea'] = True
        slip_dict['current_boat'] = None
        boat.at_sea = True
        boat.put()
        slip.current_boat = None
        slip.put()
        self.response.write(json.dumps(boat_dict))
        self.response.write(json.dumps(slip_dict))
        
    
class SlipHandler(webapp2.RequestHandler):
    def post(self):
        try:
            slip_data = json.loads(self.request.body)
            new_slip = Slip(id='',number=slip_data['number'],current_boat='',arrival_date=None)
            new_slip.put()
            new_slip.id = new_slip.key.urlsafe()
            new_slip.put()
            slip_dict = new_slip.to_dict()
            slip_dict['self'] = '/Slip/' + new_slip.key.urlsafe() 
            self.response.write(json.dumps(slip_dict))
        except:
            self.response.set_status(403)
        
    def get(self, id=None):
        if id:
            slip = ndb.Key(urlsafe=id).get()
            if slip:
                slip_d = slip.to_dict()
                slip_d['self'] = "/Slip/" + id
                self.response.write(json.dumps(slip_d))
            else:
                self.response.set_status(403)

    def delete(self, id=None):
        if id:
            slip_qry = Slip.query().filter(Slip.id == id).fetch()
            slip_dict = [a.to_dict() for a in slip_qry]
            curr_boat = slip_dict[0]
            if curr_boat['current_boat']:
                empty, extra, curr_boat_id = curr_boat['current_boat'].split('/')
                boat = ndb.Key(urlsafe=curr_boat_id).get()
                if boat:
                    boat.at_sea = True
                    boat.put()
            ndb.Key(urlsafe=id).delete();
            self.response.set_status(204)
    
    def patch(self, id=None):
        if id: 
            try:
                slip_data = json.loads(self.request.body)
                slip = ndb.Key(urlsafe=id).get()
                slip_dict = slip.to_dict()
                if slip_dict['number'] != slip_data['number']:
                    slip.number = slip_data['number']
                    slip.put()
                if slip_dict['current_boat'] != slip_data['current_boat']:
                    slip.current_boat = slip_data['current_boat']
                    slip.put()
                if slip_dict['arrival_date'] != slip_data['arrival_date']:
                    slip.arrival_date = slip_data['arrival_date']
                    slip.put()
                slip_dict = slip.to_dict()
                slip_dict['self'] = "/Slip/" + id
                self.response.write(json.dumps(slip_dict))
            except:
                    self.response.set_status(403)
    
    def put(self, id=None):
        if id:
            try:
                slip_data = json.loads(self.request.body)
                new_slip = Slip(id=id,number=slip_data['number'],current_boat='',arrival_date=None)
                new_slip.put()
                slip_dict = new_slip.to_dict()
                slip_dict['self'] = '/Slip/' + id 
                self.response.write(json.dumps(slip_dict))
            except:
                self.response.set_status(403)
            
class BoatHandler(webapp2.RequestHandler):
    def post(self):
        try:
            boat_data = json.loads(self.request.body)
            new_boat = Boat(id='',name=boat_data['name'],type=boat_data['type'],length=boat_data['length'],at_sea=True)
            new_boat.put()
            new_boat.id = new_boat.key.urlsafe()
            new_boat.put()
            boat_dict = new_boat.to_dict()
            boat_dict['self'] = '/Boat/' + new_boat.key.urlsafe() 
            self.response.write(json.dumps(boat_dict))
        except:
            self.response.set_status(403)
            
    def get(self, id=None):
        if id:
            b = ndb.Key(urlsafe=id).get();
            if b:
                b_d = b.to_dict()
                b_d['self'] = "/Boat/" + id
                self.response.write(json.dumps(b_d))
            else:
                self.response.set_status(403)
  
    def delete(self, id=None):
        if id:
            slip_qry = Slip.query().filter(Slip.current_boat == id).fetch()
            if slip_qry:
                slip_dict = [a.to_dict() for a in slip_qry]
                curr_boat = slip_dict[0]
                if curr_boat['current_boat']:
                    slip = ndb.Key(urlsafe=curr_boat['id']).get()
                    if slip:
                        slip.current_boat = None
                        slip.put()
            ndb.Key(urlsafe=id).delete();
            self.response.set_status(204) 
 
    def patch(self, id=None):
        if id:
            try:
                boat_data = json.loads(self.request.body)
                boat = ndb.Key(urlsafe=id).get()
                boat_dict = boat.to_dict()
                if boat_dict['name'] != boat_data['name']:
                    boat.name = boat_data['name']
                    boat.put()
                if boat_dict['type'] != boat_data['type']:
                    boat.type = boat_data['type']
                    boat.put()
                if boat_dict['length'] != boat_data['length']:
                    boat.length = boat_data['length']
                    boat.put()
                boat_dict = boat.to_dict()
                boat_dict['self'] = "/Boat/" + id
                self.response.write(json.dumps(boat_dict))
            except:
                self.response.set_status(403)
    
    def put(self, id=None):
        if id:
            boat_data = json.loads(self.request.body)
            new_boat = Boat(id=id,name=boat_data['name'],type=boat_data['type'],length=boat_data['length'],at_sea=True)
            new_boat.put()
            boat_dict = new_boat.to_dict()
            boat_dict['self'] = "/Boat/" + id
            self.response.write(json.dumps(boat_dict))
   
class BoatViewHandler(webapp2.RequestHandler):
    def get(self):
        qry = Boat.query().fetch(limit=None)
        self.response.write(json.dumps([p.to_dict() for p in qry])) 

class SlipViewHandler(webapp2.RequestHandler):
    def get(self):
        qry = Slip.query().fetch(limit=None)
        self.response.write(json.dumps([p.to_dict() for p in qry])) 
        
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
    ('/Slip/(.*)',SlipHandler),
    ('/Arrival',ArrivalHandler),
    ('/Arrival/(.*)/(.*)',ArrivalHandler),
    ('/Departure',DepartureHandler),
    ('/Departure/(.*)/(.*)',DepartureHandler),
    ('/ViewBoats/',BoatViewHandler),
    ('/ViewSlips/',SlipViewHandler)
], debug=True)
