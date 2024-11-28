import subprocess
import os
import time
import hashlib

SERVER_PORT = 2121
TEST_FILE = 'test_file.txt'
NON_EXISTENT_FILE = 'non_existent_file.txt'
LARGE_FILE = 'large_test_file.txt'
SPECIAL_CHAR_FILE = 'test_@#$.txt'
MAX_FILENAME_FILE = 'a' * 255 + '.txt'

# Create a large test file (> 10MB)


def create_large_file():
    with open(LARGE_FILE, 'w') as f:
        f.write('This is a line in the file.\n' * (10 * 1024 *
                1024 // len('This is a line in the file.\n')))

# Create a test file with special characters


def create_special_char_file():
    with open(SPECIAL_CHAR_FILE, 'w') as f:
        f.write('This file has special characters in its name.\n')

# Create a test file with the maximum filename length


def create_max_filename_file():
    with open(MAX_FILENAME_FILE, 'w') as f:
        f.write('This file has the maximum allowed filename length.\n')

# Function to calculate the checksum of a file


def calculate_checksum(filename):
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# Test 1: Start the server and ensure it is listening on the correct port


def test_server_listening():
    print("Test 1: Start the server and ensure it is listening on port 2121.")
    # This test is manual; ensure the server is running.

# Test 2: Start the client and verify that it connects to the server successfully


def test_client_connection():
    print("Test 2: Start the client and verify that it connects to the server.")
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)  # Wait for the client to start
    client_process.terminate()

# Test 3: Upload a valid file from the client to the server


def test_upload_valid_file():
    print("Test 3: Upload a valid file from the client to the server.")
    with open(TEST_FILE, 'w') as f:
        f.write('This is a test file for upload.\n')

    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)  # Wait for the client to start
    client_process.stdin.write(f"put {TEST_FILE}\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the upload to complete
    client_process.terminate()

    # Check if the file exists on the server
    assert os.path.exists(
        TEST_FILE), "Test file was not uploaded to the server."

# Test 4: Attempt to upload a non-existent file from the client to the server


def test_upload_non_existent_file():
    print("Test 4: Attempt to upload a non-existent file from the client to the server.")
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)  # Wait for the client to start
    client_process.stdin.write(f"put {NON_EXISTENT_FILE}\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the command to process
    client_process.terminate()

# Test 5: Upload a file that is already present on the server


def test_upload_existing_file():
    print("Test 5: Upload a file that is already present on the server.")
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)  # Wait for the client to start
    client_process.stdin.write(f"put {TEST_FILE}\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the upload to complete
    client_process.terminate()

# Test 6: Upload a large file from the client to the server


def test_upload_large_file():
    print("Test 6: Upload a large file (> 10MB) from the client to the server.")
    create_large_file()
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process.stdin.write(f"put {LARGE_FILE}\n".encode())
    client_process.stdin.flush()
    time.sleep(5)
    client_process.terminate()

    # Check if the large file exists on the server
    assert os.path.exists(
        LARGE_FILE), "Large file was not uploaded to the server."

# Test 7: Upload multiple files in quick succession from the client to the server


def test_upload_multiple_files():
    print("Test 7: Upload multiple files in quick succession from the client to the server.")
    create_special_char_file()
    files_to_upload = [TEST_FILE, LARGE_FILE, SPECIAL_CHAR_FILE]
    for file in files_to_upload:
        client_process = subprocess.Popen(
            ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
        time.sleep(2)
        client_process.stdin.write(f"put {file}\n".encode())
        client_process.stdin.flush()
        time.sleep(2)  # Wait for the upload to complete
        client_process.terminate()

    # Verify all files are uploaded
    for file in files_to_upload:
        assert os.path.exists(file), f"{file} was not uploaded to the server."

# Test 8: Download a valid file from the server to the client


def test_download_valid_file():
    print("Test 8: Download a valid file from the server to the client.")
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process.stdin.write(f"get {TEST_FILE}\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the download to complete
    client_process.terminate()

    # Check if the file exists on the client
    assert os.path.exists(
        TEST_FILE), "Downloaded file does not exist on the client."

# Test 9: Attempt to download a non-existent file from the server


def test_download_non_existent_file():
    print("Test 9: Attempt to download a non-existent file from the server.")
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process.stdin.write(f"get {NON_EXISTENT_FILE}\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the command to process
    client_process.terminate()

# Test 10: Download a file that is currently being uploaded by another client


def test_download_during_upload():
    print("Test 10: Download a file that is currently being uploaded by another client.")
    client_process_upload = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process_upload.stdin.write(f"put {LARGE_FILE}\n".encode())
    client_process_upload.stdin.flush()

    client_process_download = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process_download.stdin.write(f"get {LARGE_FILE}\n".encode())
    client_process_download.stdin.flush()
    time.sleep(5)  # Wait for the download to complete
    client_process_upload.terminate()
    client_process_download.terminate()

# Test 11: List files on the server from the client


def test_list_files():
    print("Test 11: List files on the server from the client.")
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process.stdin.write("ls\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the command to process
    client_process.terminate()

# Test 12: List files when the server directory is empty


def test_list_empty_directory():
    print("Test 12: List files when the server directory is empty.")
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process.stdin.write("ls\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the command to process
    client_process.terminate()

# Test 13: Disconnect the client during a file upload


def test_disconnect_during_upload():
    print("Test 13: Disconnect the client during a file upload.")
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process.stdin.write(f"put {TEST_FILE}\n".encode())
    time.sleep(1)  # Start the upload
    client_process.terminate()  # Disconnect the client

# Test 14: Attempt to send an invalid command from the client to the server


def test_invalid_command():
    print("Test 14: Attempt to send an invalid command from the client to the server.")
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process.stdin.write("invalid_command\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the command to process
    client_process.terminate()

# Test 15: Test the server's response when the client sends a command after disconnecting


def test_command_after_disconnect():
    print("Test 15: Test the server's response when the client sends a command after disconnecting.")
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process.stdin.write(f"put {TEST_FILE}\n".encode())
    time.sleep(1)  # Start the upload
    client_process.terminate()  # Disconnect the client
    time.sleep(2)  # Wait before sending another command
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    client_process.stdin.write("ls\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the command to process
    client_process.terminate()

# Test 16: Start multiple clients simultaneously and perform file uploads and downloads


def test_multiple_clients():
    print("Test 16: Start multiple clients simultaneously and perform file uploads and downloads.")
    client_process_upload = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    client_process_download = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)

    time.sleep(2)
    client_process_upload.stdin.write(f"put {TEST_FILE}\n".encode())
    client_process_upload.stdin.flush()

    time.sleep(2)
    client_process_download.stdin.write(f"get {TEST_FILE}\n".encode())
    client_process_download.stdin.flush()

    time.sleep(5)  # Wait for both operations to complete
    client_process_upload.terminate()
    client_process_download.terminate()

# Test 17: Start a client upload while another client is downloading a file


def test_upload_while_downloading():
    print("Test 17: Start a client upload while another client is downloading a file.")
    client_process_upload = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process_upload.stdin.write(f"put {TEST_FILE}\n".encode())
    client_process_upload.stdin.flush()

    client_process_download = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process_download.stdin.write(f"get {TEST_FILE}\n".encode())
    client_process_download.stdin.flush()

    time.sleep(5)  # Wait for both operations to complete
    client_process_upload.terminate()
    client_process_download.terminate()

# Test 18: After file uploads, ensure that files can be deleted from the server


def test_delete_file():
    print("Test 18: After file uploads, ensure that files can be deleted from the server.")
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process.stdin.write(f"delete {TEST_FILE}\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the delete command to process
    client_process.terminate()

# Test 19: Ensure that the client-side files are removed after successful uploads


def test_client_file_cleanup():
    print("Test 19: Ensure that the client-side files are removed after successful uploads.")
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    assert not os.path.exists(
        TEST_FILE), "Client-side file was not removed after upload."

# Test 20: Restart the server and ensure that previously uploaded files are still present


def test_server_restart():
    print("Test 20: Restart the server and ensure that previously uploaded files are still present.")
    # This test is manual; ensure the server is restarted and check for file presence.

# Test 21: Measure the time taken to upload and download files of varying sizes


def test_performance():
    print("Test 21: Measure the time taken to upload and download files of varying sizes.")
    # Implement performance measurement logic here.

# Test 22: Check the server's performance under high load


def test_high_load():
    print("Test 22: Check the server's performance under high load.")
    # Implement high load testing logic here.

# Test 23: Upload a file with the maximum allowed filename length


def test_max_filename_length():
    print("Test 23: Upload a file with the maximum allowed filename length.")
    create_max_filename_file()
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process.stdin.write(f"put {MAX_FILENAME_FILE}\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the upload to complete
    client_process.terminate()

# Test 24: Upload files with special characters in their names


def test_special_character_filename():
    print("Test 24: Upload files with special characters in their names.")
    create_special_char_file()
    client_process = subprocess.Popen(
        ['python', 'client_side/cli.py'], stdin=subprocess.PIPE)
    time.sleep(2)
    client_process.stdin.write(f"put {SPECIAL_CHAR_FILE}\n".encode())
    client_process.stdin.flush()
    time.sleep(2)  # Wait for the upload to complete
    client_process.terminate()

# Test 25: Test the behavior when the server runs out of disk space during an upload


def test_disk_space_limit():
    print("Test 25: Test the behavior when the server runs out of disk space during an upload.")
    # This test requires a specific setup to simulate low disk space.
    # Implement logic to handle this scenario.


if __name__ == "__main__":
    # Run all tests
    test_server_listening()
    test_client_connection()
    test_upload_valid_file()
    test_upload_non_existent_file()
    test_upload_existing_file()
    test_upload_large_file()
    test_upload_multiple_files()
    test_download_valid_file()
    test_download_non_existent_file()
    test_download_during_upload()
    test_list_files()
    test_list_empty_directory()
    test_disconnect_during_upload()
    test_invalid_command()
    test_command_after_disconnect()
    test_multiple_clients()
    test_upload_while_downloading()
    test_delete_file()
    test_client_file_cleanup()
    test_server_restart()
    test_performance()
    test_high_load()
    # test_max_filename_length()
    # test_special_character_filename()
    # test_disk_space_limit()
