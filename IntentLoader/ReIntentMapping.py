class ReIntentMapping():
    def __init__(self, re, intent_id, from_state_id, to_state_id):
        '''
            re: string
            intent_id: int
            parameters: dic:{int:string}
            from_state_id: int
            to_state_id: int
        '''
        self.re = re
        self.intent_id = intent_id
        self.from_state_id = from_state_id
        self.to_state_id = to_state_id