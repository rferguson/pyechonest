#!/usr/bin/env python
# encoding: utf-8

"""
Created by Rob Ferguson on May 5, 2013

This file contains convenience methods for working with the Rdio API
"""
import logging

from pyechonest.song import Song
from pyechonest.util import EchoNestException

class EchoNestAPICodes:
  Unknown_Error = -1
  Success = 0
  Invalid_API_Key = 1
  Insufficient_Rights = 2
  Rate_Limit_Exceeded = 3
  Missing_Parameter = 4
  Invalid_Parameter = 5

class RdioCatalog(object):
  """
  A convenience class to make calls to The Echo Nest API with Rdio Results
  """
  def __init__(self, region):
    """
    @param self.region: The Rdio catalog to call against, e.g. rdio-US (restrict to the US) or rdio-WW (all rdio catalogs)
    @return: A convenience class to make API calls to The Echo Nest with results from the Rdio Catalog.
    """
    self.region = region

  def rdio_identifier(self):
    """
    @return: Identification for the Rdio Catalog in 'self.region' country
    """
    return "rdio-%s" % self.region

  def artist_identifier(self, rdio_artist_key):
    """
    @param rdio_artist_key: Rdio artist key e.g. r91318 (Radiohead)

    @return: Format to identify an artist with an Rdio Key e.g. rdio-US:artist:r91318
    """
    return "%s:artist:%s" % (self.rdio_identifier(), artist_key)

  def bucket_identifier(self):
    """
    @return: Convenience to specify the Rdio id space.
    """
    return "id:%s" % self.rdio_identifier()

  def track_identifier(self, rdio_track_key):
    """
    @return: Format to identify a track with an Rdio Key e.g. rdio-US:track:t2062705 (Airbag)
    """
    return "%s:track:%s" % (self.region, rdio_track_key)

  def get_artist_key(self, echo_artist_object):
    """
    @param echo_artist_object: Pyechonest Artist object
    @return: An Rdio artist key (string version) from an EchoNest Artist.
    """
    try:
      # Call API
      identifier, category, id = echo_artist_object.get_foreign_id(self.rdio_identifier()).split(':')

      if not identifier == self.rdio_identifier() or not category == "artist":
        logging.error("Expected %s got %s, category %s" % (self.region, identifier, category))

      return id
    except EchoNestException as e:
      if e == EchoNestAPICodes.Invalid_Parameter:
        logging.exception("Echonest failed artist lookup: %s", echoartist)
        return None
      raise EchoNestException(e)
    except AttributeError:
      # Should not happen, but does in practice.
      return None

  def get_track_key(self, echonest_song_object):
    """
    @param echonest_song_object:  A Pyechonest Song object.
    @return: An Rdio track key
    """
    try:
      playback_dict = echonest_song_object.get_tracks(self.rdio_identifier())[0]
      identifier, category, id = playback_dict['foreign_id'].split(':')

      if not identifier == self.rdio_identifier() or not category == "track":
        logging.error("Expected %s got %s, category %s" % (self.region, identifier, category))
        return None
      return id

    except IndexError:
      logging.info("EchoNest track did not map to an Rdio track: %s" % echonest_song_object)
      return None

