from elasticsearch import Elasticsearch, helpers

from searchapp.constants import DOC_TYPE, INDEX_NAME
from searchapp.data import all_songs, SongData


def main():
    # Connect to localhost:9200 by default.
    es = Elasticsearch()

    es.indices.delete(index=INDEX_NAME, ignore=404)
    es.indices.create(
        index=INDEX_NAME,
        body={
            'mappings': {},
            'settings': {},
        },
    )

    bulk_index_songs(es, all_songs())
    #index_song(es, all_songs()[0])
    #for product in all_songs():
     #   index_songs(es, product)



def index_song(es, song: SongData):
    """Add a single song to the SongData index."""
    es.create(
        index=INDEX_NAME,
        doc_type=DOC_TYPE,
        id=song.id,
        body={
            "track_name_en": song.track_name_en,
            "track_name_si": song.track_name_si,
            "ranking": song.ranking,
            "track_rating": song.track_rating,
            "album_name_en": song.album_name_en,
            "album_name_si": song.album_name_si,
            "artist_name_en": song.artist_name_en,
            "artist_name_si": song.artist_name_si,
            "artist_rating": song.artist_rating,
            "lyrics": song.lyrics
        }
    )

    print("Indexed {}".format(song.track_name_en))

def bulk_index_songs(es, songs):

    actions = [
    {
        "_index": INDEX_NAME,
        "_type": DOC_TYPE,
        "_id": song.id,
        "_source": {
            "track_name_en": song.track_name_en,
            "track_name_si": song.track_name_si,
            "ranking": song.ranking,
            "track_rating": song.track_rating,
            "album_name_en": song.album_name_en,
            "album_name_si": song.album_name_si,
            "artist_name_en": song.artist_name_en,
            "artist_name_si": song.artist_name_si,
            "artist_rating": song.artist_rating,
            "lyrics": song.lyrics
        }
    }
    for song in songs
    ]

    helpers.bulk(es, actions)

    print("Bulk indexed all songs")

if __name__ == '__main__':
    main()
