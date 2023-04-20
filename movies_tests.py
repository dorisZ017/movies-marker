import unittest
from unittest import mock
from unittest.mock import ANY
from attrdict import AttrDict
from elasticsearch_dsl import AttrList

import utils


class TestUtils(unittest.TestCase):

    def test_parse_imdb(self):
        url = "https://www.imdb.com/title/tt6718170/?pfblah"
        parsed_id = utils.get_id(url)
        self.assertEqual(parsed_id, "tt6718170")

    @mock.patch("requests.get")
    def test_fetch_movie(self, mock_get):
        mock_get.return_value.status_code = 200
        utils.parse_and_fetch("https://www.imdb.com/title/tt6718170/?pfblah", "xx")
        mock_get.assert_called_once_with(
            "http://www.omdbapi.com/",
            {'apikey': ANY, 'i': 'tt6718170'}
        )

    @mock.patch("requests.get")
    def test_error_handle(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "{error: boo}"
        res = utils.get_imdb_poster("https://www.imdb.com/title/tt6718170/?pfblah", "yy")
        self.assertEqual(res, "")

    def test_search_query(self):
        s = utils.build_search("some_title", year=2000)
        self.assertEqual(len(s.to_dict()["query"]["bool"]["must"]), 2)

    @mock.patch("utils.get_imdb_poster")
    def test_parse_movies(self, poster_fn):
        poster_fn.return_value = "some_url"
        resp = AttrDict({
            "hits": {
                "total": {
                    "value": 2,
                    "relation": "eq"
                },
                "hits": AttrList([
                    {
                        "_id": "1",
                        "_source": {
                            "title": "The Lord of the Rings: The Fellowship of the Ring",
                            "imdb_url": "some_url1",
                            "year": 2001
                        }
                    },
                    {
                        "_id": "2",
                        "_source": {
                            "title": "The Lord of the Rings: The Two Towers",
                            "imdb_url": "some_url2",
                            "year": 2002
                        }
                    }
                ])
            }
        })
        parsed = utils.parse_movie_list(resp, "some_api_key")
        expected = [
            {'_id': '1',
             '_source': {'imdb_url': 'some_url1',
                         'poster_url': 'some_url',
                         'title': 'The Lord of the Rings: The Fellowship of the Ring',
                         'year': 2001
                         }
             },
            {'_id': '2',
             '_source': {'imdb_url': 'some_url2',
                         'poster_url': 'some_url',
                         'title': 'The Lord of the Rings: The Two Towers',
                         'year': 2002}}
        ]
        self.assertEqual(parsed, expected)
