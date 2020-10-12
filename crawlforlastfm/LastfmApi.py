import urllib
import urllib.request
import json
from configparser import ConfigParser
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) +"/db")
from MongoManager import MongoManager #none problem
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne

class LastfmApi:
    """
    Using lastFM api
    """
    mongoclient = None

    def __init__(self, api_infor):
        self.configparser = ConfigParser()
        self.configparser.read('../.config')
        self._api_infor = api_infor
        self._format="json"
        self._userLimit = 100
        self._mongodb = "lastfm"
        self._mongoUserCollection = "user"
        self._mongoFriendCollection = "friend"

        if self.mongoclient == None:
            self.mongoclient = MongoManager.getInstance()

        def __del__(self):
            self.mongoclient.close()

    def getFriendApiFirst(self):
        self._firstUser = self.configparser.get('lastfm', 'seeduser')
        self._method = "user.getFriends"
        getApiMap={"api_key":self._api_infor["api_key"],"format":self._format,"method":self._method
            ,"user":self._firstUser,"limit":self._userLimit}
        urlEncode=urllib.parse.urlencode(getApiMap)
        the_page=urllib.request.urlopen(self._api_infor["api_url"]+"?"+urlEncode)
        responseData = the_page.read().decode('utf-8')
        jsonResponse=json.loads(responseData)
        return jsonResponse

    def getFriendApiFromPage(self, userid,pageNum):
        self._method = "user.getFriends"
        self._firstUser = userid

        getApiMap={"api_key":self._api_infor["api_key"],"format":self._format,"method":self._method
            ,"user":self._firstUser,"limit":self._userLimit,"page":pageNum}
        urlEncode=urllib.parse.urlencode(getApiMap)
        the_page=urllib.request.urlopen(self._api_infor["api_url"]+"?"+urlEncode)
        responseData = the_page.read().decode('utf-8')
        jsonResponse=json.loads(responseData)
        return jsonResponse


    def getUserIdbyRandomFromMongo(self):
        userInfor = self.mongoclient[self._mongodb][self._mongoUserCollection].find_one()

        if (userInfor == None):
            print("User None Infor")
        else :
            print("checking : " , userInfor)

        if(userInfor == None) :
            friendInfor = self.getFriendApiFirst()
            fromUser=friendInfor['friends']['@attr']['user']
            totalPage=friendInfor['friends']['@attr']['totalPages']
            friendInforList = friendInfor['friends']['user']

        else :
            friendInfor = self.mongoclient[self._mongodb][self._mongoFriendCollection].aggregate(
                [ { "$sample": { "size": 1 } } ]
            )
            fromUser=friendInfor['name']
            friendInforList = self.getFriendApiFromPage(fromUser,0)['friends']['user']

        friend_upsert={"name" : fromUser}
        friend_upsert['friendlist']=set([])
        for idx,tempDic in enumerate(friendInforList):
            friend_upsert['friendlist'].add(tempDic['name'])
        print("total page",int(totalPage))

        for newpage in range(2,int(totalPage)+1):
            nextfriendInforList = self.getFriendApiFromPage(fromUser,newpage)['friends']['user']
            print(nextfriendInforList)
            for idx,tempDic in enumerate(nextfriendInforList):
                friend_upsert['friendlist'].add(tempDic['name'])

        friend_upsert['friendlist']=list(friend_upsert['friendlist'])
        result = self.mongoclient[self._mongodb][self._mongoFriendCollection].update_one({"name":fromUser},
                                                                                         {"$set" :friend_upsert}, upsert=True)
        print("get friend result : ",result.modified_count)
        print("get friend  : ",friend_upsert)
        print(len(set(friend_upsert['friendlist'])))

        #bulk_user_upsert.append(UpdateOne({"name":tempDic['name']},{"$set" : tempDic}))
        #friendInforJson[str(idx)]=tempDic
        #idInforJson[str(idx)] = {"name":tempDic['name']}




        """
        friendInforJson ={}
            idInforJson ={}
            bulk_user_upsert=[]

            for idx,tempDic in enumerate(friendInforList):
                bulk_user_upsert.append(UpdateOne({"name":tempDic['name']},{"$set" : tempDic}))
                friendInforJson[str(idx)]=tempDic
                idInforJson[str(idx)] = {"name":tempDic['name']}

            friendInforJson = json.loads(json.dumps (friendInforJson)).values()
            idJson = json.loads(json.dumps (idInforJson)).values()

            result = self.mongoclient[self._mongodb][self._mongoFriendCollection].bulk_write(bulk_user_upsert)
            from pprint import pprint
            pprint(result.bulk_api_result)
        else :
            friendInfor = self.mongoclient[self._mongodb][self._mongoFriendCollection].aggregate(
                [ { "$sample": { "size": 1 } } ]
            )
            print(friendInfor)
    """



        return "Done"
    def getFriendList(self):
        print("b")




