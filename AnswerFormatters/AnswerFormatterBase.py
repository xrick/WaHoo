import json
import os
import urllib.request

import config


class AnswerFormatterBase:

    def __init__(self):
        self._internal_service_uri_base = config.INTERNAL_SERVICE_URI_BASE
        self._internal_service_token = config.INTERNAL_SERVICE_TOKEN
        if config.ENABLE_PROXY:
            proxy_uri = config.PROXY_URI
            proxy_support = urllib.request.ProxyHandler({'http': proxy_uri})
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)

    def _query_external_api(self, query_uri):
        with urllib.request.urlopen(query_uri) as response:
            contents = response.read()
        contents = contents.decode('utf8')
        return contents

    def _query_external_api_json(self, query_uri):
        contents = self._query_external_api(query_uri)
        contents = json.loads(contents)
        return contents

    def _formate_to_dict(self, answer, action):
        """        
        Arguments:
            answer {string} -- [description]
            action {dict} -- ex:{action:'open_web',url:'...'}
        Return: dict
        """
        return {'output': answer, 'action': action}
