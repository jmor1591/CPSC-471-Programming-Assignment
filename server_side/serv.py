import socket  # Import the socket library for network communication
import os  # Import the os library for interacting with the operating system
import threading  # Import the threading library to handle multiple clients concurrently

BUFFER_SIZE = 4096  # Define a constant for the buffer size used in data transmission


def handle_client(client_socket):
    """
    Handle communication with a connected client.
    This function runs in a separate thread for each client.
    """
    while True:
        # Receive a command from the client
        command = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Received command: {command}")

        # If the client requests to list files
        if command.startswith("ls"):
            list_files(client_socket)  # Call the function to list files
            # Wait for confirmation from the client
            confirmation = client_socket.recv(BUFFER_SIZE).decode()
            if confirmation == "FILES LISTED":
                print("Client confirms listing of files.")

        # If the client requests to download a file
        elif command.startswith("get"):
            # Extract the filename from the command
            filename = command.split()[1]
            # Call the function to handle file download
            handle_get(client_socket, filename)
            confirmation = client_socket.recv(BUFFER_SIZE).decode()
            if confirmation == "FILE(S) RECEIVED":
                print("Client confirms receiving of files.")
            elif confirmation == "FILE(S) NOT RECEIVED":
                print("Client did not receive the file(s).")

        # If the client wants to upload a file
        elif command.startswith("put"):
            # Extract the filename from the command
            filename = command.split()[1]
            # Call the function to handle file upload
            handle_put(client_socket, filename)
            # Send confirmation back to the client after handling the put command
            client_socket.send("UPLOAD SUCCESS".encode())

        # If the client wants to disconnect
        elif command == "quit":
            print("Client disconnected.")
            client_socket.close()  # Close the connection to the client
            break  # Exit the loop

        # Implement logic for invalid commands (else statement) do not add code here


def list_files(client_socket):
    """
    List all files in the current directory and send the list to the client.
    """
    files = "\n".join(os.listdir(
        '.'))  # Get a list of files in the current directory
    client_socket.send(files.encode())  # Send the list of files to the client


def handle_get(client_socket, filename):
    """
    Handle a request to download a file from the server to the client.
    """
    # Check if the requested file exists
    if os.path.exists(filename):
        # Notify the client that the file exists
        client_socket.send("SUCCESS".encode())
        # Create a new socket for data connection
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind(('', 0))  # Bind to an ephemeral port
        # Get the port number assigned by the OS
        data_port = data_socket.getsockname()[1]
        # Send the data port number to the client
        client_socket.send(f"DATA_PORT {data_port}".encode())
        # Start listening for incoming connections on the data port
        data_socket.listen(1)

        # Wait for the client to connect to the data port
        data_conn, addr = data_socket.accept()
        # Log the address of the connected client
        print(f"Data connection established with {addr}")

        # Open the requested file in binary read mode
        with open(filename, 'rb') as f:
            data = f.read(BUFFER_SIZE)  # Read the first chunk of data
            while data:  # While there is data to send
                data_conn.send(data)  # Send the chunk of data to the client
                data = f.read(BUFFER_SIZE)  # Read the next chunk of data

        data_conn.close()  # Close the data connection after sending the file
        # Log successful file transfer
        print(f"File {filename} sent successfully.")
    else:
        # Notify the client that the file does not exist
        client_socket.send("FAILURE: File not found".encode())


def handle_put(client_socket, filename):
    """
    Handle file upload requests from the client.

    This function establishes a data connection and receives a file from the client, 
    saving it to the specified filename.
    """
    # Create a new socket for the data connection
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to an ephemeral port (0 means the OS will choose an available port)
    data_socket.bind(('', 0))
    # Get the port number assigned by the OS
    data_port = data_socket.getsockname()[1]

    # Send the assigned data port number back to the client
    client_socket.send(f"DATA_PORT {data_port}".encode())

    # Listen for incoming connections on the data port
    data_socket.listen(1)

    # Wait for the client to connect to the data port
    data_conn, addr = data_socket.accept()
    print(f"Data connection established with {addr}")

    # Open the specified file in binary write mode
    with open(filename, 'wb') as f:
        # Receive data from the client in chunks
        data = data_conn.recv(BUFFER_SIZE)
        while data:
            f.write(data)  # Write the received chunk to the file
            data = data_conn.recv(BUFFER_SIZE)  # Receive the next chunk

    # Close the data connection after the upload is complete
    data_conn.close()
    print(f"File {filename} uploaded successfully.")


def main():
    """
    Main function to set up the server.

    This function initializes the server socket, listens for incoming client connections,
    and starts a new thread to handle each client.
    """
    # Create a TCP socket for the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the server to all interfaces on port 2121
    server.bind(("0.0.0.0", 2121))

    # Start listening for incoming connections (with a backlog of 5)
    server.listen(5)
    print("Server listening on port 2121")

    while True:
        # Accept a new client connection
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        # Start a new thread to handle the client connection
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()  # Run the main function to start the server
