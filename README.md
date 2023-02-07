### titanium-white

Python3 library for interfacing with the [courtlistener](https://www.courtlistener.com/) API. 

### Installation
Source: 
``` 
git clone https://github.com/ctrl-schaff/titanium-white
cd ./titanium-white && pip install .
```

pypi: 
```
pip install titanium-white
```


### Usage
In order to interface with the API you'll have to provide an API token from courtlistener. After
you've generated your token you can construct a `CourtSession` instance to provide relevant
information for targetting a courtlistener endpoint

```
from titanium_white import CourtSession

mock_endpoint = "https://courtlistener.com/api/rest/v3/mock"
mock_api_key = "MOCK_API_KEY"
session_instance = CourtSession(
    endpoint=mock_endpoint,
    api_key=mock_api_key,
    headers={},
    parameters={},
)
```

With our `session_instance` we can use this to construct our `CourtListener` object and send a query
to the endpoint specified by `session_instance`

```
from titanium_white import CourtListener

listener_instance = CourtListener(court_session=session_instance)
query_response, query_request = listener_instance.get_query()
```

`get_query` will return both the response from the endpoint along with the prepared request object
for more in-depth inspection










