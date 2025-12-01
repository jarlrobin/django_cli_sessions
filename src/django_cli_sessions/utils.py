import json
import re


def load_json_file(filepath):
    """
    Load a JSON file
    """
    with open(filepath, "r") as infile:
        urls = json.load(infile)
    return urls


def index_by_name(endpoints):
    """
    Index Django endpoints by name
    """
    indexed_endpoints = {}
    for _endpoint in endpoints:
        name = _endpoint["name"]
        url = _endpoint["url"]
        _endpoint["format_string_mapper"] = create_format_string_mapper(
            find_format_strings_in_url(url)
        )

        if name in indexed_endpoints and "format" in url:
            indexed_endpoints[f"{name}-format"] = _endpoint
        else:
            indexed_endpoints[name] = _endpoint
    return indexed_endpoints


def index_by_module(endpoints):
    """
    Index Django endpoints by module
    """
    tmp_index = {}
    for _endpoint in endpoints:
        module = _endpoint["module"]
        if module in tmp_index:
            tmp_index[module].append(_endpoint)
        else:
            tmp_index[module] = [_endpoint]

    indexed_endpoints = {}
    for module, endpoints in tmp_index.items():
        indexed_endpoints[module] = index_by_name(endpoints)
    return indexed_endpoints


def index_by_app(endpoints):
    """
    Index Django endpoints by app
    """
    tmp_index = {}
    for _endpoint in endpoints:
        module = _endpoint["module"]
        module_split = module.split(".")
        app_label = module_split[0]
        if app_label in tmp_index:
            tmp_index[app_label].append(_endpoint)
        else:
            tmp_index[app_label] = [_endpoint]

    indexed_endpoints = {}
    for app_label, endpoints in tmp_index.items():
        indexed_endpoints[app_label] = index_by_name(endpoints)
    return indexed_endpoints


def find_format_strings_in_url(url_string):
    """
    Django show_urls gives URLS with a format
    string on the form <variable>

    This finds every occurence of those in a URL
    string
    """
    regex = re.compile("<[a-zA-Z_:]*>")
    return regex.findall(url_string)


def create_format_string_mapper(format_strings):
    """
    Create a mapper for format strings like

    {'id': '<id>'}
    """
    mapper = {}
    for format_string in format_strings:
        mapper[format_string[1:-1]] = format_string
    return mapper


def parse_endpoints_from_json(filepath):
    """
    Parse endpoints dumped by show_urls with JSON
    formatting into dicts
    """
    endpoints = load_json_file(filepath)
    indexed_endpoints = {
        "by_name": index_by_name(endpoints),
        "by_module": index_by_module(endpoints),
        "by_app": index_by_app(endpoints),
    }
    return indexed_endpoints
