#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2018 Freecnpro
#
# Author: Bill Wang <freecnpro@gmail.com>
# Created: 2018-02-02

import json
import logging

from base_handler import BaseHandler

log = logging.getLogger('blockchain.nodes')


class RegisterNodeHandler(BaseHandler):

    def post(self):
        try:
            data = json.loads(self.request.body)

            nodes = data.get('nodes')
            if nodes is None:
                self.response_with_json(status_code=400, chunk={'errmsg': 'please supply a valid list of nodes'})
                return

            blockchain = self.settings['blockchain']

            for node in nodes:
                blockchain.register_node(node)

            chunk = {
                'message': f'New nodes have been added',
                'total_nodes': list(blockchain.nodes)
            }

            self.response_with_json(status_code=201, chunk=chunk)
        except ValueError:
            self.response_with_json(status_code=400, chunk={'errmsg': 'only accept json'})
        except Exception as e:
            log.warning("RegisterNodeHandler: %r", e)
            self.response_with_json(status_code=500, chunk={'errmsg': 'server internal error'})


class ConsensusHandler(BaseHandler):

    def get(self):
        blockchain = self.settings['blockchain']

        replaced = blockchain.resolve_conflicts()

        if replaced:
            chunk = {
                'message': 'Our chain was replaced',
                'new_chain': blockchain.chain
            }
        else:
            chunk = {
                'message': 'Our chain is authoritative',
                'chain': blockchain.chain
            }

        self.response_with_json(chunk=chunk)
