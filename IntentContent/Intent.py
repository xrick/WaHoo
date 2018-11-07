class Intent():
    def __init__(self, id, domain, initial_state_id, reply_dic, parameters):
        '''
            id: int, intent_id
            domain: string
            initial_state_id: int
            reply_dic: dic:{(int, int or None):string} note:(current_state_id, last_sate_id):reply
            parameters: List of IntentParameter
        '''
        self.id = id
        self.domain = domain
        self.initial_state_id = initial_state_id
        self.reply_dic = reply_dic
        self.parameters = parameters
