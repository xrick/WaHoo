from Chatbot.Chatbot import Chatbot

if __name__ == "__main__":
    bot = Chatbot()
    while True:
        question = input('Q:')
        answer = bot.interact(question, 'test_id')
        print('A:{0}'.format(answer))
