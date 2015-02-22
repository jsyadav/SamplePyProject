'''
Created on Feb 22, 2015

@author: jyadav
'''
from datetime import *

def TextField():
    return ""

def ListField(t):
    return []

def IntegerField():
    return 0

def DateTimeField():
    return datetime.date()

def DictField():
    return {}

def BooleanField():
    return False

class ConsolidatedDoc():
    projects = ListField(DictField())
    sentimentScore = IntegerField()
    indexes = DictField()
    publishedDateAndTime = datetime.datetime 
    ''' Changed from indexDate on indexData '''
    scrapeDate = DateTimeField()
    createdDate = DateTimeField()
    source = TextField()
    isChild = BooleanField()
    sourceType = TextField()
    plainText = TextField()
    translatedText = TextField()
    cleanedText = TextField()
    parsedDoc = TextField()
    namedEntities = ListField(TextField())
    totalWordCount = IntegerField()
    hitsCount = IntegerField()
    poiID = TextField()
    geo = DictField()
    places = ListField(TextField())
    people = ListField(TextField())
    tags = ListField(TextField())
    VirtualKey = TextField()
    rawDocument = TextField()
    Author = TextField()
    AuthorId = TextField()
    AuthorFriendsCount = IntegerField()
    AuthorFollowersCount = IntegerField()
    docType = TextField()
    docTypelocale = TextField()
    uri = TextField()
    groupid = TextField()
    parentid = TextField()
    state = TextField()
    gender = TextField()
    kloutScore = IntegerField()
    title = TextField()
    topics = ListField(TextField())
    dataprovider = TextField()
    organizations =  ListField(TextField())
    guests =  ListField(TextField())
    sourceLocale = TextField()
    sourceNationalityLocale = TextField()
    sourceNationality = TextField()
    sourceLanguage = TextField()
    sourceLanguageLocale = TextField()
    publishCountryLocale = TextField()
    publishCountry = TextField()
    '''TV EYEs Fields'''
    mediaPersonalities = ListField(DictField())
    mediaClipDuration = TextField()
    
    productName = TextField()
    productNumber = TextField()
    productManufacturer = TextField()
    productPrice = TextField()
