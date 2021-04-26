import os
from json import JSONDecodeError

import requests
from requests.exceptions import HTTPError, ConnectTimeout, ReadTimeout

url = "https://free.currconv.com/api/v7/convert"

params = {
    "compact": "ultra",
    "apiKey": os.getenv("CURRCONV_APIKEY")
}


class CorrConvError(Exception):
    pass


def convert(currency, to):
    symbols = f"{currency.upper()}_{to.upper()}"
    params.update({"q": symbols})
    try:
        response = requests.get(url, params=params, timeout=2)
        response.raise_for_status()
    except (HTTPError, ConnectTimeout, ReadTimeout) as e:
        raise CorrConvError(f"Can not connect to currency converter API: {str(e)}")
    try:
        return response.json().get(symbols)
    except JSONDecodeError as e:
        raise CorrConvError(f"There was a problem parsing data: {str(e)}")
