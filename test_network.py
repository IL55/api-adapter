from unittest.mock import MagicMock, patch
import unittest

from network import post_request

class Response:
  status_code = 404
  json_result = {}
  content = {}

  def __init__(self, status_code=404, json_result={}):
    self.status_code = status_code
    self.json_result = json_result

  def json(self):
    return self.json_result


class TestNetwork(unittest.TestCase):
  @patch("network.requests.post", MagicMock(return_value=Response(status_code = 404)))
  def test_post_request_failed_404(self):
    result = post_request("url", {"header": "ok"}, {"data": "1"})
    self.assertEqual(result, None)

  @patch("network.requests.post", MagicMock(return_value=Response(status_code=200, json_result={"data": "2"})))
  def test_post_request_200(self):
    result = post_request("url", {"header": "ok"}, {"data": "1"})
    self.assertEqual(result, {"data": "2"})

  @patch("network.requests.post", MagicMock(return_value=Response(status_code=201, json_result={"data": "2"})))
  def test_post_request_201(self):
    result = post_request("url", {"header": "ok"}, {"data": "1"})
    self.assertEqual(result, {"data": "2"})


