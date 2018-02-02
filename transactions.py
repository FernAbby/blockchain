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

log = logging.getLogger('blockchain.transactions')


class NewTransactionHandler(BaseHandler):

    def post(self):
        try:
            data = json.loads(self.request.body)

            # Check that the required fields are in the POST's data
            required = ['sender', 'recipient', 'amount']
            if not all(k in data for k in required):
                self.response_with_json(status_code=400, chunk={'errmsg': 'missing values'})
                return

            # Create a new Transaction
            blockchain = self.settings['blockchain']

            index = blockchain.new_transaction(data['sender'], data['recipient'], data['amount'])

            chunk = {
                'message': f'Transaction will be added to Block {index}'
            }

            self.response_with_json(status_code=201, chunk=chunk)
        except ValueError:
            self.response_with_json(status_code=400, chunk={'errmsg': 'only accept json'})
        except Exception as e:
            log.warning("NewTransactionHandler: %r", e)
            self.response_with_json(status_code=500, chunk={'errmsg': 'server internal error'})
