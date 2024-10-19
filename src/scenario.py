# scenario.py

class Scenario:
    def __init__(self, name):
        self.name = name
        self.url = None
        self.method = None
        self.headers = {}
        self.body = None
        self.save_variable = None

    def set_url(self, url):
        self.url = url
        return self

    def set_method(self, method):
        self.method = method.upper()
        return self

    def set_headers(self, headers):
        if headers:
            if isinstance(headers, dict):
                self.headers = headers
            elif isinstance(headers, str):
                headers_dict = {}
                for line in headers.strip().split('\n'):
                    if line:
                        key, value = line.split(':', 1)
                        headers_dict[key.strip()] = value.strip()
                self.headers = headers_dict
        else:
            self.headers = {}
        return self

    def set_body(self, body):
        self.body = body if body else None
        return self

    def save(self, variable_name):
        self.save_variable = variable_name
        return self
