# usage:
#
# python app.py start
# python app.py stop
#

import json

from daemon import runner  # pip install python-daemon
from tornado import websocket, web, ioloop

subs = {}

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, channel_id):
        if channel_id:
            if channel_id not in subs:
                subs[channel_id] = []
            if self not in subs[channel_id]:
                subs[channel_id].append(self)

    def on_close(self):
        for i in subs.keys():
            if self in subs[i]:
                subs[i].remove(self)
                break


class ApiHandler(web.RequestHandler):
    @web.asynchronous
    def post(self, *args):
        self.finish()
        channel_id = self.get_argument("channel")
        # data = json.dumps({
        #        "answer": self.get_argument("answer"),
        #    })
        data = self.get_argument("answer")
        if channel_id in subs:
            for c in subs[channel_id]:
                c.write_message(data)


# daemon stuff
class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/ask_tornado.pid'
        self.pidfile_timeout = 5

    def run(self):
        app = web.Application([
            (r'/ws/([0-9]*)$', SocketHandler),
            (r'/push', ApiHandler),
        ])
        app.listen(8888)
        ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    tornado_daemon = App()
    daemon_runner = runner.DaemonRunner(tornado_daemon)
    daemon_runner.do_action()
