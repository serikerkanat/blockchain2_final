# Blockchain-based Voting System

A simple and secure voting system implemented using blockchain technology.

## Features

- Secure and transparent voting using blockchain
- Each vote is recorded immutably
- Prevents double voting
- Real-time vote counting
- Publicly verifiable results

## Installation

1. Install Node.js from https://nodejs.org/
2. Clone this repository
3. Install dependencies:
   ```
   npm install
   ```

## Running the Application

1. Start the server:
   ```
   npm start
   ```
2. The server will run on http://localhost:3000

## API Endpoints

- GET /blockchain - Get the current blockchain status
- POST /vote - Cast a vote (requires voterId and candidate in body)
- GET /results - Get current voting results
- GET /votes - Get all recorded votes

## Security Features

- Each vote is recorded in a blockchain block
- Immutable records prevent vote tampering
- Double voting is prevented through voter ID tracking
- All transactions are timestamped and hashed
