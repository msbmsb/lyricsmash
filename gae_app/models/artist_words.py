"""
artist_words.py: 

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from google.appengine.ext import db

class ArtistWords(db.Model):
  name = db.StringProperty(required=True)
  words = db.TextProperty(required=True)
