from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from typing import List

from searchapp.constants import DOC_TYPE, INDEX_NAME

HEADERS = {'content-type': 'application/json'}


class SearchResult:
    """Represents a song returned from elasticsearch."""

    def __init__(self, id_, track_name_si, track_name_en):
        self.id = id_
        self.track_name_si = track_name_si
        self.track_name_en = track_name_en

    def from_doc(doc) -> 'SearchResult':
        print(doc)
        return SearchResult(
            id_=doc.meta.id,
            track_name_en=doc.track_name_en,
            track_name_si=doc.track_name_si,
        )


def search(term: str, count: int, artist_name='', album_name='') -> List[SearchResult]:
    client = Elasticsearch()
    client.transport.connection_pool.connection.headers.update(HEADERS)

    s = Search(using=client, index=INDEX_NAME, doc_type=DOC_TYPE)
    filters = []

    if album_name.strip() != '':
        album_facet = {
            "match": {
                "album_name_si": {
                    "query": album_name,
                    'operator': 'and',
                    "fuzziness": "AUTO"
                }
            }
        }
        filters.append(album_facet)

    if artist_name.strip() != '':
        artist_facet = {
            "match": {
                "artist_name_si": {
                    "query": artist_name,
                    'operator': 'and',
                    "fuzziness": "AUTO"
                }
            }
        }
        filters.append(artist_facet)

    title_query = {
        "bool": {
            "must": [{
                "match": {
                    "track_name_si": {
                        "query": term,
                        'operator': 'and',
                        "fuzziness": "AUTO"
                    }
                }
            }],
            "filter": filters
        }
    }

    lyrics_query = {
        "bool": {
            "must": [{
                "match": {
                    "lyrics": {
                        "query": term,
                        'operator': 'and',
                        "fuzziness": "AUTO"
                    }
                }
            }],
            "filter": filters
        }
    }

    artist_query = {
        "bool": {
            "must": [{
                "match": {
                    "artist_name_si": {
                        "query": term,
                        'operator': 'and',
                        "fuzziness": "AUTO"
                    }
                }
            }],
            "filter": filters
        }
    }

    album_query = {
        "bool": {
            "must": [{
                "match": {
                    "album_name_si": {
                        "query": term,
                        'operator': 'and',
                        "fuzziness": "AUTO"
                    }
                }
            }],
            "filter": filters
        }
    }

    artist_facet_query = {
        "bool": {
            "must": [{
                "match": {
                    "artist_name_si": {
                        "query": artist_name,
                        'operator': 'and',
                        "fuzziness": "AUTO"
                    }
                }
            }],
            "filter": filters
        }
    }

    album_facet_query = {
        "bool": {
            "must": [{
                "match": {
                    "album_name_si": {
                        "query": album_name,
                        'operator': 'and',
                        "fuzziness": "AUTO"
                    }
                }
            }],
            "filter": filters
        }
    }

    dismax_query = {
        "dis_max": {
            "tie_breaker" : 0.7,
            "boost" : 1.2,
            "queries": [title_query, artist_query, album_query, lyrics_query],
        },
    }

    if term.strip() == '':
        dismax_query = {
            'dis_max': {
                'queries': [artist_facet_query, album_facet_query],
            },
        }
    

    songsWords = ['සින්දු', 'සිංදු', 'ගීත', 'ගී']
    if "ගේ" in term:
        for word in songsWords:
            if word in term:
                termSplit = term.split()
                if "ගේ" in termSplit:
                    termSplit.remove("ගේ")
                termSplit.remove(word)
                term = " ".join(termSplit)

                artist_query = {
                    "bool": {
                        "must": [{
                            "match": {
                                "artist_name_si": {
                                    "query": term,
                                    'operator': 'and',
                                    "fuzziness": "AUTO"
                                }
                            }
                        }],
                        "filter": filters
                    }
                }

                print(artist_query)
                docs = s.query(artist_query)[:count].execute()
                return [SearchResult.from_doc(d) for d in docs]

    if "උණුසුම්" in term or "හොඳම" in term or "ජනප්‍රිය" in term:
        termSplit = term.split()
        for word in termSplit:
            if word.isdigit():
                word = int(word )
                print(word)

                query_body = {
                    "aggs": {
                        "top_rank": {
                            "top_hits": {
                                "sort": [
                                    {"ranking": {
                                            "order": "asc"
                                        }
                                    }
                                ],
                                "size": word
                            }
                        }
                    }
                }

                print(query_body)
                docs = s.update_from_dict(query_body)[:word]
                return [SearchResult.from_doc(d) for d in docs]

    print(dismax_query)
    docs = s.query(dismax_query)[:count].execute()

    #docs = s.query(query)[:count].execute()

    return [SearchResult.from_doc(d) for d in docs]
