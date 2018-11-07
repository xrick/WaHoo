class IntentParameter():
    def __init__(self, keyword_name, name, ask, max_num, re_ask, default_value, data_type):
        '''
            keyword_name: string 
            name: string 
            ask: string
            max_num: int
            re_ask: string or None
            default_value: string or None
            data_type: string
        '''
        self.keyword_name = keyword_name
        self.name = name
        self.ask = ask
        self.max_num = max_num
        self.re_ask = re_ask
        self.default_value = default_value
        self.data_type = data_type
