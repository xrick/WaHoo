class IntentRecord():
    def __init__(self, intent_id, state_id):
        self.intent_id = intent_id
        self.user_paramenters = {}
        self.state_id = state_id