"""
lyricsmash.py:

Handler for lyricsmash

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from google.appengine.runtime import DeadlineExceededError
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os
import traceback
import time
import yaml
import logging
import urllib
import re

from markov_brain import Brain

from models.artist_words import ArtistWords

class LyricsmashHandler(webapp.RequestHandler):
  # GET
  def get(self):
    template_values = {
      'http_get': True,
      'artists': ArtistWords.all(keys_only=True).fetch(3100)
    }

    path = os.path.join(
      os.path.dirname(__file__), '..', 'templates', 'lyricsmash.html'
    )
    self.response.out.write(template.render(path, template_values))

  # POST
  def post(self):
    template_values = self.runLyricsmash(self.request.get('a0'), self.request.get('a1'), self.request.get('str'))

    path = os.path.join(
      os.path.dirname(__file__), '..', 'templates', 'lyricsmash.html'
    )
    self.response.out.write(template.render(path, template_values))

  def runLyricsmash(self, artist0, artist1, str_):
    if str_ is None or str_ == '':
      template_values = {
        'http_get': True,
        'error': "No text entered. Try again."
      }
      return template_values

    try:
      brain = Brain()
      artist_words0 = ArtistWords.get_by_key_name(artist0)
      if artist_words0:
        brain.remember(artist_words0.words.split())
      if artist0 != artist1:
        artist_words1 = ArtistWords.get_by_key_name(artist1)
        if artist_words1:
          brain2 = Brain()
          brain2.remember(artist_words1.words.split())
          brain.import_from(brain2.memory)
      result = self.format_result(brain.speak_about(str_, 640))

      template_values = {
        'http_get': False,
        'a0': artist0,
        'a1': artist1,
        'str': str_,
        'result': result,
        'artists': ArtistWords.all(keys_only=True).fetch(3100)
      }
    except DeadlineExceededError:
      template_values = {
        'http_get': True,
        'error': "The request has timed out, please try another."
      }

    return template_values

  def format_result(self, result):
    # 1. newlines at capitalized words
    retVal = re.sub(r'([A-Z][^\s]+\s)', r'<br />\1', result)
    retVal = re.sub(r'\sA\s', r'\sa\s', retVal)
    return retVal
