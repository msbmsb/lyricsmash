"""
loaddb.py:
Handler for loading and reinitializing the data store.

* Author: Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License: MIT License: http://creativecommons.org/licenses/MIT/
"""

from google.appengine.runtime import DeadlineExceededError
from google.appengine.ext import webapp
from google.appengine.ext import db

import os
import sys
from models.artist_words import ArtistWords

class LoadDbHandler(webapp.RequestHandler):
  def get(self):
    clear = self.request.get('clear')
    if clear:
      past_words = db.GqlQuery("SELECT * FROM ArtistWords")
      for pastw in past_words:
        pastw.delete()
      self.response.out.write('Cleared DB<br />')

    self.response.out.write('Loading DB<br />')
    try:
      self.loaddb()
      self.response.out.write('Saved all data.<br />')
    except DeadlineExceededError:
      self.response.out.write('Saved some data, try again.<br />')

  def post(self):
    self.response.out.write('Try again<br />')

  def loaddb(self):
    # load every artist file
    for subdir, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), "../data/")):
      for f in files:
        if ArtistWords.get_by_key_name(f):
          self.response.out.write('Skipping ')
          continue
        try:
          path = os.path.join(
            os.path.dirname(__file__), "../data/" + f
          )
          df = open(path, 'r')
        except IOError:
          continue
        else:
          aname = unicode(df.readline().rstrip(), 'utf-8')
          lyr = ArtistWords(key_name=aname, name=aname, words=unicode(df.read(), 'utf-8'))
          lyr.put()
          df.close()
