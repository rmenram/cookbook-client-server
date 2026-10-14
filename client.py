# ==============================================================================
# Description: An interactive TCP Client. It connects to the server on Port 9000,
#              sends a text command, and displays the text file returned.
# ==============================================================================

import socket
import sys
import time

# Network Configuration Settings
HOST = '127.0.0.1'       # Target IP address (Loopback interface)
PORT = 9000             # Target port path for communication
BUFFER_SIZE = 4096      # 4KB client cache buffer to prevent stream truncation

def request_database_info(command_token):
    """
    Handles the network connection lifecycle for a single request.
    Connects, sends the command, reads the response, and prints it.
    """
    print("\n" + "-"*50)
    print(f"[Client] Initiating request sequence...")
    print(f"[Client] Target command token: '{command_token}'")
    
    # 1. Initialize the raw TCP socket instance
    print("[Socket] Initializing socket architecture...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 2. Connect to the server port listener
        print(f"[Connection] Connecting to host: {HOST} on port: {PORT}...")
        client_socket.connect((HOST, PORT))
        print("[Connection] TCP handshake established with remote host.")
        
        # Capture the active local port coordinates assigned by the OS
        local_ip, local_port = client_socket.getsockname()
        print(f"[Connection] Communication channel active on local port: {local_port}")
        
        # 3. Convert request string into standard UTF-8 network bytes
        print(f"[Data] Encoding string command payload to bytes...")
        encoded_payload = command_token.encode('utf-8')
        
        print(f"[Data] Transmitting packet data down the wire...")
        client_socket.sendall(encoded_payload)
        print("[Data] Message completely transmitted to server.")
        
        # 4. Block and listen for incoming response bytes from the server
        print("[Data] Awaiting response bytes from network buffer...")
        raw_response = client_socket.recv(BUFFER_SIZE)
        print(f"[Data] Received {len(raw_response)} raw packet bytes back.")
        
        # 5. Decode the incoming server bytes back into plaintext string format
        print("[Data] Decoding response bytes to text...")
        decoded_response = raw_response.decode('utf-8')
        
        # 6. Render the data payload onto the terminal screen
        print("\n" + "="*60)
        print("                  SERVER DATABASE INVENTORY                     ")
        print("="*60)
        print(decoded_response)
        print("="*60 + "\n")
        
    except ConnectionRefusedError:
        print("[Error] Connection rejected. Target server is offline.")
        print("[Error] Verify that server.py is running in a separate window.")
    except Exception as network_error:
        print(f"[Error] A runtime network exception occurred: {str(network_error)}")
    finally:
        # 7. Close the socket connection to free up system memory resources
        client_socket.close()
        print("[Client] Socket pipeline closed cleanly.")
        print("-"*50)

def display_user_control_menu():
    """
    Displays a terminal menu allowing users to select an operation code,
    send an invalid test payload, or exit the script.
    """
    while True:
        print("\n" + "="*40)
        print("      NETWORKING CONTROL MENU   ")
        print("="*40)
        print("1. Request Database Inventory Records")
        print("2. Send Invalid Test Command")
        print("3. Exit Client Program")
        print("="*40)
        
        user_choice = input("Select an option (1-3): ").strip()
        
        if user_choice == "1":
            # Fire valid message
            request_database_info("FETCH_DATABASE_INVENTORY")
            time.sleep(1) # Brief delay for terminal legibility
        elif user_choice == "2":
            # Fire invalid message to test server error-handling routines
            request_database_info("INVALID_TEST_SIGNAL_X")
            time.sleep(1)
        elif user_choice == "3":
            print("\n[Client] Closing terminal control shell. Exiting.")
            sys.exit(0)
        else:
            print("\n[Warning] Option not recognized. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    # Launch terminal menu loop
    display_user_control_menu()
