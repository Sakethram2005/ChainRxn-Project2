import hashlib
import json
import time
from flask import Flask, request, jsonify

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
        return new_block

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/addBlock', methods=['POST'])
def add_block():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'Missing data'}), 400

    new_block = blockchain.add_block(data)
    return jsonify({
        'index': new_block.index,
        'timestamp': new_block.timestamp,
        'data': new_block.data,
        'previous_hash': new_block.previous_hash,
        'hash': new_block.hash
    }), 200

@app.route('/getchain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'previous_hash': block.previous_hash,
            'hash': block.hash
        })
    return jsonify(chain_data), 200

@app.route('/getlatestblock', methods=['GET'])
def get_latest_block():
    block = blockchain.get_latest_block()
    return jsonify({
        'index': block.index,
        'timestamp': block.timestamp,
        'data': block.data,
        'previous_hash': block.previous_hash,
        'hash': block.hash
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
