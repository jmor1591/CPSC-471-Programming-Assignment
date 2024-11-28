import socket  # Import the socket library for network communication
import os  # Import the os library for interacting with the operating system

# Define a constant for the buffer size used in data transmission
BUFFER_SIZE = 4096


def main():
    """
    Main function to set up the client.
    This function connects to the server and handles user commands for file transfer.
    """
    server_ip = "127.0.0.1"  # IP address of the server (localhost)
    server_port = 2121  # Port number on which the server is listening

    # Create a TCP socket for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the client socket to the server's IP and port
    client.connect((server_ip, server_port))

    while True:
        # Prompt the user for a command
        command = input("ftp> ")

        # Handle the 'get' command for downloading a file
        if command.startswith("get"):
            # Extract the filename from the command
            filename = command.split()[1]
            # Call the function to handle file download
            handle_get(client, filename)

        # Handle the 'put' command for uploading a file
        elif command.startswith("put"):
            # Extract the filename from the command
            filename = command.split()[1]
            # Call the function to handle file upload
            handle_put(client, filename)

        # Handle the 'ls' command to list files on the server
        elif command == "ls":
            # Send the ls command to the server
            client.send(command.encode())
            # Receive the list of files from the server and decode it
            file_list = client.recv(BUFFER_SIZE).decode()
            print("Files on server:")
            print(file_list)  # Display the list of files
            # Send confirmation back to the server that files have been listed
            client.send("FILES LISTED".encode())

        # Handle the 'quit' command to exit the client
        elif command == "quit":
            # Inform the server of the disconnection
            client.send(command.encode())
            client.close()  # Close the client socket
            break  # Exit the loop and end the client session

        # Implement logic for invalid commands (e.g., notify the user or send an error to the server)
        # TODO: Add code here for handling invalid commands


def handle_get(client_socket, filename):
    """
    Function to handle file download requests from the server.
    This function sends a request to download a file and receives the file over a data connection.
    """
    client_socket.send(f"get {filename}".encode()
                       )  # Send the get request to the server

    # Wait for a response from the server indicating success or failure
    response = client_socket.recv(BUFFER_SIZE).decode()
    if response == "SUCCESS":
        # Receive the data port number for the file transfer
        data_port_response = client_socket.recv(BUFFER_SIZE).decode()
        # Extract the port number from the response
        data_port = int(data_port_response.split()[1])

        # Create a new socket for the data connection to receive the file
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server's data port
        data_socket.connect((client_socket.getpeername()[0], data_port))

        # Open a file in binary write mode to save the downloaded data
        with open(filename, 'wb') as f:
            # Receive the first chunk of data
            data = data_socket.recv(BUFFER_SIZE)
            while data:  # While there is data to receive
                f.write(data)  # Write the received chunk to the file
                data = data_socket.recv(BUFFER_SIZE)  # Receive the next chunk

        data_socket.close()  # Close the data socket after the transfer is complete
        print(f"File {filename} downloaded successfully.")

        # Send confirmation back to the server that the file has been received
        client_socket.send("FILE(S) RECEIVED".encode())
    else:
        # If the download was unsuccessful, inform the server
        client_socket.send("FILE(S) NOT RECEIVED".encode())
        print(response)  # Print the error message received from the server


def handle_put(client_socket, filename):
    """
    Function to handle file upload requests to the server.
    This function sends the file data over a data connection established with the server.
    """
    # Check if the file exists on the client
    if os.path.exists(filename):
        # Send a command to the server indicating the file to upload
        client_socket.send(f"put {filename}".encode())

        # Wait for the server's response containing the data port number for the upload
        data_port_response = client_socket.recv(BUFFER_SIZE).decode()
        # Extract the port number from the response
        data_port = int(data_port_response.split()[1])

        # Create a new socket for the data connection
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server's data port using the IP address and port number
        data_socket.connect((client_socket.getpeername()[0], data_port))

        # Open the specified file in binary read mode to send its contents
        with open(filename, 'rb') as f:
            # Read the first chunk of data from the file
            data = f.read(BUFFER_SIZE)
            # Continue reading and sending chunks until the entire file is sent
            while data:
                # Send the current chunk of data to the server
                data_socket.send(data)
                # Read the next chunk of data from the file
                data = f.read(BUFFER_SIZE)

        # Close the data socket after the transfer is complete
        data_socket.close()
        print(f"File {filename} uploaded successfully.")

        # Wait for confirmation from the server that the file has been received
        confirmation = client_socket.recv(BUFFER_SIZE).decode()
        if confirmation == "UPLOAD SUCCESS":
            print("Server confirms the file has been received.")
    else:
        # Print an error message if the file does not exist on the client
        print(f"FAILURE: File '{
              filename}' not found. No command sent to the server.")


if __name__ == "__main__":
    main()  # Run the main function to start the client
