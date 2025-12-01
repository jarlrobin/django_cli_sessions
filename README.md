# Django CLI Sessions

Personal project to make a CLI session client that can be used in `ipython` shells.


Example usage:

```python
from django_cli_sessions.django_cli_sessions import DjangoCLISessionClientWithEndpoints
client = DjangoCLISessionWithEndpoints(
    url="http://localhost/",
    init_path="api/auth/init/",
    login_path="api/auth/login/",
    username="username",
    password="password",
    filepath="/path/to/json/with/urls.json",
)
```

The `client` can now be used to make requests to your application, this is an example for a hypothetical endpoint giving details about a user:

``` python
endpoint_details = client.endpoints_by_app["auth"]["auth-user-detail"]
path = client.format_path_variables(endpoint_details, {"pk": 1})
response = client.django_request(
    method="get",
    path=path,
)
```


Creating the JSON file with URLs:

(This requires [django-extensions](https://django-extensions.readthedocs.io/en/latest/))
``` shell
./manage.py show_urls --format=pretty-json > urls.json
```
Note: The first line in `urls.json` might be something like `2025-12-01 15:29.40 [info     ] debug mode: False`, which is from the management command, make sure to remove it before trying to parse the JSON.
