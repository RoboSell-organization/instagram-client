import json

import requests
from requests import RequestException

from instagram_client.exceptions.http_exceptions import BadRequestApiException, UnexpectedServerApiException


class BaseAPI:
    def __init__(self, base_url: str):
        self.BASE_URL = base_url

    def _make_request(self, method: str, path: str, data: dict = None,
                      params: dict = None, headers: dict = None, reset_base_url: bool = False, form_encoded: bool = False) -> requests.Response:
        """
        A general method to make HTTP requests (GET, POST, etc.)

        This method abstracts the process of making HTTP requests, allowing for
        different types of requests (GET, POST, PUT, DELETE) to be easily performed
        by specifying the method and other parameters. This adheres to the DRY
        (Don't Repeat Yourself) principle by centralizing request handling.

        :param method: HTTP method to use for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE').
        :param path: The API endpoint path to which the request is made. This should be
                     relative to the base URL defined in the class.
        :param data: Optional dictionary containing the data to be sent in the body of
                     the request (used for POST and PUT requests). Default is None.
        :param params: Optional dictionary containing query parameters to be included
                       in the request URL. Default is None.
        :param headers: Optional dictionary containing any custom headers to be sent
                        with the request. Default is None.
        :return: Response object containing the server's response to the HTTP request.
        :raises APIException: Raises a custom APIException if the request fails for
                             any reason, including invalid HTTP methods, network issues,
                             or JSON parsing errors.

        The method constructs the full URL from the base URL and the provided path.
        It uses a dictionary to map HTTP methods to their respective request functions
        from the requests library. After making the request, it checks the response
        status and attempts to parse the response as JSON.
        """
        url = self.BASE_URL + path

        if reset_base_url:
            url = path

        try:
            request_methods = {
                'POST': requests.post,
                'GET': requests.get,
                'PUT': requests.put,
                'DELETE': requests.delete
            }

            if method not in request_methods:
                raise BadRequestApiException(f"Unsupported HTTP method: {method}")

            kwargs = {
                'params': params,
                'headers': headers,
                'data' if form_encoded else 'json': data
            }

            response = request_methods[method](url, **kwargs)

            data = response.json()

            if not (200 <= response.status_code < 300):
                error_message = data.get("message")
                if error_message is not None:
                    raise BadRequestApiException(error_message)

                raise UnexpectedServerApiException(f"Unexpected error occured: {response.text}")

            return response

        except RequestException as e:
            raise BadRequestApiException(f"Request failed: {e}") from e
        except (json.JSONDecodeError, ValueError) as e:
            raise BadRequestApiException(f"Failed to parse JSON: {e}") from e

    def _post(self, path: str, data: dict, headers: dict = None, params: dict = None, reset_base_url: bool = False, form_encoded: bool = False) -> requests.Response:
        return self._make_request('POST', path, data=data, headers=headers, params=params, reset_base_url=reset_base_url, form_encoded=form_encoded)

    def _get(self, path: str, params: dict = None, headers: dict = None, reset_base_url: bool = False, form_encoded: bool = False) -> requests.Response:
        return self._make_request('GET', path, params=params, headers=headers, reset_base_url=reset_base_url, form_encoded=form_encoded)

    def _put(self, path: str, params: dict = None, data: dict = None, headers: dict = None, reset_base_url: bool = False, form_encoded: bool = False) -> requests.Response:
        return self._make_request('PUT', path, params=params, data=data, headers=headers, reset_base_url=reset_base_url, form_encoded=form_encoded)

    def _delete(self, path: str, headers: dict = None, reset_base_url: bool = False, form_encoded: bool = False) -> requests.Response:
        return self._make_request('DELETE', path, headers=headers, reset_base_url=reset_base_url, form_encoded=form_encoded)
