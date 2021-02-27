# -*- coding: utf-8 -*-
"""
Spyder Editor 

#To be installed
# Flask==0.12.2: pip install Flas==0
This is a temporary script file.
"""
import datetime
import hashlib
import json
import flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+ 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
