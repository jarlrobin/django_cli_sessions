from urllib.parse import urljoin, urlsplit


def get_list_columns(client, path):
    list_conf_response = client.django_request(
        method="get",
        path=path,
        json={"year": 2025},
    )

    list_conf = list_conf_response.json()
    list_columns = list_conf["columns"]

    # Ensure columns that are active by
    # default are set as such
    for key, val in list_columns.items():
        if val.get("defaultActive", False):
            val["active"] = True
    return list_columns


def get_list_data(
    client,
    path,
    columns=None,
    org_id: int = 1,
    page: int = 1,
    per_page: int = 100,
    search: str = "",
    extra_query_params: dict = {},
):
    # If columns are not specified manually
    # we set all columns to active
    if not columns:
        columns = get_list_columns(client, path)
        for key, val in columns.items():
            val["active"] = True

    # Tabula Rasa request dict
    request_dict = {
        "queryParams": {
            "org_id": org_id,
        },
        "state": {
            "columns": columns,
            "page": page,
            "perPage": per_page,
            "search": search,
        },
    }
    request_dict["queryParams"].update(extra_query_params)

    # Split and rejoin path to add 'data/'
    split_path = urlsplit(path)
    path = urljoin(split_path.path, "data/")

    list_response = client.django_request(
        method="post",
        path=path,
        params=split_path.query,
        json=request_dict,
    )
    return list_response
