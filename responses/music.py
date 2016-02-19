# -*- coding: utf-8 -*-
from AbstractResponse import AbstractResponse
import requests
import os
import json
import sys

class ResponseMusic(AbstractResponse):
    RESPONSE_KEY = "#music"

    def __init__(self, msg):
        super(ResponseMusic, self).__init__(msg)

    def respond(self):
        out = ""
        print("lastfm")
        lastfm_endpoint = "http://ws.audioscrobbler.com/2.0/"
        person_status_template = u"{name} : {song}\n"
        key = None
        try:
            with open('local_variables.json') as f:
                local_var = json.load(f)
                key = local_var["LASTFM_KEY"]
        except EnvironmentError:
                key = os.getenv("LASTFM_KEY")

        if not key:
            print("failed to load LASTFM_KEY--- aborting!")
            return

        req_data = dict()
        req_data['format'] = 'json'
        req_data['limit'] = 1
        req_data['method'] = "user.getRecentTracks"

        for person, username in AbstractResponse.GroupMetoLastfm.iteritems():
            try:
                if not username:
                    continue
                print("Looking up username: " + username)
                req_data['user'] = username
                req_data['api_key'] = key

                response = requests.post(lastfm_endpoint, data=req_data)
                response = response.json()

                if not response:
                    continue

                last_track = response['recenttracks']['track'][0]

                # returning last played song for everyone
                # if last_track['@attr']['nowplaying'] != 'true':
                #     continue

                trackname = last_track['name']
                artist = last_track['artist']['#text']
                song = u"{} by {}".format(trackname, artist)

                out += person_status_template.format(name=person, song=song)
            except Exception, e:
                line_fail = sys.exc_info()[2].tb_lineno
                print("\tError: {} on line {}".format(repr(e), line_fail))

        return out