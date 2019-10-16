from requests import codes, Session
from web.url import get
import pytest
GOOGLE = 'https://www.google.com'

def test_can_call_api():
  result = get(Session(), GOOGLE)
  assert result.status_code == codes.ok

def test_low_timeout_returns_error():
  result = get(Session(), GOOGLE, timeout=0.0001)
  assert result['result'] == 'error'
  assert result['reason'] == 'retry_failure'