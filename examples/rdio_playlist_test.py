#!/usr/bin/python 
import sys

from pyechonest.artist import Artist
from pyechonest.playlist import Playlist
from pyechonest.rdio import RdioCatalog

def process(artist_name):
    rdio = RdioCatalog('US')
    a = Artist(artist_name)
    p = Playlist(type="artist-radio", artist=a, buckets=[rdio.bucket_identifier(), 'tracks'])
    songs = p.get_next_songs(5)
    for s in songs:
        print "Found rdio track id: %s" % rdio.get_track_id(s)

def main():
    process(sys.argv[1])

if __name__ == "__main__":
    main()
