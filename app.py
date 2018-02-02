#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2018 Freecnpro
#
# Author: Bill Wang <freecnpro@gmail.com>
# Created: 2018-02-02

import tornado.web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line
from uuid import uuid4
import logging

from blockchain import Blockchain
from chain import ChainHandler
from mine import MineHandler
from transactions import NewTransactionHandler
from nodes import RegisterNodeHandler, ConsensusHandler

define("port", default=5000, help="run on the given port", type=int)
define("address", default="0.0.0.0", help="run on the bind address")

log = logging.getLogger('blockchain')
log.setLevel(logging.DEBUG)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/transactions/new/?', NewTransactionHandler),
            (r'/mine/?', MineHandler),
            (r'/chain/?', ChainHandler),
            (r'/nodes/register/?', RegisterNodeHandler),
            (r'/nodes/resolve/?', ConsensusHandler),
        ]

        node_identifier = str(uuid4()).replace('-', '')

        blockchain = Blockchain()

        settings = dict(
            node_identifier=node_identifier,
            blockchain=blockchain,
            debug=True
        )

        super(Application, self).__init__(handlers, **settings)


if __name__ == '__main__':
    parse_command_line()

    http_server = HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port, address=options.address)

    IOLoop.current().start()
