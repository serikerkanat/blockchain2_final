from flask import Flask, request, jsonify, render_template
from blockchain import CharityBlockchain
from datetime import datetime

app = Flask(__name__)
blockchain = CharityBlockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donate', methods=['POST'])
def donate():
    data = request.json
    required = ['donor', 'amount', 'recipient', 'purpose']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400

    block = blockchain.add_transaction(
        donor=data['donor'],
        amount=amount,
        recipient=data['recipient'],
        purpose=data['purpose']
    )
    
    return jsonify({
        'message': 'Transaction successful',
        'block': block.data
    })

@app.route('/transactions', methods=['GET'])
def get_transactions():
    donor = request.args.get('donor')
    recipient = request.args.get('recipient')
    history = blockchain.get_transaction_history(donor, recipient)
    return jsonify(history)

@app.route('/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return jsonify({'is_valid': is_valid})

if __name__ == '__main__':
    app.run(debug=True)
