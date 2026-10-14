# ==============================================================================
# Description: A TCP Server that binds to a local port, listens for client
#              connections, reads a local text file, and sends the contents
#              back across the network channel.
# ==============================================================================

import socket
import os
import datetime

# Network Configuration Settings
HOST = '127.0.0.1'       # Localhost
PORT = 9000             # Dedicated Port
BUFFER_SIZE = 1024      # 1KB buffer size
FILE_NAME = "local_data_pantry.txt"

def verify_and_initialize_database():
    """
    Checks if the database text file exists. If missing, it creates 
    a fresh file with default data to prevent execution errors.
    """
    print("[System Check] Verifying local database file...")
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            f.write("=== SEMANTIC MEMORY MICROSERVICE DATABASE ===\n")
            f.write("1. Mexican_Cuisine_Manual.pdf - Ingested via Rust Watcher Module 1\n")
            f.write("2. Italian_Baking_Mastery.pdf - Processed via Python Pantry Module 2\n")
            f.write("3. Low_Level_Sockets_Guide.pdf - Active in Transport Network Module 3\n")
        print(f"[System Check] File was missing. Created fresh file at: {FILE_NAME}")
    else:
        print(f"[System Check] Database file online and ready: {FILE_NAME}")

def start_server():
    """
    Initializes the network socket, binds it to the local port, and runs 
    a loop to accept and process client requests.
    """
    # 1. Ensure the database file exists
    verify_and_initialize_database()

    # 2. Create the network socket (IPv4, TCP stream)
    print("[Server] Initializing network socket...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 3. Release the port immediately on exit to prevent port locking errors
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 4. Bind the socket and start listening
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[Server] Active and listening on {HOST}:{PORT}...")
    except Exception as bind_error:
        print(f"[Error] Server could not secure the port: {str(bind_error)}")
        return
    
    try:
        while True:
            print("\n" + "="*50)
            print("[Server] Waiting for a client to connect...")
            
            # 5. Wait for an incoming connection
            connection, client_address = server_socket.accept()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [Connection] Handshake accepted from: {client_address}")
            
            try:
                # 6. Read the raw request bytes from the network
                raw_bytes = connection.recv(BUFFER_SIZE)
                if not raw_bytes:
                    print("[Server] Received empty packet. Skipping loop.")
                    continue
                
                # 7. Decode bytes into a text string
                request_signal = raw_bytes.decode('utf-8')
                print(f"[Server] Received command: '{request_signal}'")
                
                # 8. Process the command and send the file content
                if request_signal == "FETCH_DATABASE_INVENTORY":
                    print(f"[File IO] Reading data from: {FILE_NAME}")
                    with open(FILE_NAME, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    
                    # Send the data back over the network
                    connection.sendall(file_content.encode('utf-8'))
                    print("[Server] Sent database content to client.")
                else:
                    error_msg = f"Error: Request code not recognized: '{request_signal}'"
                    connection.sendall(error_msg.encode('utf-8'))
                    print(f"[Warning] Rejected unrecognized command: {request_signal}")
                
                # 9. Send shutdown signal to flush buffers cleanly before closing
                print("[Network] Flushing stream pipelines.")
                connection.shutdown(socket.SHUT_WR) 
                    
            except Exception as transaction_error:
                print(f"[Error] Data transfer failed: {str(transaction_error)}")
            finally:
                # 10. Close the client connection
                connection.close()
                print(f"[Connection] Session closed for: {client_address}")
                
    except KeyboardInterrupt:
        print("\n[Server] Detected exit command from keyboard.")
    finally:
        # 11. Close the core socket listener pool
        server_socket.close()
        print("[Server] Main listener closed. Port 9000 released. Exiting.")

if __name__ == "__main__":
    start_server()
