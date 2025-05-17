// blockchain.js
class Block {
    constructor(index, timestamp, data, previousHash = '') {
        this.index = index;
        this.timestamp = timestamp;
        this.data = data;
        this.previousHash = previousHash;
        this.hash = this.calculateHash();
    }

    calculateHash() {
        const crypto = require('crypto');
        return crypto.createHash('sha256')
            .update(this.index + this.previousHash + this.timestamp + JSON.stringify(this.data))
            .digest('hex');
    }
}

class Blockchain {
    constructor() {
        this.chain = [this.createGenesisBlock()];
        this.votes = {};
    }

    createGenesisBlock() {
        return new Block(0, new Date().toString(), { votes: [] }, "0");
    }

    getLatestBlock() {
        return this.chain[this.chain.length - 1];
    }

    addBlock(newBlock) {
        newBlock.previousHash = this.getLatestBlock().hash;
        newBlock.hash = newBlock.calculateHash();
        this.chain.push(newBlock);
    }

    isValid() {
        for (let i = 1; i < this.chain.length; i++) {
            const currentBlock = this.chain[i];
            const previousBlock = this.chain[i - 1];

            if (currentBlock.hash !== currentBlock.calculateHash()) {
                return false;
            }

            if (currentBlock.previousHash !== previousBlock.hash) {
                return false;
            }
        }
        return true;
    }

    addVote(voterId, candidate) {
        if (!this.votes[voterId]) {
            this.votes[voterId] = candidate;
            const newBlock = new Block(
                this.chain.length,
                new Date().toString(),
                { voterId, candidate }
            );
            this.addBlock(newBlock);
            return true;
        }
        return false;
    }

    getResults() {
        const results = {};
        this.chain.forEach(block => {
            if (block.data.voterId && block.data.candidate) {
                const candidate = block.data.candidate;
                results[candidate] = (results[candidate] || 0) + 1;
            }
        });
        return results;
    }
}

// Export the Blockchain class
module.exports = Blockchain;