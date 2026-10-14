# Overview

My goal with this project was to gain a hands-on understanding of network transport protocols and port-binding rules without relying on web frameworks like FastAPI or Flask, which handle network tasks automatically. By developing directly against the built-in socket layer, I aimed to learn how data travels across network layers and establish a communication channel that can be later integrated into a microservice architecture.

This software consists of a dual-script system written in Python that enables real-time communication using TCP. 
*   **The Server (`server.py`)** acts as a database controller. It runs continuously, listening for a specific matching request phrase from a client. When it receives that phrase, it verifies the file location on the hard drive, reads the text database file, and streams that content across the network pipeline.
*   **The Client (`client.py`)** acts as an interactive control panel. It connects directly to the server, allows the user to select a command from a terminal menu, and handles sending and receiving the text data packages.

### How to Run the Software

To run this project, open two separate terminal windows side-by-side:

1. **Start the Server First**: In your left terminal window, navigate to your project directory and start the listener script:
   ```bash
   python server.py
   ```
   The server will run a quick automated check to confirm the text database file exists, open up local port 9000, and wait for a client to connect.

2. **Launch the Interactive Client Menu**: In your right terminal window, start the client script:
   ```bash
   python client.py
   ```
   A terminal menu will display on your screen. Enter 1 to pull the text database contents across the network, 2 to send an invalid test command to verify error handling, or 3 to shut the client down.

The big-picture purpose of building this tool was to create a communication layer using TCP. Eventually, this will allow an external file-monitoring tool (like a background folder watcher written in Rust) to tell a Python backend processor exactly when a new file has arrived.

[Software Demo Video](https://youtu.be/43J5HmC0Mf8)

# Network Communication

This software utilizes a **Client-Server Architecture**. In this layout, the server waits to receive incoming connection handshakes, processes user commands against its local data layer, and sends structured text responses right back over the network line.

The system is based on the **Transmission Control Protocol (TCP)** at the transport layer for data integrity, ordered packet arrival, and error-checked stream processing. By default, the software connects over local port **9000** using the standard loopback IP address (`127.0.0.1`).

The messages sent back and forth rely on an application data structure. The client sends a clear text string command (`FETCH_DATABASE_INVENTORY`) encoded into standard UTF-8 network bytes. The server instantly decodes the bytes, reads the local text registry file (`local_data_pantry.txt`), and streams that plain-text data back to the client to be displayed on your screen.

# Development Environment

The entire project was built using **Visual Studio Code** as the main code editor. Running multiple command terminals side-by-side within VS Code made it easy to watch the client and server talk to each other and monitor loopback connections in real time.

The software is written in **Python 3**. No web frameworks, external packages, or dependencies were used. The project runs using only two built-in standard Python modules:
*   `socket`: Used to configure TCP/IP connections, handle port address reuse rules (`SO_REUSEADDR`), and stream messages back and forth across network channels.
*   `os`: Used by the server component to perform file checks on your hard drive before initiating text-reading workflows.

# Useful Websites

- [Real Python: Socket Programming in Python Guide](https://realpython.com/python-sockets/)
- [GeeksforGeeks: Socket Programming Basics in Python](https://www.geeksforgeeks.org/python/socket-programming-python/)
- [Python Standard Library: Official Socket Module Documentation](https://python.org)

# Future Work

* **Introduce Multi-Client Support**: Upgrade the server's main processing loop to handle multiple incoming client requests at the same time using asynchronous code (`asyncio`) or background thread pooling.
* **Add JSON Serialization and Structure**: Upgrade the message system from raw, simple text strings to a formalized JSON packet structure to handle advanced metadata and custom response keys.
* **Build Cross-Language Connectivity**: Refactor the client side into a compiled, standalone background utility written in Rust, proving that entirely different programming languages can communicate seamlessly across the same local TCP port pathway.
