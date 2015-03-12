'''
Created on Mar 03, 2015

@author: jyadav
'''
import datetime
import json
 
 
def TextField():
    return None
 
 
def ListField(t):
    return None
 
 
def IntegerField():
    return None
 
 
def DateTimeField():
    return None
 
 
def DictField():
    return None
 
 
def BooleanField():
    return None
 
 
class ConsolidatedDocument(dict):
    def __init__(self, **kwargs):
        super(ConsolidatedDocument, self).__init__(**kwargs)
        self.projects = ListField(DictField())
        self.sentiment_score = IntegerField()
        self.socialgist_id = IntegerField()
        self.status_id = IntegerField()
        self.pic_id = IntegerField()
        self.bmiddle_pic = TextField()
        self.original_pic = TextField()
        self.thumbnail_pic = TextField()
        self.m_id = IntegerField()
        self.favorited = BooleanField()
        self.reposts_count = IntegerField()
        self.comments_count = IntegerField()
        self.indexes = DictField()
        self.published_date_and_time = DateTimeField()
        ''' Changed from indexDate on indexData '''
        self.scrape_date = DateTimeField()
        self.created_date = DateTimeField()
        self.source = TextField()
        self.is_child = BooleanField()
        self.source_type = TextField()
        self.plain_text = TextField()
        self.translated_text = TextField()
        self.cleaned_text = TextField()
        self.parsed_doc = TextField()
        self.named_entities = ListField(TextField())
        self.total_word_count = IntegerField()
        self.hits_count = IntegerField()
        self.poi_id = TextField()
        self.geo = DictField()
        self.places = ListField(TextField())
        self.people = ListField(TextField())
        self.tags = ListField(TextField())
        self.virtual_key = TextField()
        self.raw_document = TextField()
        self.keyword = TextField()
        self.keyword_flag = TextField()
        self.author = TextField()
        self.author_domain = TextField()
        self.author_coordinates = TextField()
        self.author_id = TextField()
        self.author_city_id = IntegerField()
        self.author_verified = BooleanField()
        self.author_followers_count = IntegerField()
        self.author_verified_type = IntegerField()
        self.author_province = IntegerField()
        self.author_province_id = IntegerField()
        self.author_statuses_count = IntegerField()
        self.author_description = TextField()
        self.author_friends_count = IntegerField()
        self.author_profile_image = TextField()
        self.author_profile_url = TextField()
        self.author_following = BooleanField()
        self.author_city = TextField()
        self.author_geo_enabled = BooleanField()
        self.author_screen_name = TextField()
        self.author_fav_count = TextField()
        self.author_other_url = TextField()
        self.author_gender = TextField()
        self.author_join_date = TextField()
        self.author_pagefriends_count = IntegerField()
        self.author_province_coordinates = TextField()
        self.mblog_id = TextField()
        self.doc_type = TextField()
        self.doc_type_locale = TextField()
        self.uri = TextField()
        self.group_id = TextField()
        self.parent_id = IntegerField()
        self.state = TextField()
        self.klout_score = IntegerField()
        self.title = TextField()
        self.topics = ListField(TextField())
        self.dataprovider = TextField()
        self.organizations = ListField(TextField())
        self.guests = ListField(TextField())
        self.source_locale = TextField()
        self.source_nationality_locale = TextField()
        self.source_nationality = TextField()
        self.source_language = TextField()
        self.source_language_locale = TextField()
        self.publish_country_locale = TextField()
        self.publish_country = TextField()
        self.id = IntegerField()
       # Newly added fields for renren
       # renren status
        self.sharedstatus_id = IntegerField()
        self.shareduser_id = IntegerField()
        self.share_count = IntegerField()
        self.author_star = BooleanField()
        self.author_bday = TextField()
        self.author_emo_state = TextField()
        self.author_work = TextField()
        self.author_page_info = TextField()
        self.author_stats = TextField()
        self.author_vip_info = TextField()
        self.author_education = TextField()
        self.author_like = TextField()
        # renren blog
        self.access_control = TextField()
        self.view_count = IntegerField()
        self.album_id = IntegerField()
        self.album_desc = TextField()
        self.photo_count = IntegerField()
        self.album_cover = TextField()
        self.lastmodify_time = TextField()
        self.content_type = TextField()
        self.album_name = TextField()
        self.comment_type = TextField()
        self.owner_id = IntegerField()
        #newly added fields for tencent
        self.queries = TextField()
        self.thread_id = IntegerField()
        self.post_id = IntegerField()
        self.posts_count = IntegerField()
        self.author_following_count  = IntegerField()
        self.pic_url = TextField()
        '''TV EYEs Fields'''
        self.media_personalities = ListField(DictField())
        self.media_clip_duration = TextField()
        self.product_name = TextField()
        self.product_number = TextField()
        self.product_manufacturer = TextField()
        self.product_price = TextField()
 
    def __getstate__(self):
        return self
 
    def __setstate__(self, state):
        self = state
       
    def __setattr__(self, name, value):
        self[name] = value
 
    def __getattr__(self, name):
        value = self[name]
        if isinstance(value, (list, tuple, dict)):
            return json.dumps(value)
        else:
            return value
 
    def to_dict(self):
        """Return the JSON string representation of the object"""
        d = {}
        keys = vars(self).keys()
        for k in keys:
            d[k] = self.__getattribute__(k)
        return d