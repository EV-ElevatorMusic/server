import pymongo
from pymongo import MongoClient

conn=MongoClient('localhost',27017)
db=conn['mocon']
# name music_key             emotion view
#  o   2G4AUqfwxcV1UdQjm2ouYr sad     0