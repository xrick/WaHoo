import re
import json
#import Engine

REPLACE_FORMATE = '${{{0}}}'
RE_REPLACE_FORMATE = r'\$\{([^\$]*?)\}'
ANCHOR_FORMATE = '^{0}$'
_regex_keyword_list = []
TEST_TEXT = "小豆請倒數計時10秒"
TEST_TEXT2 = "小豆請幫第3組加5分"
#"小[豆|鬥|逗]|(倒數){1}|(計時)?|\d+|[秒|分]"
pattern1 = "小{bean}|.+|{counttime}|{quantity}|{timeunit}"
#小[豆|鬥|逗]|(\d+(小)[組|隊])|[加|多]|(\d|[分|點])
pattern2 = "小{bean}|.+|{quantity}|{addact}|{quantity}|{scoreunit}"
pattern_list = [("cmd1",pattern1),("cmd2",pattern2)]
keyword_list = [
    ("bean", "小[豆|鬥|逗]"), ("counttime", "(倒數){1}|(計時)?"), ("quantity", "\d+"), ("timeunit", "[秒|分]")
    , ("addcat", "[加|多]"), ("scoreunit", "(\d|[分|點])")
        ]
keword_dict = {1:"[{syn1}]|"}



def _extract_entities(user_input):
    return_entities_list = []
    #取得所有的regular expressions and domain
    for entities_type,reg in keyword_list:
        tmp_input_for_replace = user_input
        isfound = True
        #_reg = re.compile(reg)
        #while isfound:
        search_result = re.search(reg,tmp_input_for_replace).group()#_reg.search(tmp_input_for_replace)
        if search_result != None:
            tmp_input_for_replace = re.sub(reg,
                REPLACE_FORMATE.format(entities_type),
                tmp_input_for_replace,
                count=1
                )
            return_entities_list.append(
                    (entities_type, search_result[0]))
        else:
            isfound = False

    return return_entities_list

def main():
    retData = _extract_entities(TEST_TEXT)
    print(retData)
    #read the command from json
    #cmdJson = json.loads(open("habookcmd.json").read())["SpeechCmds"]
    #print(cmdJson)
    #rep_str = "this is a {test} string for {demo}"
    #pattern = "((早|晚)上?|(上|中|下)午)?(([0-2]?\d)|一|二|兩|三|四|五|六|七|八|九|十|十一|十二)(點|:)(半|([0-5]\d))?|現在"
    #print()
    
if __name__ == "__main__":
    main()
