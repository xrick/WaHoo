class EngineQueryResult():
    def __init__(self, intent_id, prob, to_state_id, intent_parameters, entites):
        '''
            intent_id:int
            prob:
            entities :list of tupleL catched
            intent_parameter:dict, key:para_name(str) value:para_value(string)
            to_state_id:int
        '''
        self.intent_id = intent_id
        self.prob = prob
        self.to_state_id = to_state_id
        self.intent_parameters = intent_parameters
        self.entities = entites
