# Create a large text file (more than 10MB)
filename = 'large_test_file.txt'

# Specify the size in bytes (10MB = 10 * 1024 * 1024 bytes)
size_in_bytes = 10 * 1024 * 1024 + 1  # 10MB + 1 byte

# Open the file in write mode
with open(filename, 'w') as f:
    # Write a repeated string to reach the desired size
    f.write('This is a line in the file.\n' *
            (size_in_bytes // len('This is a line in the file.\n')))

print(f'Created file: {filename} with size: {size_in_bytes} bytes')
