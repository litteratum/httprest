# httprest
`httprest` is a minimalistic framework for communicating with REST APIs.
Its goal is to reduce a boilerplate code required to communicate with APIs.
  * It has the `http` package exposing an HTTP client interface. There is also a client implementation that uses `urllib` under the hood. So no need to use extra libraries like `requests`
  * It has the `api.API` class which may be overridden and used to make API calls

## Usage
```python
from httprest import API

class MyAPI(API):
    def operation(self):
        result = self._request("POST", "/operation/endpoint", json={...})
        if result.ok:
            print(result.json)

api = MyAPI("http://api.com")
api.operation()
```

## Installation
```bash
pip install httprest
```


## HTTP client
The library exposes an `HTTPClient` interface.
There is also an `http.urllib_client.UrllibHTTPClient` implementation that is used by default.

You may define your own HTTP client like this:
```python
from httprest.http import HTTPClient, HTTPResponse

class MyHTTPClient(HTTPClient):
    def _request(...) -> HTTPResponse
```

And then you simply use it in the API client:
```python

api = MyAPI(..., http_client=MyHTTPClient())
```
