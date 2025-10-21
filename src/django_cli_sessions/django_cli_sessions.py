from http import HTTPStatus

import requests

from django_cli_sessions import utils


class DjangoCLISession:
    """
    """
    def __init__(self, url='', init_path='', login_path='',
                 username=None, password=None):
        self.url = url if url else 'http://localhost'
        self.username = username
        self.password = password

        self.session = requests.session()
        self.init_url = f'{self.url}/{init_path}'
        self.login_url = f'{self.url}/{login_path}'

        self.login()

    def login(self):
        """
        Login to the Django site
        """
        login_data = {
            'username': self.username,
            'password': self.password,
        }
        init_response = self.session.get(self.init_url)

        if init_response.status_code != HTTPStatus.OK:
            error_msg = ('Initialisation failed, ',
                         f'error {init_response._content}')
            raise ValueError(error_msg)

        login_response = self.session.post(url=self.login_url,
                                           json=login_data,
                                           headers=self.get_headers())
        if login_response.status_code != HTTPStatus.OK:
            error_msg = (f'Login failed, error {login_response._content}, ',
                         f'status_code {login_response.status_code}')
            raise ValueError(error_msg)

    def get_headers(self):
        """
        """
        return {"X-CSRFToken": self.session.cookies.get("csrftoken", '')}

    def django_request(self, method, path, *args, **kwargs):
        """
        """
        api_url = f'{self.url}/{path}'
        headers= self.get_headers()
        if "extra_headers" in kwargs:
            custom_headers = kwargs.pop("extra_headers")
            headers.update(custom_headers)
        return getattr(self.session, method)(api_url, *args, **kwargs,
                                             headers=headers)


class DjangoCLISessionWithEndpoints(DjangoCLISession):
    """
    """
    def __init__(self, url='', init_path='', login_path='',
                 username=None, password=None, filepath=None):
        if not filepath:
            raise ValueError('No filepath provided')

        super().__init__(url=url, init_path=init_path, login_path=login_path,
                         username=username, password=password)

        self.filepath = filepath
        self.endpoints = utils.parse_endpoints_from_json(self.filepath)
        self.endpoints_by_name = self.endpoints['by_name']
        self.endpoints_by_module = self.endpoints['by_module']
        self.endpoints_by_app = self.endpoints['by_app']


    def format_url_variables(self, endpoint_details, variables):
        """
        Format URL variables based on the mapper
        created from the URL details in the JSON

        Formats a URL like:
            /users/get/<pk>/
        To:
            /users/get/1/
        """
        format_string_mapper = endpoint_details['format_string_mapper']
        if format_string_mapper.keys() != variables.keys():
            raise ValueError('Variables do not match')

        url = endpoint_details['url']
        for key, val in variables.items():
            format_string = format_string_mapper[key]
            url = url.replace(format_string, str(val))
        return url
