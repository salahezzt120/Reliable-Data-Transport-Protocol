# Reliable Data Transport Protocol Implementation
Alamein University  
Faculty of Computer Science & Engineering  
Course Code: CSE261 - Computer Networks  

![Project Banner](Screenshot 2024-12-06 135828.png)

## 📌 Project Overview
This project implements a **Reliable Data Transport Protocol (RDT)** over the UDP protocol, ensuring ordered and reliable delivery of data packets. It mimics TCP functionalities, including acknowledgments and retransmissions, and supports two RDT methods:
- **Stop-and-Wait**
- **Selective Repeat**

The project also simulates packet loss to test protocol reliability and includes performance analysis under varying network conditions.

## 🚀 Features
- Reliable data transfer over UDP.
- Packet loss simulation using configurable **Packet Loss Probability (PLP)**.
- Error detection using checksum (bonus feature).
- Performance comparison of Stop-and-Wait vs. Selective Repeat protocols.

## 📂 Repository Structure
Reliable-Data-Transport-Protocol/
├── client/
│   ├── client.py         # Client implementation
│   ├── client.in         # Input configuration file for the client
├── server/
│   ├── server.py         # Server implementation
│   ├── server.in         # Input configuration file for the server
├── utils/
│   ├── checksum.py       # Checksum implementation (bonus feature)
│   ├── logger.py         # Logging utility for packet losses and timeouts
├── tests/
│   ├── large_file.txt    # Example large file for testing
│   ├── test_results.md   # Testing results and observations
├── reports/
│   ├── analysis.md       # Comparison of Stop-and-Wait vs Selective Repeat
│   ├── instructions.md   # Instructions for running the project
│   ├── design_doc.md     # Design decisions and assumptions
├── README.md             # Project overview and setup instructions
├── requirements.txt      # Python dependencies
└── LICENSE               # License information (if applicable)

## 🛠️ How to Run
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Reliable-Data-Transport-Protocol.git
   cd Reliable-Data-Transport-Protocol

2. **Install Dependencies:
   ```bash
   pip install -r requirements.txt

4. **Run the Server:
   ```bash
   python server/server.py

6. **Run the  Client:
   ```bash
   python client/client.py
