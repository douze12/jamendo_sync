
import urllib.request
import json


class JamendoUtil:

    def __init__(self, client_id, base_url):
        if not client_id:
            raise Exception("You must provide a client_id setting")

        self.client_id = client_id
        
        self.base_url = base_url
        
    def _createUrlParameters(self, **kwargs):
        params = dict()
        params["client_id"] = self.client_id
        for key in kwargs:
            params[key] = kwargs[key]
            
        return urllib.parse.urlencode(params)
    
    def _parseResponse(self, response):
        
        jsonResp = json.loads(response.decode("UTF-8"))
        if(jsonResp == None or jsonResp["headers"] == None):
            raise JamendoError(12000, "Error when load JSON response")
        
        if(jsonResp["headers"]["status"] != "success"):
            raise JamendoError(jsonResp["headers"]["code"], jsonResp["headers"]["error_message"])
        
        return jsonResp
        
      
    def getUserId(self, userName):
        
        if(userName == None or len(userName) <= 0):
            raise Exception("User name should not be empty")
        
        requestUrl = self.base_url + "/users/?%s" % self._createUrlParameters(name=userName)

        request = urllib.request.Request(requestUrl)
        response = urllib.request.urlopen(request)
            
        jsonResponse=response.read()
        obj = self._parseResponse(jsonResponse)
        
        if(len(obj["results"]) < 1):
            raise JamendoError(12001, "Empty result when trying to get user id")
        
        return obj["results"][0]["id"]
    
    def getPublicPlaylists(self, userId):
        
        if(userId == None or int(userId) <= 0):
            raise Exception("User id must be set")
        
        requestUrl = self.base_url + "/playlists/?%s" % self._createUrlParameters(user_id=userId)
        request = urllib.request.Request(requestUrl)
        response = urllib.request.urlopen(request)
            
        jsonResponse=response.read()
        obj = self._parseResponse(jsonResponse)
        
        return obj["results"]
    
    def getPlaylistTracks(self, playlistId):
        if(playlistId == None or int(playlistId) <= 0):
            raise Exception("Playlist id must be set")
        
        requestUrl = self.base_url + "/playlists/tracks/?%s" % self._createUrlParameters(id=playlistId)
        request = urllib.request.Request(requestUrl)
        response = urllib.request.urlopen(request)
            
        jsonResponse=response.read()
        obj = self._parseResponse(jsonResponse)
        
        if len(obj["results"]) <= 0 or len(obj["results"][0]) <= 0:
            return []
        
        return obj["results"][0]["tracks"]
            
            
class JamendoError(Exception):
    
    def __init__(self, code, message):
        self.code = code
        self.message = message
            
        
