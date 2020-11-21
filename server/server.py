#!/usr/bin/env python
# -*- coding:utf-8 -*-
import signal
import settings
import router
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.web
from utils.db.db_manage import init_mysql_db

def handle_signal(server):

    def _shutdown():
        server.stop()

    def _sig_term_handler(sig, frame):
        tornado.ioloop.IOLoop.instance().add_callback(_shutdown)

    signal.signal(signal.SIGTERM, _sig_term_handler)


if __name__ == '__main__':
    application = tornado.web.Application(router.ROUTER, **settings.SETTINGS)
    server = tornado.httpserver.HTTPServer(application,
                                           max_body_size=settings.MAX_BODY_SIZE,
                                           xheaders=True)

    if settings.SETTINGS['debug'] or settings.SETTINGS['autoreload']:
        server.listen(11002)
        server.start(1)
    else:
        server.bind(11002)
        server.start(1)

    init_mysql_db()

    tornado.ioloop.IOLoop.instance().start()
    handle_signal(server)



