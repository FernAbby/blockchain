#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2018 Freecnpro
#
# Author: Bill Wang <freecnpro@gmail.com>
# Created: 2018-02-02

import logging

from base_handler import BaseHandler

log = logging.getLogger('blockchain.chain')


class ChainHandler(BaseHandler):

    def get(self):
        blockchain = self.settings['blockchain']

        chunk = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }

        self.response_with_json(chunk=chunk)
