from configparser import ConfigParser
from LastfmApi import LastfmApi

if __name__ == "__main__":
    print("Crawling start")
    configparser = ConfigParser()
    configparser.read('../.config')
    api_infor={}
    api_infor["username"] = configparser.get('lastfm', 'username')
    api_infor["password"] = configparser.get('lastfm', 'password')
    api_infor["api_key"] = configparser.get('lastfm', 'API_KEY')
    api_infor["api_url"] = configparser.get('lastfm', 'API_URL')
    testApi = LastfmApi(api_infor)
    print(testApi.getUserIdbyRandomFromMongo())
    #print(testApi.getFriendApiTest())




