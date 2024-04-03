# Simple Blockchain Project

This blockchain project serves as an educational tool to explore the basic principles and implementation details of blockchain technology. It is designed to be accessible and easy to set up, either on a Raspberry Pi or within a development environment such as Visual Studio Code.

## Prerequisites

Before you start, ensure you know your IP address. This is crucial for setting up nodes on different devices. If you're running the blockchain on your local device, the default IP address will be `127.0.0.1`, which refers to localhost.

### Configuring Nodes

If you plan to run the blockchain across multiple devices, you will need to edit the `testrun.py` file to specify the nodes:

```python
pis = [('your_ip_address', your_port_number)]
# Add as many nodes as you require
```

Ensure you have Python 3.9 installed on your machine, as this project relies on that specific version. This version compatibility must be considered when setting up your development environment.

## Setup and Installation

Follow these steps to get your blockchain environment ready:

1. **Clone the Repository**

   From your terminal or command line, clone the repo to your local machine:

   ```
   git clone <repository_url>
   ```

2. **Create a Virtual Environment**

   With Python 3.9, create a virtual environment in your project directory:

   ```
   python3.9 -m venv block
   ```

3. **Activate the Virtual Environment**

   - On Linux or macOS:
     ```
     source block/bin/activate
     ```
   - On Windows (Visual Studio Code):
     ```
     block\Scripts\activate
     ```

4. **Install Dependencies**

   Install the required Python packages as specified in the `requirements.txt` file:

   ```
   pip install -r requirements.txt
   ```

## Running the Blockchain

1. **Start the First Node**

   To run the first node on your main device, execute:

   ```
   python full_node.py --port=8000 --ip=your_ip_address --mine=1
   ```

2. **Start Additional Nodes**

   For each additional device, start a node by specifying its own port and the first node's IP address and port:

   ```
   python full_node.py --port=8001 --ip=your_ip_address --node=first_node_ip:8000 --mine=1
   ```

3. **Viewing Block Information**

   To display the blockchain data, run:

   ```
   python testrun.py
   ```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

```
MIT License

Copyright (c) 2023 <Team 14>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
