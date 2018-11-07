import tornado.web
import tornado.httpserver
import json

from Chatbot.Chatbot import Chatbot

chat_bot = Chatbot()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/chatbot", ChatbotHandler),
        ]
        settings = {"template_path": 'templates'}
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class ChatbotHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            content = json.loads(self.request.body.decode('utf-8'))
            q = content['user_says']
            user_id = content['user_id']
            reply = chat_bot.interact(q, user_id)
            self.write(reply)
        except Exception as e:
            self.write(str(e))

if __name__ == "__main__":
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(5000)

    tornado.ioloop.IOLoop.instance().start()
