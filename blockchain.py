#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2018 Freecnpro
#
# Author: Bill Wang <freecnpro@gmail.com>
# Created: 2018-02-02

import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n------------\n")

            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                print('==> False 1')
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], block['previous_hash']):
                print('==> False 2')
                return False

            last_block = block
            current_index += 1

        print('==> True')
        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network

        :return: True if chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grad and verify the chains from all the nodes in our network
        for node in neighbours:
            resp = requests.get(f'http://{node}/chain')

            if resp.status_code == 200:
                result = resp.json()
                length = result['length']
                chain = result['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discover a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Create a new transaction to go into the next mined Block

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block

        :param block: Block
        :return: The hash of the Block
        """
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm

        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        print(f'==> proof: {proof}')
        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
