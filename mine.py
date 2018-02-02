#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2018 Freecnpro
#
# Author: Bill Wang <freecnpro@gmail.com>
# Created: 2018-02-02

import logging

from base_handler import BaseHandler

log = logging.getLogger('blockchain.mine')


class MineHandler(BaseHandler):

    def get(self):
        # We run the proof of work algorithm to get the next proof...
        blockchain = self.settings['blockchain']
        node_identifier = self.settings['node_identifier']
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin.
        blockchain.new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=1
        )

        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        chunk = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }

        self.response_with_json(chunk=chunk)
