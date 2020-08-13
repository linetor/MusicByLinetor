import urllib
import urllib.request
import json

class LastfmApi:
    """
    Using lastFM api
    """
    def __init__(self, api_infor):
        self._api_infor = api_infor
        self._format="json"

    def getFriendApiTest(self):
        self._firstUser = "eartle"
        self._method = "user.getFriends"
        getApiMap={"api_key":self._api_infor["api_key"],"format":self._format,"method":self._method
            ,"user":self._firstUser,"limit":1}
        urlEncode=urllib.parse.urlencode(getApiMap)
        the_page=urllib.request.urlopen(self._api_infor["api_url"]+"?"+urlEncode)
        responseData = the_page.read().decode('utf-8')
        jsonResponse=json.loads(responseData)
        print (jsonResponse)




