# Secured-voting-system-using-blockchain
![Voting System Screenshot](static/images/login.png)

# Blockchain Voting System

### Summary

A decentralized voting system built on a blockchain to ensure transparency, security, and immutability in voting records. This system allows multiple nodes to cast votes, share blockchain updates, and achieve consensus, making it ideal for secure online voting applications. The project initially integrated MongoDB to store voter information but has been modified to use static data for local testing and ease of setup.

---

### Features

- **Decentralized Network**: Operates across multiple nodes, ensuring no single point of failure.
- **Immutable Ledger**: All votes are securely stored on a blockchain, making records tamper-resistant.
- **Automatic Peer Discovery**: Each node can register with existing nodes, forming a connected network.
- **Consensus Mechanism**: Nodes validate and synchronize with the longest blockchain to ensure consistency.
- **RESTful API**: Interact with the voting system via HTTP endpoints for easy integration and testing.
- **MongoDB (Optional)**: Initially used for voter information storage, now replaced with static data for local testing.

---

### Technology Used

- **Python**: Core language for building the application logic.
- **Flask**: Lightweight web framework to handle API requests.
- **MongoDB (Optional)**: Initially integrated for storing voter information.
- **Postman**: Tool for testing API endpoints.
- **JSON**: Data format for data exchange across nodes.

---

### To Run This App, Follow the Steps Below

1. **Clone the repository** from GitHub:
   ```bash
   git clone https://github.com/yourusername/blockchain-voting-system.git

