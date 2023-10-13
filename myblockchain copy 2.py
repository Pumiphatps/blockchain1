import datetime
import json
import hashlib
from flask import Flask , jsonify ,request


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction=0
        self.create_block(nonce=1, previous_hash="0")

    def create_block(self, nonce, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "nonce": nonce,
            "data":self.transaction,
            "previous_hash": previous_hash
            
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]
    def hash(self,block):
        encode_block=json.dumps(block,sort_keys=True).encode()
        #sha-256
        return hashlib.sha256(encode_block).hexdigest()
    def proof_of_work(self,previous_nonce):
        #หาค่า nonce 0000*****
        new_nonce=1
        check_proof = False

        #แก้โจทย์
        while check_proof is False:
            hashoperation=hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:4] =="0000":
                check_proof=True
            else:
                new_nonce +=1
        return new_nonce
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index<len(chain):
            block= chain[block_index]
            if block["previous_hash"] != self.hash(previous_block) :
                return False
            previous_nonce = previous_block["nonce"] #before
            nonce = block["nonce"] # nonce block now 
            hashoperation=hashlib.sha256(str(new_nonce**4 - previous_nonce**8).encode()).hexdigest()
            
            if hashoperation[:5] !="00001":
                return False
            previous_block=block
            block_index+=1
        return True
            
    #web server 
app =Flask(__name__)
#routing
blockchain = Blockchain()
@app.route('/')
def hello():
    return  "<p>Hello pumiphat</p>"
@app.route('/get_chain',methods=["GET"])
def get_chain():
    response={
        "chain":blockchain.chain,
        "length":len(blockchain.chain)
    }
    return jsonify(response),200
@app.route('/mining')
def mining_block():
    amount = 1000000
    blockchain.transaction = blockchain.transaction+amount
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    nonce = blockchain.proof_of_work(previous_nonce)
    previous_hash = blockchain.hash(previous_block)
    block=blockchain.create_block(nonce,previous_hash)
    response={
        "message":"mining block เสร็จ",
        "index" : block["index"],
        "timestamp": block["timestamp"],
        "data":block["data"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response),200
@app.route('/is_valid',methods=["GET"])
def is_vaild():
    is_vaild= blockchain.is_chain_valid(blockchain.chain)
    if is_vaild:
        response={"message": "blockcahin is valid"}
    else:
        response={"message": "have problem "}
    return jsonify(response),200

# Add Transaction:
@app.route('/add_transaction', methods=["POST"])
def add_transaction():
    data = request.get_json()
    sender = data["sender"]
    receiver = data["receiver"]
    amount = data["amount"]
    blockchain.transaction += amount
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    nonce = blockchain.proof_of_work(previous_nonce)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(nonce, previous_hash)
    response = {
        "message": "Transaction added successfully",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "data": block["data"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200
#Get Transaction History
@app.route('/get_transaction_history', methods=["GET"])
def get_transaction_history():
    response = {
        "transaction_history": blockchain.transaction
    }
    return jsonify(response), 200
# Get Balance
@app.route('/get_balance/<string:account>', methods=["GET"])
def get_balance(account):
    balance = blockchain.transaction if account == 'all' else 0
    response = {
        "account": account,
        "balance": balance
    }
    return jsonify(response), 200
# add custom to data
@app.route('/add_custom_data', methods=["POST"])
def add_custom_data():
    data = request.get_json()
    custom_data = data["custom_data"]
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    nonce = blockchain.proof_of_work(previous_nonce)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(nonce, previous_hash)
    block["custom_data"] = custom_data
    response = {
        "message": "Custom data added to the block",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "data": block["data"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"],
        "custom_data": block["custom_data"]
    }
    return jsonify(response), 200

if __name__=="__main__":
    app.run()
    
    
