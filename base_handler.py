#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2018 Freecnpro
#
# Author: Bill Wang <freecnpro@gmail.com>
# Created: 2018-02-02

from tornado import web
import json


class BaseHandler(web.RequestHandler):

    def response_with_plain(self, status_code=200, headers=None, chunk=None):
        self.set_status(status_code)
        if headers is None:
            headers = {'Content-Type': 'text/plain'}

        if headers:
            for name, value in headers.items():
                self.set_header(name, value)

        self.finish(chunk)

    def response_with_json(self, status_code=200, headers=None, chunk=None):
        self.set_status(status_code)
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        if headers:
            for name, value in headers.items():
                self.set_header(name, value)

        self.finish(json.dumps(chunk, separators=(',', ':')))

    def response(self, status_code=200, headers=None, chunk=None):
        self.set_status(status_code)

        if headers:
            for name, value in headers.items():
                self.set_header(name, value)

        self.finish(chunk)
