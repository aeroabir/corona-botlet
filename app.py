#!/usr/bin/env python

import csv
import difflib
import datetime
from difflib import SequenceMatcher
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
from flask import Flask
from flask import request
from flask import make_response
import json
import operator
import os
import random
import requests
import time
import urllib
# from flask_sqlalchemy import SQLAlchemy

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # res1 = {
    #     "speech": "aaa",
    #     "displayText": "aaa",
    #     "data": "aaa",
    #     "contextOut": "aaa",
    #     "source": "apiai-choicehotel-queries"
    # }
    # r = make_response(res1)
    # print("Request:")
    # print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)

    r.headers['Content-Type'] = 'application/json'
    return r


def get_overall_counts():
    count = dict()
    for d in jdata['raw_data']:
        if d['currentstatus'] not in count:
            count[d['currentstatus']] = 0
        count[d['currentstatus']] += 1
    return count


def get_state_counts(state='Kerala'):
    count = dict()
    for d in jdata['raw_data']:
        if d['detectedstate'] == state:
            if d['currentstatus'] not in count:
                count[d['currentstatus']] = 0
            count[d['currentstatus']] += 1
    return count


def makeWebhookResult(req):

    # get string matching scores
    # def get_matching_scores(t1, t2):
    #     r1 = fuzz.ratio(t1, t2)
    #     r2 = fuzz.partial_ratio(t1, t2)
    #     r3 = fuzz.token_set_ratio(t1, t2)
    #     return max(r1, r2, r3)

    property_details = {
    'txc78': {'property_details': {'status': 'OK', 'hotel': {'status': 'ACTIVE', 'amenityGroups': [{'description': 'Meeting Space', 'id': 'MEET'}, {'description': 'Fitness Center', 'id': 'EXRM'}, {'description': 'Laundry, Guest', 'id': 'LNDR'}, {'description': 'Free WiFi', 'id': 'HIGH'}, {'description': 'Business Center', 'id': 'BUSC'}, {'description': 'Continental Breakfast', 'id': 'COFP'}, {'description': 'Smoke Free', 'id': 'NSKH'}], 'brandCode': 'SL', 'lat': '29.794360', 'name': 'Sleep Inn & Suites Near Downtown North', 'productCode': 'AS', 'productName': 'Inn & Suites', 'id': 'TXC78', 'coOpParticipant': False, 'brandName': 'Sleep', 'amenities': [{'description': 'Convenience Store', 'distanceDescription': 'Nearby', 'business': False, 'code': 'MART', 'distanceValue': 1.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'Meeting Room', 'distanceDescription': 'Onsite', 'business': True, 'code': 'MEET', 'distanceValue': 0.0, 'charge': True}, {'description': 'Car Rental Service', 'distanceDescription': 'Nearby', 'business': True, 'code': 'CARR', 'distanceValue': 9.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'Designed to Dream Property', 'distanceDescription': 'Onsite', 'business': False, 'code': 'DSTD', 'distanceValue': 0.0, 'charge': False, 'longDescription': "Sleep Inn is getting even better. This hotel, as part of a nationwide refresh of the Sleep Inn brand, has incorporated stylish design features and amenities to create a unique atmosphere that will help you have a restful stay. Experience 'better' for yourself at this Sleep Inn hotel."}, {'description': 'Fishing', 'distanceDescription': 'Nearby', 'business': False, 'code': 'FISH', 'distanceValue': 10.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'Convention Center', 'distanceDescription': 'Nearby', 'business': True, 'code': 'CONV', 'distanceValue': 5.0, 'charge': False, 'distanceUnit': 'Miles'}, {'description': 'Outdoor Parking', 'distanceDescription': 'Onsite', 'business': False, 'code': 'PRKO', 'distanceValue': 0.0, 'charge': False}, {'description': 'Shopping', 'distanceDescription': 'Nearby', 'business': False, 'code': 'MALL', 'distanceValue': 2.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'Free Continental Breakfast', 'distanceDescription': 'Onsite', 'business': False, 'code': 'CONT', 'distanceValue': 0.0, 'charge': False}, {'description': 'Interior Corridors', 'distanceDescription': 'Onsite', 'business': False, 'code': 'CORI', 'distanceValue': 0.0, 'charge': False}, {'description': 'Free Newspaper Mon-Fri', 'distanceDescription': 'Onsite', 'business': True, 'code': 'NEWP', 'distanceValue': 0.0, 'charge': False}, {'description': 'Guest Use Copy Machine', 'distanceDescription': 'Onsite', 'business': True, 'code': 'COPY', 'distanceValue': 0.0, 'charge': True}, {'description': 'Elevator(s)', 'distanceDescription': 'Onsite', 'business': False, 'code': 'ELEV', 'distanceValue': 0.0, 'charge': False}, {'description': 'Beauty Shop', 'distanceDescription': 'Nearby', 'business': False, 'code': 'BEAU', 'distanceValue': 2.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'Beach Access', 'distanceDescription': 'Nearby', 'business': False, 'code': 'BCH', 'distanceValue': 50.0, 'charge': False, 'distanceUnit': 'Miles'}, {'description': 'Driving Range', 'distanceDescription': 'Nearby', 'business': False, 'code': 'GLFD', 'distanceValue': 5.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'Government Travelers: FEMA Approved', 'distanceDescription': 'Onsite', 'business': False, 'code': 'FEMA', 'distanceValue': 0.0, 'charge': False}, {'description': '100% Smoke Free Hotel', 'distanceDescription': 'Onsite', 'business': False, 'code': 'NSKH', 'distanceValue': 0.0, 'charge': False}, {'description': 'Valet Cleaning Service', 'distanceDescription': 'Onsite', 'business': True, 'code': 'VLSV', 'distanceValue': 0.0, 'charge': True}, {'description': 'Barber Shop', 'distanceDescription': 'Nearby', 'business': False, 'code': 'BARB', 'distanceValue': 2.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'No Pets Allowed', 'distanceDescription': 'Onsite', 'business': False, 'code': 'NPET', 'distanceValue': 0.0, 'charge': False}, {'description': 'Bus Parking', 'distanceDescription': 'Onsite', 'business': False, 'code': 'PRKB', 'distanceValue': 0.0, 'charge': False}, {'description': 'Bowling', 'distanceDescription': 'Nearby', 'business': False, 'code': 'BOWL', 'distanceValue': 3.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'Free WiFi', 'distanceDescription': 'Onsite', 'business': True, 'code': 'FWHI', 'distanceValue': 0.0, 'charge': False}, {'description': 'Golf Course', 'distanceDescription': 'Nearby', 'business': False, 'code': 'GOLF', 'distanceValue': 5.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'Airline Ticket Desk', 'distanceDescription': 'Nearby', 'business': True, 'code': 'AIRD', 'distanceValue': 9.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'Business Center', 'distanceDescription': 'Onsite', 'business': True, 'code': 'BUSC', 'distanceValue': 0.0, 'charge': False}, {'description': 'Miniature Golf', 'distanceDescription': 'Nearby', 'business': False, 'code': 'MINI', 'distanceValue': 6.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'Billiard Room', 'distanceDescription': 'Nearby', 'business': False, 'code': 'BILL', 'distanceValue': 2.0, 'charge': True, 'distanceUnit': 'Miles'}, {'description': 'Banquet Rooms', 'distanceDescription': 'Onsite', 'business': True, 'code': 'BAQT', 'distanceValue': 0.0, 'charge': True}, {'description': 'Exercise Room', 'distanceDescription': 'Onsite', 'business': True, 'code': 'EXRM', 'distanceValue': 0.0, 'charge': False}, {'description': 'Guest Use Fax Machine', 'distanceDescription': 'Onsite', 'business': True, 'code': 'FAXX', 'distanceValue': 0.0, 'charge': True}, {'description': 'Lake', 'distanceDescription': 'Nearby', 'business': False, 'code': 'LAKE', 'distanceValue': 10.0, 'charge': False, 'distanceUnit': 'Miles'}, {'description': 'Guest Laundry', 'distanceDescription': 'Onsite', 'business': False, 'code': 'LNDR', 'distanceValue': 0.0, 'charge': True}, {'description': 'Basketball', 'distanceDescription': 'Nearby', 'business': False, 'code': 'BSKT', 'distanceValue': 3.0, 'charge': False, 'distanceUnit': 'Miles'}, {'description': 'Putting Green', 'distanceDescription': 'Nearby', 'business': False, 'code': 'PUTG', 'distanceValue': 5.0, 'charge': True, 'distanceUnit': 'Miles'}], 'taxInclusive': False, 'lon': '-95.372278', 'description': 'Dream better at our Designed to Dream Sleep Inn and Suites Near Downtown North in Houston, TX. Enjoy a convenient location to the Houston Toyota Center, Minute Maid Park, Memorial Park, the Galleria Mall and te George Brown Convention Center. Our hotel also offers a free continental breakfast, free WiFi, free parking and an exercise room. Enjoy one of our guest rooms, all of which are inspired by nature to help you relax. Each room comes equipped with a hair dryer, coffee maker, iron and ironing board and refrigerator. Start earning rewards points with your next stay when you sign up for our Choice Privileges program.', 'address': {'line1': '2475 North Freeway', 'country': 'US', 'subdivision': 'TX', 'postalCode': '77009', 'city': 'Houston'}, 'phone': '(713) 862-6300'}}, 'property_address': {'address': '2475 North Freeway,Houston,77009,TX,US', 'id': 'TXC78', 'name': 'Sleep Inn & Suites Near Downtown North', 'city': 'houston'}},
    'tx933': {'property_details': {'status': 'OK', 'hotel': {'status': 'ACTIVE', 'amenityGroups': [{'description': 'Fitness Center', 'id': 'EXRM'}, {'description': 'Laundry, Guest', 'id': 'LNDR'}, {'description': 'Free WiFi', 'id': 'HIGH'}, {'description': 'Truck Parking', 'id': 'PRKT'}, {'description': 'Outdoor Pool', 'id': 'POUT'}, {'description': 'Business Center', 'id': 'BUSC'}, {'description': 'Smoke Free', 'id': 'NSKH'}, {'description': 'Continental Breakfast', 'id': 'COFP'}], 'brandCode': 'MS', 'lat': '29.700203', 'name': 'MainStay Suites Texas Medical Center/Reliant Park', 'productCode': 'SU', 'productName': 'Suites', 'id': 'TX933', 'coOpParticipant': True, 'brandName': 'MainStay', 'amenities': [{'description': 'Computer w/ Internet', 'distanceDescription': 'Onsite', 'business': True, 'code': 'INET', 'distanceValue': 0.0, 'charge': False}, {'description': 'DVD Disk Rental', 'distanceDescription': 'Onsite', 'business': False, 'code': 'DVDR', 'distanceValue': 0.0, 'charge': True}, {'description': 'Outdoor Parking', 'distanceDescription': 'Onsite', 'business': False, 'code': 'PRKO', 'distanceValue': 0.0, 'charge': False}, {'description': 'Interior Corridors', 'distanceDescription': 'Onsite', 'business': False, 'code': 'CORI', 'distanceValue': 0.0, 'charge': False}, {'description': 'Guest Use Copy Machine', 'distanceDescription': 'Onsite', 'business': True, 'code': 'COPY', 'distanceValue': 0.0, 'charge': True}, {'description': 'Windows Open', 'distanceDescription': 'Onsite', 'business': False, 'code': 'OPEN', 'distanceValue': 0.0, 'charge': False}, {'description': 'Well-lit Area, In-Room', 'distanceDescription': 'Onsite', 'business': True, 'code': 'LITE', 'distanceValue': 0.0, 'charge': False}, {'description': 'Government Travelers: FEMA Approved', 'distanceDescription': 'Onsite', 'business': False, 'code': 'FEMA', 'distanceValue': 0.0, 'charge': False}, {'description': 'Airport Shuttle (Charge)', 'distanceDescription': 'Onsite', 'business': False, 'code': 'AIRS', 'distanceValue': 0.0, 'charge': True}, {'description': '100% Smoke Free Hotel', 'distanceDescription': 'Onsite', 'business': False, 'code': 'NSKH', 'distanceValue': 0.0, 'charge': False}, {'description': 'Valet Cleaning Service', 'distanceDescription': 'Onsite', 'business': True, 'code': 'VLSV', 'distanceValue': 0.0, 'charge': True}, {'description': 'Hotel accessible to individuals with disabilities', 'distanceDescription': 'Onsite', 'business': False, 'code': 'ACBL', 'distanceValue': 0.0, 'charge': False}, {'description': 'Convenience Store', 'distanceDescription': 'Onsite', 'business': False, 'code': 'MART', 'distanceValue': 0.0, 'charge': True}, {'description': 'Bus Parking', 'distanceDescription': 'Onsite', 'business': False, 'code': 'PRKB', 'distanceValue': 0.0, 'charge': False}, {'description': 'Outdoor Pool', 'distanceDescription': 'Onsite', 'business': False, 'code': 'POUT', 'distanceValue': 0.0, 'charge': False}, {'description': 'Gift Shop', 'distanceDescription': 'Onsite', 'business': False, 'code': 'SHGF', 'distanceValue': 0.0, 'charge': True}, {'description': 'Guest Use Fax Machine', 'distanceDescription': 'Onsite', 'business': True, 'code': 'FAXX', 'distanceValue': 0.0, 'charge': True}, {'description': 'Guest Laundry', 'distanceDescription': 'Onsite', 'business': False, 'code': 'LNDR', 'distanceValue': 0.0, 'charge': True}, {'description': 'First-aid staff/24hr', 'distanceDescription': 'Onsite', 'business': False, 'code': 'AIDE', 'distanceValue': 0.0, 'charge': False}, {'description': 'No Pets Allowed', 'distanceDescription': 'Onsite', 'business': False, 'code': 'NPET', 'distanceValue': 0.0, 'charge': False}, {'description': 'Free WiFi', 'distanceDescription': 'Onsite', 'business': True, 'code': 'FWHI', 'distanceValue': 0.0, 'charge': False}, {'description': 'Truck Parking', 'distanceDescription': 'Onsite', 'business': False, 'code': 'PRKT', 'distanceValue': 0.0, 'charge': False}, {'description': 'Free Deluxe Continental Breakfast', 'distanceDescription': 'Onsite', 'business': False, 'code': 'DLUX', 'distanceValue': 0.0, 'charge': False}, {'description': 'Business Center', 'distanceDescription': 'Onsite', 'business': True, 'code': 'BUSC', 'distanceValue': 0.0, 'charge': False}, {'description': 'Exercise Room', 'distanceDescription': 'Onsite', 'business': True, 'code': 'EXRM', 'distanceValue': 0.0, 'charge': False}, {'description': 'Braille Elevator(s)', 'distanceDescription': 'Onsite', 'business': False, 'code': 'HDBR', 'distanceValue': 0.0, 'charge': False}], 'taxInclusive': False, 'lon': '-95.378115', 'description': 'Enjoy a longer stay away from home at our Mainstay Suites Texas Medical Center/Reliant Park hotel in Houston, TX near Texas Medical Center. Our hotel is near George R. Brown Convention Center, the Houston Museum of Natural Science and Museum of Fine Arts. Enjoy amenities like free breakfast, free WiFi, a fitness center, an outdoor heated pool and more. Rooms include kitchen facilities, a flat-screen TV, hair dryer, iron and ironing board. Also, earn rewards including free nights and gift cards with our Choice Privileges Rewards program. \n\nShuttle service to Texas Medical Center and 3 mile radius including Lakewood church. Monday - Friday 7:00 am - 9:00 pm and Saturday & Sunday 9:00 am - 5:00 pm. Airport shuttle to/from William P. Hobby airport available for nominal fee. Shuttle hours are 7:00 am - 9:00 pm, weekdays. From 9 am. - 3 pm on weekends. Shuttle runs every two hours. Cash paying guests are required to post a 150.00USD deposit at check-in.', 'address': {'line1': '3134 Old Spanish Trail', 'country': 'US', 'subdivision': 'TX', 'postalCode': '77054', 'city': 'Houston'}, 'phone': '(832) 201-3131'}}, 'property_address': {'address': '3134 Old Spanish Trail,Houston,77054,TX,US', 'id': 'TX933', 'name': 'MainStay Suites Texas Medical Center/Reliant Park', 'city': 'houston'}},
    'ma074': {'property_address': {'address': '1186 Worcester Rd.,Framingham,01701,MA,US', 'city': 'boston', 'name': 'Econo Lodge', 'id': 'MA074'}, 'property_details': {'status': 'OK', 'hotel': {'lon': '-71.445728', 'amenities': [{'code': 'PRKO', 'business': False, 'distanceValue': 0.0, 'description': 'Outdoor Parking', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'OPEN', 'business': False, 'distanceValue': 0.0, 'description': 'Windows Open', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'LNGE', 'business': False, 'distanceValue': 0.0, 'description': 'Lounge/Bar', 'charge': True, 'distanceDescription': 'Onsite'}, {'code': 'LITE', 'business': True, 'distanceValue': 0.0, 'description': 'Well-lit Area, In-Room', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'LATE', 'business': True, 'distanceValue': 0.0, 'description': 'Late Check-Out Available', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'FEMA', 'business': False, 'distanceValue': 0.0, 'description': 'Government Travelers: FEMA Approved', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'COFE', 'business': False, 'distanceValue': 0.0, 'description': 'Free Coffee', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'GOLF', 'business': False, 'distanceValue': 0.5, 'description': 'Golf Course', 'distanceUnit': 'Miles', 'charge': True, 'distanceDescription': 'Nearby'}, {'code': 'NPET', 'business': False, 'distanceValue': 0.0, 'description': 'No Pets Allowed', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'FWHI', 'business': True, 'distanceValue': 0.0, 'description': 'Free WiFi', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'FAXX', 'business': True, 'distanceValue': 0.0, 'description': 'Guest Use Fax Machine', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'CORX', 'business': False, 'distanceValue': 0.0, 'description': 'Exterior Corridors', 'charge': False, 'distanceDescription': 'Onsite'}], 'brandName': 'Econo Lodge', 'taxInclusive': False, 'status': 'ACTIVE', 'name': 'Econo Lodge', 'coOpParticipant': True, 'productName': 'Lodge', 'amenityGroups': [{'id': 'HIGH', 'description': 'Free WiFi'}], 'id': 'MA074', 'description': 'The Econo Lodge hotel in Framingham, MA is an easy stop on the road. Our hotel is near several colleges throughout the area, such as Boston College, Harvard University, Boston University, Brandeis University and Wellesley College. Amenities include free WiFi, free coffee, outdoor parking and fax services. Guest rooms include modern bedding, TVs and more. We also offer membership to the Choice Privileges Program, which gives members the opportunity to earn valuable rewards points toward airline miles, gift cards and free hotel room nights. Must have 1 adult 21 years or older in each room.', 'lat': '42.298625', 'productCode': 'LO', 'address': {'line1': '1186 Worcester Rd.', 'subdivision': 'MA', 'city': 'Framingham', 'postalCode': '01701', 'country': 'US'}, 'brandCode': 'EL', 'phone': '(508) 879-1510'}}},
    'ma012': {'property_address': {'address': '1005 Belmont Street,Brockton,02301,MA,US', 'city': 'boston', 'name': 'Rodeway Inn', 'id': 'MA012'}, 'property_details': {'status': 'OK', 'hotel': {'lon': '-71.058029', 'amenities': [{'code': 'MART', 'business': False, 'distanceValue': 1.0, 'description': 'Convenience Store', 'distanceUnit': 'Miles', 'charge': True, 'distanceDescription': 'Nearby'}, {'code': 'GOLF', 'business': False, 'distanceValue': 2.0, 'description': 'Golf Course', 'distanceUnit': 'Miles', 'charge': True, 'distanceDescription': 'Nearby'}, {'code': 'COPY', 'business': True, 'distanceValue': 0.0, 'description': 'Guest Use Copy Machine', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'PRKO', 'business': False, 'distanceValue': 0.0, 'description': 'Outdoor Parking', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'CORI', 'business': False, 'distanceValue': 0.0, 'description': 'Interior Corridors', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'OPEN', 'business': False, 'distanceValue': 0.0, 'description': 'Windows Open', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'GLFD', 'business': False, 'distanceValue': 5.0, 'description': 'Driving Range', 'distanceUnit': 'Miles', 'charge': True, 'distanceDescription': 'Nearby'}, {'code': 'FEMA', 'business': False, 'distanceValue': 0.0, 'description': 'Government Travelers: FEMA Approved', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'NSKH', 'business': False, 'distanceValue': 0.0, 'description': '100% Smoke Free Hotel', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'PRKB', 'business': False, 'distanceValue': 0.0, 'description': 'Bus Parking', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'MINI', 'business': False, 'distanceValue': 5.0, 'description': 'Miniature Golf', 'distanceUnit': 'Miles', 'charge': True, 'distanceDescription': 'Nearby'}, {'code': 'FWHI', 'business': True, 'distanceValue': 0.0, 'description': 'Free WiFi', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'PRKT', 'business': False, 'distanceValue': 0.0, 'description': 'Truck Parking', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'HOTB', 'business': False, 'distanceValue': 0.0, 'description': 'Free Hot Breakfast', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'FAXX', 'business': True, 'distanceValue': 0.0, 'description': 'Guest Use Fax Machine', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'MAIL', 'business': True, 'distanceValue': 0.0, 'description': 'Voice Mail', 'charge': False, 'distanceDescription': 'Onsite'}], 'brandName': 'Rodeway', 'taxInclusive': False, 'status': 'ACTIVE', 'name': 'Rodeway Inn', 'coOpParticipant': False, 'productName': 'Inn', 'amenityGroups': [{'id': 'HIGH', 'description': 'Free WiFi'}, {'id': 'PRKT', 'description': 'Truck Parking'}, {'id': 'HOTB', 'description': 'Hot Breakfast'}, {'id': 'NSKH', 'description': 'Smoke Free'}], 'id': 'MA012', 'description': 'A good night and a great savings await you at the Rodeway Inn hotel in Brockton, MA located just south of Boston. Nearby destinations include Fenway Park, The Shaws Center, Campanelli Stadium, Brockton Fairgrounds, The Fuller Craft Museum and The War Memorial Building. Take advantage of amenities like free deluxe continental breakfast, free WiFi, seasonal outdoor pool, meeting rooms and access to fax and copy machines. Guest rooms feature a coffee maker, hair dryer, iron and ironing board. Also, earn rewards including free nights and gift cards with our Choice Privileges Rewards program.', 'lat': '42.063795', 'productCode': 'IN', 'address': {'line1': '1005 Belmont Street', 'subdivision': 'MA', 'city': 'Brockton', 'postalCode': '02301', 'country': 'US'}, 'brandCode': 'RW', 'phone': '(508) 588-3333'}}},
    'ma036': {'property_address': {'address': '4 Fisher Street,Foxboro,02035,MA,US', 'city': 'boston', 'name': 'Comfort Inn', 'id': 'MA036'}, 'property_details': {'status': 'OK', 'hotel': {'lon': '-71.238951', 'amenities': [{'code': 'PRKO', 'business': False, 'distanceValue': 0.0, 'description': 'Outdoor Parking', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'CORI', 'business': False, 'distanceValue': 0.0, 'description': 'Interior Corridors', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'COPY', 'business': True, 'distanceValue': 0.0, 'description': 'Guest Use Copy Machine', 'charge': True, 'distanceDescription': 'Onsite'}, {'code': 'OPEN', 'business': False, 'distanceValue': 0.0, 'description': 'Windows Open', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'LNGE', 'business': False, 'distanceValue': 0.0, 'description': 'Lounge/Bar', 'charge': True, 'distanceDescription': 'Onsite'}, {'code': 'RMCF', 'business': True, 'distanceValue': 0.0, 'description': 'In-Room Coffee Maker', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'LITE', 'business': True, 'distanceValue': 0.0, 'description': 'Well-lit Area, In-Room', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'FEMA', 'business': False, 'distanceValue': 0.0, 'description': 'Government Travelers: FEMA Approved', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'COFE', 'business': False, 'distanceValue': 0.0, 'description': 'Free Coffee', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'HLTH', 'business': True, 'distanceValue': 1.0, 'description': 'Health Club/Spa', 'distanceUnit': 'Miles', 'charge': True, 'distanceDescription': 'Nearby'}, {'code': 'NSKH', 'business': False, 'distanceValue': 0.0, 'description': '100% Smoke Free Hotel', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'VLSV', 'business': True, 'distanceValue': 0.0, 'description': 'Valet Cleaning Service', 'charge': True, 'distanceDescription': 'Onsite'}, {'code': 'PRKB', 'business': False, 'distanceValue': 0.0, 'description': 'Bus Parking', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'HOTB', 'business': False, 'distanceValue': 0.0, 'description': 'Free Hot Breakfast', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'FAXX', 'business': True, 'distanceValue': 0.0, 'description': 'Guest Use Fax Machine', 'charge': True, 'distanceDescription': 'Onsite'}, {'code': 'LNDR', 'business': False, 'distanceValue': 0.0, 'description': 'Guest Laundry', 'charge': True, 'distanceDescription': 'Onsite'}, {'code': 'GLFD', 'business': False, 'distanceValue': 6.0, 'description': 'Driving Range', 'distanceUnit': 'Miles', 'charge': True, 'distanceDescription': 'Nearby'}, {'code': 'NEWP', 'business': True, 'distanceValue': 0.0, 'description': 'Free Newspaper Mon-Fri', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'ELEV', 'business': False, 'distanceValue': 0.0, 'description': 'Elevator(s)', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'MVTH', 'business': False, 'distanceValue': 5.0, 'description': 'Movie Theatre', 'distanceUnit': 'Miles', 'charge': True, 'distanceDescription': 'Nearby'}, {'code': 'GOLF', 'business': False, 'distanceValue': 10.0, 'description': 'Golf Course', 'distanceUnit': 'Miles', 'charge': True, 'distanceDescription': 'Nearby'}, {'code': 'IRON', 'business': False, 'distanceValue': 0.0, 'description': 'Iron & Ironing Board', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'MINI', 'business': False, 'distanceValue': 3.0, 'description': 'Miniature Golf', 'distanceUnit': 'Miles', 'charge': True, 'distanceDescription': 'Nearby'}, {'code': 'HIKE', 'business': False, 'distanceValue': 5.0, 'description': 'Hiking/Nature Area', 'distanceUnit': 'Miles', 'charge': False, 'distanceDescription': 'Nearby'}, {'code': 'NPET', 'business': False, 'distanceValue': 0.0, 'description': 'No Pets Allowed', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'BILL', 'business': False, 'distanceValue': 6.0, 'description': 'Billiard Room', 'distanceUnit': 'Miles', 'charge': True, 'distanceDescription': 'Nearby'}, {'code': 'FWHI', 'business': True, 'distanceValue': 0.0, 'description': 'Free WiFi', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'RSTP', 'business': True, 'distanceValue': 0.0, 'description': 'Restaurant', 'charge': True, 'distanceDescription': 'Onsite'}, {'code': 'EXRM', 'business': True, 'distanceValue': 0.0, 'description': 'Exercise Room', 'charge': False, 'distanceDescription': 'Onsite'}, {'code': 'HDBR', 'business': False, 'distanceValue': 0.0, 'description': 'Braille Elevator(s)', 'charge': False, 'distanceDescription': 'Onsite'}], 'brandName': 'Comfort', 'taxInclusive': False, 'status': 'ACTIVE', 'name': 'Comfort Inn', 'coOpParticipant': True, 'productName': 'Inn', 'amenityGroups': [{'id': 'EXRM', 'description': 'Fitness Center'}, {'id': 'LNDR', 'description': 'Laundry, Guest'}, {'id': 'HIGH', 'description': 'Free WiFi'}, {'id': 'BAKE', 'description': 'Restaurant'}, {'id': 'HOTB', 'description': 'Hot Breakfast'}, {'id': 'NSKH', 'description': 'Smoke Free'}], 'id': 'MA036', 'description': 'Behind every great day is a great night at the Comfort Inn hotel in Foxboro, MA, which is conveniently located near Xfinity Center, Gillette Stadium, Mansfield Municipal Airport, Boston, Providence, and numerous colleges and universities. Our great amenities help you to get ready to take on the day, including free WiFi, ample free parking, free hot breakfast, fitness center, restaurant and bar. Rest up and refresh yourself in your cozy guest room, which features a coffee maker, hair dryer, TV, iron and ironing board. Some also have a refrigerator and microwave.  The more often you stay with us, the more rewards you earn with our Choice Privileges Rewards program. Rested. Set. Go.', 'lat': '42.038837', 'productCode': 'IN', 'address': {'line1': '4 Fisher Street', 'subdivision': 'MA', 'city': 'Foxboro', 'postalCode': '02035', 'country': 'US'}, 'brandCode': 'CI', 'phone': '(508) 543-1000'}}}
    }

    context_out = []

    if req.get("queryResult").get("action") == 'get.count':
        result = req.get("queryResult")
        parameters = result.get("parameters")
        speech = "Could not find the numbers, please refine the query ... "
        data = {}
        data = requests.get('https://api.covid19india.org/raw_data.json')
        jdata = data.json()

        if 'geo-state' in parameters:
            state = parameters.get('geo-state')
            counts = get_state_counts(state)
        else:
            counts = get_overall_counts()
        text = ''
        for k in counts.keys():
            text += k + ': ' + str(counts[k])
        speech = text
        data = counts

    elif req.get("result").get("action") == 'get.hotel.code':

        result = req.get("result")
        parameters = result.get("parameters")
        speech = "Could not locate any property, please refine the search ... "
        data = {}

        if 'address' in parameters:
            address = parameters.get('address')
            user_input = address + " "
        else:
            address = None

        if 'geo-city' in parameters:
            city = parameters.get('geo-city')
            user_input += city + " "
        else:
            city = None

        if 'hotel_brands' in parameters:
            brand = parameters.get('hotel_brands')
            user_input += brand + " "
        else:
            brand = None

        if 'geo-state-us' in parameters:
            us_state = parameters.get('geo-state-us')
            user_input += us_state
        else:
            us_state = None

        if 'specific_requests' in parameters:
            specific_request = parameters.get("specific_requests")
        else:
            specific_request = None

        specific_key = None
        if specific_request in ['pet', 'pets', 'dog', 'dogs']:
            specific_key = 'Pet-friendly Hotel'
        elif specific_request in ['free breakfast', 'breakfast', 'coffee']:
            specific_key = 'Free Hot Breakfast'

        property_address = [{'city': 'houston', 'address': '2475 North Freeway,Houston,77009,TX,US', 'id': 'TXC78', 'name': 'Sleep Inn & Suites Near Downtown North'},
        {'city': 'houston', 'address': '3134 Old Spanish Trail,Houston,77054,TX,US', 'id': 'TX933', 'name': 'MainStay Suites Texas Medical Center/Reliant Park'},
        {'city': 'houston', 'address': '6712 Morningside Drive,Houston,77030,TX,US', 'id': 'TX448', 'name': 'Rodeway Inn & Suites Medical Center'},
        {'city': 'houston', 'address': '7905 S. Main St.,Houston,77025,TX,US', 'id': 'TX280', 'name': 'Econo Lodge Near NRG Park - Medical Center'},
        {'city': 'buffalo', 'address': '5234 Ferry Street,Niagara Falls,L2G 1R5,ON,CA', 'id': 'CN856', 'name': 'Quality Inn & Suites'},
        {'city': 'buffalo', 'address': '5781 Victoria Ave.,Niagara Falls,L2G 3L6,ON,CA', 'id': 'CN166', 'name': 'Econo Lodge By the Falls'},
        {'city': 'buffalo', 'address': '7514 Lundys La.,Niagara Falls,L2H 1G8,ON,CA', 'id': 'CN167', 'name': "Comfort Inn Lundy's Lane"},
        {'city': 'buffalo', 'address': '551 South Transit Street,Lockport,14094,NY,US', 'id': 'NY098', 'name': 'Quality Inn'}]

        properties = []
        hotel_ids = []
        all_data = []
        if city and brand:
            for row in property_address:
                if row['city'].lower() == city.lower():
                    if brand.lower() in row['name'].lower() or brand.lower() in row['address'].lower():
                        properties.append(row['id'].lower() + ": " + row['name'] + ", " + row['address'] + ", " + row['city'])
                        hotel_ids.append(row['id'].lower())
                        all_data.append(row)
            out_string = ' and '.join(properties)
            speech = "Found " + str(len(properties)) + " propertie(s): " + out_string
            data = properties

        elif city and address:
            for row in property_address:
                if row['city'].lower() == city.lower():
                    if address.lower() in row['name'].lower() or address.lower() in row['address'].lower():
                        properties.append(row['id'].lower() + ": " + row['name'] + ", " + row['address'] + ", " + row['city'])
                        hotel_ids.append(row['id'].lower())
                        all_data.append(row)
            out_string = ' and '.join(properties)
            speech = "Found " + str(len(properties)) + " propertie(s): " + out_string
            data = properties

            # Duplicate from the below part (address) - need to merge
            if len(properties) == 0:
                possible_id = None
                possible_description = None
                max_score = 0
                specific_row = None
                for row in property_address:
                    score = SequenceMatcher(None, user_input, row['name'] + ' ' + row['address'] + ' ' + row['city']).ratio()
                    if score > max_score:
                        possible_id = row['id']
                        possible_description = row['id'].lower() + ": " + row['name'] + ", " + row['address'] + ", " + row['city']
                        specific_row = row
                        max_score = score

                if possible_id:
                    hotel_ids.append(possible_id)
                    properties.append(possible_description)
                    all_data.append(specific_row)
                    speech = "Top matching property is: " + possible_description
                    data = properties
                else:
                    speech = "Trying to get the top matching property ..."

        elif address:
            possible_id = None
            possible_description = None
            max_score = 0
            specific_row = None
            for row in property_address:
                # max_score = get_matching_scores(user_input, row['name'] + ' ' + row['address'] + ' ' + row['city'])
                score = SequenceMatcher(None, address, row['name'] + ' ' + row['address'] + ' ' + row['city']).ratio()
                if score > max_score:
                    possible_id = row['id']
                    possible_description = row['id'].lower() + ": " + row['name'] + ", " + row['address'] + ", " + row['city']
                    specific_row = row
                    max_score = score

            # sorted_properties = sorted(possible_properties.items(), key=operator.itemgetter(1))
            # take the most similar property
            if possible_id:
                hotel_ids.append(possible_id)
                properties.append(possible_description)
                all_data.append(specific_row)
                speech = "Top matching property is: " + possible_description
                data = properties
            else:
                speech = "Trying to get the top matching property ..."

        if len(properties) == 1 and specific_key:
            id = hotel_ids[0]
            # r2 = requests.post("https://www.choicehotels.com/webapi/hotel/"+id.lower(),
            #                    data={"businessFunction": "view_hotel",
            #                          "include": ["amenities", "amenity_groups"], "preferredLocaleCode": "en-us"})
            # d2 = json.loads(r2.text)

            d2 = property_details['id']['property_details']

            descriptions = [a['description'] for a in d2['hotel']['amenities']]

            if specific_key in descriptions:
                if specific_key == 'Pet-friendly Hotel':
                    speech = properties[0] + ' allows pets'
                elif specific_key == 'Free Hot Breakfast':
                    speech = properties[0] + ' has free breakfast'
            else:
                speech = properties[0] + " does not have the facility for " + specific_request

        # context_out = {"contextOut": all_data}
        context_out = [{"name": "hotel-codes", "lifespan": 5, "parameters": {"property_data": all_data}}]
        # if not specific_key:
        #     # context_out = {"contextOut": [{"name":"weather", "lifespan":2, "parameters":{"city":"Rome"}}]}
        #     context_out = all_data

    # fetch property details by property code
    elif req.get("result").get("action") == "get.property.details":  # action name
        result = req.get("result")
        parameters = result.get("parameters")

        if 'property_code' in parameters:
            property_code = parameters.get('property_code')
        else:
            property_code = 'ma199'

        if 'hotel_data' in parameters:
            query = parameters.get('hotel_data')
        else:
            query = 'amenities'

        if query == 'amenities':
            include_list = ["amenities", "amenity_groups"]
        elif query in ['attractions', 'airports', 'restaurants']:
            include_list = ['destinations']
        else:
            include_list = []

        try:
            # r = requests.post("https://www.choicehotels.com/webapi/hotel/" + property_code.lower(),
            #                    data={"businessFunction": "view_hotel",
            #                          "include": include_list, "preferredLocaleCode": "en-us"})
            # r = requests.post("https://www.choicehotels.com/webapi/hotel/" + property_code.lower(),
            #                    data={"businessFunction": "view_hotel"})
            # d = json.loads(r.text)
            d = property_details[property_code.lower()]['property_details']

            print(d['status'])
            hotel_name = d['hotel']['name']

            if query == 'amenities':
                descriptions = [a['description'] for a in d['hotel']['amenities']]
                out_string = ','.join(descriptions)
                speech = "Following amenities are available in " + hotel_name + ": " + out_string

            elif query == 'attractions':
                descriptions = [a['name'] for a in d['hotel']['destinations']['attractions']]
                out_string = ';'.join(descriptions)
                speech = "There are " + str(len(descriptions)) + " places to visit near " + hotel_name + ": " + out_string

            elif query == 'airports':
                descriptions = [a['name'] for a in d['hotel']['destinations']['airports']]
                out_string = ';'.join(descriptions)
                speech = "There are " + str(len(descriptions)) + " airports near " + hotel_name + ": " + out_string

            elif query == 'restaurants':
                descriptions = [a['name'] for a in d['hotel']['destinations']['restaurants']]
                out_string = ';'.join(descriptions)
                speech = "There are " + str(len(descriptions)) + " restaurants near " + hotel_name + ": " + out_string

            elif query == 'address':
                descriptions = d['hotel']['address']
                out_string = ','.join([descriptions[k] for k in ['line1', 'city', 'postalCode', 'subdivision', 'country']])
                speech = 'The address of ' + hotel_name + ' is: ' + out_string

            elif query in ['phone', 'phone number', 'contact']:
                descriptions = d['hotel']['phone']
                speech = 'The contact number of ' + hotel_name + ' is: ' + descriptions

            else:
                descriptions = 'NA'

            data = descriptions
        except:
            speech = 'Cannot fetch any data for ' + property_code + ' (' + str(r) + ') found'
            data = {}

    elif req.get("result").get("action") == "specific.answer":  # action name

        result = req.get("result")
        contexts = result.get("contexts")

        # 'hotel-codes' context is coming from intent = "specific_question_single_property"
        # 'available-hotel-codes' is coming from find_hotels_in_an_area (intent)
        if contexts[0]['name'] == 'hotel-codes' or contexts[0]['name'] == 'available-hotel-codes':

            parameters = contexts[0].get("parameters")

            if 'property_data' in parameters:
                property_data = parameters.get("property_data")
                property_dict = property_data
                # if len(property_data) > 0:
                #     property_dict = property_data[0]
                # else:
                #     property_dict = None
            else:
                property_dict = None

            if 'specific_requests' in parameters:
                specific_request = parameters.get("specific_requests")
            else:
                specific_request = None

            if specific_request in ['pet', 'pets']:
                specific_key = 'Pet-friendly Hotel'
                include_list = ["amenities", "amenity_groups"]
            elif specific_request in ['free breakfast', 'breakfast']:
                specific_key = 'Free Hot Breakfast'
                include_list = ["amenities", "amenity_groups"]
            elif specific_request in ['amenities']:
                specific_key = specific_request
                include_list = ["amenities", "amenity_groups"]
            elif specific_request in ['attractions', 'airports', 'restaurants']:
                specific_key = specific_request
                include_list = ['destinations']
            else:
                specific_key = specific_request
                include_list = []

            if len(property_dict) > 1 and specific_key:
                data = []
                if specific_key in ['Pet-friendly Hotel', 'Free Hot Breakfast']:
                    flag = False
                    qualifying_properties = []
                    
                    for p in property_dict:
                        d = property_details[p['id'].lower()]['property_details']
                        descriptions = [a['description'] for a in d['hotel']['amenities']]
                        if specific_key in descriptions:
                            # qualifying_properties.append(p['name'] + ', ' + p['address'])
                            qualifying_properties.append(p['id'].lower() + ': ' + p['name'])
                        data.append(descriptions)

                    if len(qualifying_properties) > 0:
                        all_qualifying_properties = '\n'.join(qualifying_properties)
                        if specific_key == 'Pet-friendly Hotel':
                            speech = all_qualifying_properties + ' will allow pets'
                        elif specific_key == 'Free Hot Breakfast':
                            speech = all_qualifying_properties + ' will provide free breakfast'
                    else:
                        if specific_key == 'Pet-friendly Hotel':
                            speech = 'None of these properties allows pets'
                        elif specific_key == 'Free Hot Breakfast':
                            speech = 'None of these properties provides free breakfast'
                
            elif len(property_dict)==1 and specific_key:
                # r = requests.post("https://www.choicehotels.com/webapi/hotel/"+property_dict['id'].lower(),
                #                    data={"businessFunction": "view_hotel",
                #                          "include": include_list, "preferredLocaleCode": "en-us"})
                # d = json.loads(r.text)
                d = property_details[property_dict['id'].lower()]['property_details']

                if specific_key in ['Pet-friendly Hotel', 'Free Hot Breakfast']:
                    descriptions = [a['description'] for a in d['hotel']['amenities']]
                    if specific_key in descriptions:
                        if specific_key == 'Pet-friendly Hotel':
                            speech = property_dict["name"] + ' allows pets'
                        elif specific_key == 'Free Hot Breakfast':
                            speech = property_dict["name"] + ' has free breakfast'
                    else:
                        speech = property_dict["name"] + " does not have the facility for " + specific_request

                elif specific_key == 'amenities':
                    descriptions = [a['description'] for a in d['hotel']['amenities']]
                    out_string = ', '.join(descriptions)
                    speech = "Following amenities are available in " + property_dict["name"] + ": " + out_string

                elif specific_key == 'attractions':
                    descriptions = [a['name'] for a in d['hotel']['destinations']['attractions']]
                    out_string = '; '.join(descriptions)
                    speech = "There are " + str(len(descriptions)) + " places to visit near " + property_dict["name"] + ": " + out_string

                elif specific_key == 'airports':
                    descriptions = [a['name'] for a in d['hotel']['destinations']['airports']]
                    out_string = '; '.join(descriptions)
                    speech = "There are " + str(len(descriptions)) + " airports near " + property_dict["name"] + ": " + out_string

                elif specific_key == 'restaurants':
                    descriptions = [a['name'] for a in d['hotel']['destinations']['restaurants']]
                    out_string = '; '.join(descriptions)
                    speech = "There are " + str(len(descriptions)) + " restaurants near " + property_dict["name"] + ": " + out_string

                elif specific_key == 'address':
                    descriptions = d['hotel']['address']
                    out_string = ', '.join([descriptions[k] for k in ['line1', 'city', 'postalCode', 'subdivision', 'country']])
                    speech = 'The address of ' + property_dict["name"] + ' is: ' + out_string

                elif specific_key in ['phone', 'phone number', 'contact']:
                    descriptions = d['hotel']['phone']
                    speech = 'The contact number of ' + property_dict["name"] + ' is: ' + descriptions
                data = descriptions
            
            else:
                speech = "Cannot fetch any data ... (python code)"
                data = {}

        # This context is coming from intent = "specific_question_multiple_properties"
        elif contexts[0]['name'] == 'hotel_search_details':

            parameters = result.get("contexts")[0].get("parameters")  # data coming from previous context, not from parameters

            if 'geo-city' in parameters:
                place = parameters.get("geo-city")
            else:
                place = 'London'

            if 'start-date' in parameters:
                start_date = parameters.get("start-date")
            else:
                start_date = time.strftime('%Y-%m-%d')  # today's date

            if 'end-date' in parameters:
                end_date = parameters.get("end-date")
            else:
                today = datetime.datetime.today()
                tomorrow = today + datetime.timedelta(1)
                end_date = datetime.datetime.strftime(tomorrow,'%Y-%m-%d')  # tomorrow's date

            if 'cardinal' in parameters:
                num_adults = int(parameters.get('cardinal'))
            else:
                num_adults = 1

            if 'specific_requests' in parameters:
                specific_request = parameters.get("specific_requests")
            else:
                specific_request = 'NA'

            specific_key = 'NA'
            if specific_request in ['pet', 'pets']:
                specific_key = 'Pet-friendly Hotel'
            elif specific_request in ['free breakfast', 'breakfast']:
                specific_key = 'Free Hot Breakfast'

            try:
                r = requests.post("https://www.choicehotels.com/webapi/location/hotels", data={"placeName": place,
                    "adults": num_adults, "checkInDate": start_date, "checkOutDate": end_date,
                    "ratePlans": "RACK%2CPREPD%2CPROMO%2CSCPM", "rateType":"LOW_ALL"})
                if r.status_code == 200:
                    d = json.loads(r.text)
                    hotels = d['hotels']
                    hotel_id_dict = {}
                    for h in hotels:
                        hotel_id_dict[h['id']] = h['name']
                    # hotel_names = [': '.join([h['id'], h['name']]) for h in hotels if h['hotelSectionType'] == 'AVAILABLE_HOTELS']
                    hotel_ids = [h['id'] for h in hotels if h['hotelSectionType'] == 'AVAILABLE_HOTELS']
                    hotel_ids = hotel_ids[:10]  # limit the search to 10 properties for time-out error
                    selected_hotels = []
                    # out_str = ''
                    for id in hotel_ids:
                        # r2 = requests.post("https://www.choicehotels.com/webapi/hotel/"+id.lower(),
                        #                    data={"businessFunction": "view_hotel",
                        #                          "include": ["amenities", "amenity_groups"], "preferredLocaleCode": "en-us"})
                        # d2 = json.loads(r2.text)
                        d2 = property_details[id.lower()]['property_details']

                        descriptions = [a['description'] for a in d2['hotel']['amenities']]
                        # out_str += id + '--'.join(descriptions)
                        if specific_key in descriptions:
                            selected_hotels.append(hotel_id_dict[id])

                    hotel_names_string = ' and '.join(selected_hotels)
                    speech = "Found " + str(len(selected_hotels)) + " hotel(s) for " + specific_request + ": " + hotel_names_string
                    # speech = out_str
                    data = selected_hotels
                else:
                    speech = "Requesting for " + place + ' returned status: ' + str(r.status_code) + r.reason
                    data = {}

            except:
                speech = 'Not working for ' + place
                data = {}

    elif req.get("result").get("action") == "show.hotels":  # action name

        result = req.get("result")
        parameters = result.get("parameters")

        if 'geo-city' in parameters:
            place = parameters.get("geo-city")
        else:
            place = 'London'

        if 'geo-state-us' in parameters:
            state = parameters.get("geo-state-us")
            if len(state) > 0:
                place += ", " + state

        if 'start-date' in parameters:
            start_date = parameters.get("start-date")
        else:
            start_date = time.strftime('%Y-%m-%d')  # today's date

        if 'end-date' in parameters:
            end_date = parameters.get("end-date")
        else:
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(1)
            end_date = datetime.datetime.strftime(tomorrow,'%Y-%m-%d')  # tomorrow's date

        if 'cardinal' in parameters:
            num_adults = int(parameters.get('cardinal'))
        else:
            num_adults = 1

        # try:
            # r = requests.post("https://www.choicehotels.com/webapi/location/hotels", data={"placeName": place,
            #     "adults": num_adults, "checkInDate": start_date, "checkOutDate": end_date,
            #     "ratePlans": "RACK%2CPREPD%2CPROMO%2CSCPM", "rateType":"LOW_ALL"})
            # if r.status_code == 200:
            #     d = json.loads(r.text)
            #     hotels = d['hotels']
            #     hotel_names = [': '.join([h['id'], h['name']]) for h in hotels if h['hotelSectionType'] == 'AVAILABLE_HOTELS']
            #     hotel_names_string = '\t'.join(hotel_names)
            #     speech = "Found " + str(len(hotel_names)) + " hotel(s): " + hotel_names_string
            #     data = hotel_names
            # else:
            #     speech = "Requesting for " + place + ' returned status: ' + str(r.status_code) + ', ' + r.reason
            #     data = {}

        available_properties = {
            'boston_1': ['MA225: enVision Hotel Boston-Everett, an Ascend Hotel Collection Member', 'MA199: enVision Hotel Boston-Longwood, an Ascend Hotel Collection Member', 'MA109: Comfort Inn', 'MA051: Comfort Inn & Suites Logan International Airport', 'MA129: Rodeway Inn Logan International Airport', 'MA080: Econo Lodge', 'MA230: Quality Inn', 'MA110: Comfort Inn', 'MA193: Comfort Inn Randolph - Boston', 'MA147: Quality Inn & Suites', 'MA047: Comfort Inn Rockland - Boston', 'MA139: Econo Lodge', 'MA074: Econo Lodge', 'MA012: Rodeway Inn', 'MA036: Comfort Inn'],
            'boston_2': ['MA225: enVision Hotel Boston-Everett, an Ascend Hotel Collection Member', 'MA199: enVision Hotel Boston-Longwood, an Ascend Hotel Collection Member', 'MA109: Comfort Inn', 'MA051: Comfort Inn & Suites Logan International Airport', 'MA129: Rodeway Inn Logan International Airport', 'MA080: Econo Lodge', 'MA230: Quality Inn', 'MA110: Comfort Inn', 'MA193: Comfort Inn Randolph - Boston', 'MA147: Quality Inn & Suites', 'MA047: Comfort Inn Rockland - Boston', 'MA139: Econo Lodge', 'MA074: Econo Lodge', 'MA012: Rodeway Inn', 'MA036: Comfort Inn'],
            'london_1': ['GB113: Comfort Inn Victoria', 'GB209: Comfort Inn Westminster', 'GB125: Comfort Inn Buckingham Palace Road', 'GB049: Comfort Inn St Pancras - Kings Cross', 'GB157: Comfort Inn Edgware Road W2', 'GB182: Comfort Inn Hyde Park', 'GB645: Quality Hotel Hampstead', 'GB191: Clarion Collection Hotel Richmond Gate', 'GB193: Clarion Collection Harte and Garter Hotel and Spa'],
            'london_2': ['GB113: Comfort Inn Victoria', 'GB209: Comfort Inn Westminster', 'GB125: Comfort Inn Buckingham Palace Road', 'GB049: Comfort Inn St Pancras - Kings Cross', 'GB157: Comfort Inn Edgware Road W2', 'GB182: Comfort Inn Hyde Park', 'GB645: Quality Hotel Hampstead', 'GB191: Clarion Collection Hotel Richmond Gate', 'GB193: Clarion Collection Harte and Garter Hotel and Spa']
        }

        hotel_names = available_properties[place.lower()+'_'+str(num_adults)]
        hotel_names_string = '\n'.join(hotel_names)
        speech = "Found " + str(len(hotel_names)) + " hotel(s): " + hotel_names_string
        data = hotel_names
        all_data = []
        for h in hotel_names:
            pid, name = h.split(": ")
            all_data.append({'id': pid, 'name': name})

        modified_parameters = parameters
        modified_parameters["property_data"] = all_data
        context_out = [{"name": "available-hotel-codes", "lifespan": 5, "parameters": modified_parameters}]
        # except:
        #     speech = 'Not working for ' + place
        #     data = {}

    else:
        speech = 'No matching intent found ... python code returns None'
        data = {}


    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": data,
        "contextOut": context_out,
        "source": "apiai-choicehotel-queries"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    # print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
