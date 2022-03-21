from blockchain_and_currency.helpers import hash256, encode_varint


class Transaction:
    def __init__(self, tx_ins, tx_outs, timestamp):
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.timestamp = timestamp

    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return 'tx: {}\ntx_ins:\n{}tx_outs:\n{}timestamp:\n{}'.format(self.id(), tx_ins, tx_outs, self.timestamp)

    def id(self):
        return self.hash().hex()

    def hash(self):
        return hash256(self.serialize())[::-1]

    def serialize(self):
        """Returns the byte serialization of the transaction input"""
        encode_varint()

