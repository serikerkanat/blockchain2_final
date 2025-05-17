import json
from web3 import Web3
from solcx import compile_source

# Connect to local Ganache
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Compile the contract
compiled_sol = compile_source(
    '''
    pragma solidity ^0.8.0;

    contract Charity {
        struct Donation {
            address donor;
            uint256 amount;
            string recipient;
            string purpose;
            uint256 timestamp;
        }

        Donation[] public donations;
        mapping(address => uint256) public donorCounts;
        mapping(string => uint256) public recipientCounts;

        event DonationMade(address indexed donor, uint256 amount, string recipient, string purpose);

        function donate(string memory _recipient, string memory _purpose) public payable {
            require(msg.value > 0, "Donation amount must be greater than 0");
            
            donations.push(Donation({
                donor: msg.sender,
                amount: msg.value,
                recipient: _recipient,
                purpose: _purpose,
                timestamp: block.timestamp
            }));

            donorCounts[msg.sender]++;
            recipientCounts[_recipient]++;

            emit DonationMade(msg.sender, msg.value, _recipient, _purpose);
        }

        function getDonationCount() public view returns (uint256) {
            return donations.length;
        }

        function getDonation(uint256 _index) public view returns (address, uint256, string memory, string memory, uint256) {
            require(_index < donations.length, "Invalid donation index");
            Donation memory d = donations[_index];
            return (d.donor, d.amount, d.recipient, d.purpose, d.timestamp);
        }

        function getDonorCount(address _donor) public view returns (uint256) {
            return donorCounts[_donor];
        }

        function getRecipientCount(string memory _recipient) public view returns (uint256) {
            return recipientCounts[_recipient];
        }
    }
    ''',
    output_values=['abi', 'bin']
)

# Get the contract interface
contract_id, contract_interface = compiled_sol.popitem()

# Get bytecode and ABI
bytecode = contract_interface['bin']
abi = contract_interface['abi']

# Get the first account from Ganache
account = web3.eth.accounts[0]

# Create contract instance
Charity = web3.eth.contract(abi=abi, bytecode=bytecode)

# Build transaction
transaction = Charity.constructor().buildTransaction({
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei'),
    'from': account,
    'nonce': web3.eth.getTransactionCount(account)
})

# Sign transaction (in Ganache, we don't need private key)
signed_txn = web3.eth.account.signTransaction(transaction, private_key='YOUR_PRIVATE_KEY')

# Send transaction
print("Deploying contract...")
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(f"Transaction hash: {txn_hash.hex()}")

# Wait for transaction to be mined
txn_receipt = web3.eth.waitForTransactionReceipt(txn_hash)
print(f"Contract deployed at address: {txn_receipt.contractAddress}")

# Save contract details
contract_details = {
    'address': txn_receipt.contractAddress,
    'abi': abi
}

with open('contract_details.json', 'w') as f:
    json.dump(contract_details, f)

print("Contract details saved to contract_details.json")
