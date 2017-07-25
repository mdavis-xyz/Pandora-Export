#!/usr/bin/env python3
##
### This script was written by Matthew Davis in July 2017.
# It uses the Pandora library writte by Kevin Mehall <km@kevinmehall.net> and Christopher Eby <kreed@kreed.org>
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

# import requests
import json
import pprint as pp
import pandora
import getpass
# from multiprocessing import Pool
from io import StringIO 

class Exporter(object):

  def __init__(self):
    object.__init__(self)
    self.pan = pandora.Pandora()

  def login(self, userid, password):
    client = pandora.data.client_keys[pandora.data.default_client_id]
    print("Connecting ...")
    self.pan.connect(client, userid, password)
    print("Connected")

  def getLikes(self):

    print("Getting list of your stations")
    stations = self.pan.get_stations()
    print("Got list of station names")

    print("Looking up thumbs for each station")
    def getInfo(s):
      print("#", end="", flush=True)
      return s.get_info(extended=True)

    fullData = [getInfo(s) for s in stations]

    # This doesn't work, because something isn't picklable
    # with Pool(4) as self.pandora:
    #     fullData = self.pandora.map(lambda s:s.get_info(extended=True), stations)
    print("Got thumbs for each station")

    print('Formatting results')
    station_base = [s['music'] for s in fullData if 'music' in s]

    # likes = {y:[x[y] for x in likes_raw if y in x] for y in ['artists','genres','songs']}
    # dislikes = {y:[x[y] for x in dislikes_raw if y in x] for y in ['artists','genres','songs']}

    neatData = {
        'thumbsUp':{
            'artists':[],
            'songs':[],
            'genres':[]
        },
        'thumbsDown':{
            'artists':[],
            'songs':[],
            'genres':[]
        }
    }

    for x in station_base:
        if 'songs' in x:
            songs = [{'name':s['artistName'],'artist':s['artistName']} for s in x['songs']]
            neatData['thumbsUp']['songs'].extend(songs)
        if 'genres' in x:
            genres = [g['genreName'] for g in x['genres']]
            neatData['thumbsUp']['genres'].extend(genres)
        if 'artists' in x:
            artists = [a['artistName'] for a in x['artists']]
            neatData['thumbsUp']['artists'].extend(artists)

    for direction in ['thumbsUp','thumbsDown']:
        for station in fullData:
            if 'feedback' in station:
                for x in station['feedback'][direction]:
                    if 'songName' in x:
                        neatData[direction]['songs'].append({'name':x['songName'],'artist':x['artistName']})
                    else:
                        assert('artistName' in x)
                        neatData[direction]['artists'].append(x['artistName'])
    
    self.neatData = neatData
    self.fullData = fullData

  def getJson(self, filename):
    neatData = self.neatData
    fullData = self.fullData
    
    if filename == "full.json":
      theData = fullData
    elif filename == "neat.json":
      theData = neatData
    else:
      raise Exception("bad json name")

    io = StringIO()
    json.dump(theData, io)
    return io.getvalue()

  def save(self, fullFileName='full.json', neatFileName = 'neat.json'):
    neatData = self.neatData
    fullData = self.fullData

    # If you want the final output to be formatted a particular way
    # do that here
    print('Saving full neatData to file %s' % fullFileName)
    with open(fullFileName, 'w') as fp:
        json.dump(fullData, fp, indent=3)
    print('saved full neatData to %s' % fullFileName)

    print("Saving summarised neatData to file %s" % neatFileName)
    with open(neatFileName, 'w') as fp:
        json.dump(neatData, fp, indent=3)
    print('saved summarised data to %s' % neatFileName)

MAIN="__main__"

if __name__ == MAIN:
    exporter = Exporter()
    user = input("Enter your username (which is probably an email address)\n")
    pwd = getpass.getpass()
    exporter.login(user, pwd)
    exporter.getLikes()
    exporter.save()
    print('Done')
