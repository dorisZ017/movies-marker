from datetime import datetime
import unittest
from sqlite3 import Cursor, Connection
from unittest import mock
from unittest.mock import Mock
import op_utils


class TestOperationUtils(unittest.TestCase):

    # Insert to database with the correct query
    @mock.patch("op_utils.get_conn")
    @mock.patch("op_utils.get_timestamp")
    def test_insert(self, dt_fn, conn_fn):
        cursor = Mock(Cursor)
        conn = Mock(Connection)
        conn_fn.return_value = conn, cursor
        dt_fn.return_value = datetime(2017, 2, 20, 7, 7, 3)
        params = {"title": "Some Title", "release_year": "2012", "operation": "bookmark"}
        op_utils.insert_operation(params)
        query = """INSERT INTO movie_operations 
    (title, release_year, timestamp, operation, operation_input) 
    VALUES 
    (
    "Some Title", 2012, "2017-02-20 07:07:03", "bookmark", "None"
    )"""
        cursor.execute.assert_called_with(query)

    # Read from database correctly
    @mock.patch("op_utils.get_conn")
    def test_get_bookmarked(self, conn_fn):
        cursor = Mock(Cursor)
        conn = Mock(Connection)
        cursor.fetchall.return_value = [["Some Title", 2012, "2017-02-20 07:07:03", "bookmark", ""]]
        conn_fn.return_value = conn, cursor
        res = op_utils.get_movies("bookmarked")
        self.assertEqual(res, [
            {"title": "Some Title", "release_year": 2012, "activity_time": "2017-02-20 07:07:03", "detail": "NA"}])

    @mock.patch("op_utils.get_conn")
    def test_get_rated(self, conn_fn):
        cursor = Mock(Cursor)
        conn = Mock(Connection)
        cursor.fetchall.return_value = [["Some Title", 2012, "2017-02-20 07:07:03", "rate", "5"]]
        conn_fn.return_value = conn, cursor
        res = op_utils.get_movies("rate")
        self.assertEqual(res, [
            {"title": "Some Title", "release_year": 2012, "activity_time": "2017-02-20 07:07:03", "detail": "5"}])

    # raise errors if the input is invalid
    def test_invalid_op(self):
        self.assertRaises(Exception, op_utils.insert_operation, {})
        self.assertRaises(Exception, op_utils.insert_operation,
                          {"title": "a", "release_year": 2020, "operation": "rate"})
        self.assertRaises(Exception, op_utils.get_movies, "boo")
