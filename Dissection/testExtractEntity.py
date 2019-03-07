import re
import json

REPLACE_FORMATE = '${{{0}}}'
RE_REPLACE_FORMATE = r'\$\{([^\$]*?)\}'
ANCHOR_FORMATE = '^{0}$'
_regex_keyword_list = []

def _extract_entities(self, user_input):
    return_entities_list = []
    for reg, entities_type in _regex_keyword_list:
        tmp_input_for_replace = user_input
        isfound = True
        while isfound:
            search_result = reg.search(tmp_input_for_replace)
            if search_result != None:
                tmp_input_for_replace = reg.sub(
                    REPLACE_FORMATE.format(entities_type),
                    tmp_input_for_replace,
                    count=1
                )
                return_entities_list.append(
                        (entities_type, search_result[0]))
            else:
                isfound = False

    return return_entities_list

