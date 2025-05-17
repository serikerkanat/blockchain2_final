const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const Blockchain = require('./blockchain.js');

const app = express();
const blockchain = new Blockchain();

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(__dirname));
app.get('/', (req, res) => {
    res.json({
        message: "Welcome to Blockchain Voting System",
        endpoints: {
            "/vote": "POST - Cast a vote",
            "/results": "GET - Get voting results",
            "/blockchain": "GET - Get blockchain status",
            "/votes": "GET - Get all votes"
        }
    });
});
// Get blockchain status
app.get('/blockchain', (req, res) => {
    res.json({
        chain: blockchain.chain,
        isValid: blockchain.isValid()
    });
});

// Cast a vote
app.post('/vote', (req, res) => {
    const { voterId, candidate } = req.body;
    
    if (!voterId || !candidate) {
        return res.status(400).json({ error: 'Missing voterId or candidate' });
    }

    const success = blockchain.addVote(voterId, candidate);
    
    if (success) {
        res.json({ message: 'Vote successfully cast', block: blockchain.getLatestBlock() });
    } else {
        res.status(400).json({ error: 'Voter has already cast a vote' });
    }
});

// Get voting results
app.get('/results', (req, res) => {
    res.json(blockchain.getResults());
});

// Get all votes
app.get('/votes', (req, res) => {
    res.json(blockchain.votes);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Blockchain Voting System running on port ${PORT}`);
});

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});