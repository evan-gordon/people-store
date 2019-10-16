# Module for wrapping default network request functionality
from requests import exceptions, codes
from typing import Tuple, Union

DEFAULT_TIMEOUT = 10

def get(session: any, endpoint, *, params=None,
        timeout=DEFAULT_TIMEOUT) -> Union[Tuple, any]:
  try:
    response = session.get(endpoint, params=params, timeout=timeout)
    if (codes.ok == response.status_code):
      return response
    else:
      return {
          'result': 'error',
          'status_code': response.status_code,
          'type': 'GET',
          'endpoint': endpoint,
          'params': params
      }
  except exceptions.Timeout:
    return {'result': 'error', 'reason': 'Timeout', 'endpoint': endpoint}
  except exceptions.ConnectionError:
    return {
        'result': 'error',
        'reason': 'Retry Failure',
        'endpoint': endpoint
    }
