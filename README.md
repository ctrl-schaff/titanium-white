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

###### Case 1 No Context Management
```
from titanium_white import CourtSession

mock_api_key = "MOCK_API_KEY"
session_obj = CourtSession(api_key=mock_api_key)

mock_endpoint = "https://courtlistener.com/api/rest/v3/mock"
response = session_obj.get_query(endpoint=mock_endpoint,
                                 headers={},
                                 parameters={})
...
```

`get_query` will return both the response from the endpoint along with the prepared request object
for more in-depth inspection


###### Case 2 Internal Context Management
```
from titanium_white import CourtSession

mock_api_key = "MOCK_API_KEY"
session_obj = CourtSession(api_key=mock_api_key)

endpoint_base = "https://courtlistener.com/api/rest/v3/"
endpoints = ["mock1", "mock2", "mock3"]

with CourtSession(api_key=mock_api_key) as session_obj:
    for endpoint in endpoints:
        full_endpoint = f"{endpoint_base}{endpoint}"
        response = session_obj.get_query(endpoint=full_endpoint,
                                         headers={},
                                         parameters={})
```
