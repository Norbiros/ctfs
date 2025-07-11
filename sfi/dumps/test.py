with open("file1.bin", "rb") as f1, open("file2.bin", "rb") as f2, open("intersection", "wb") as intersection:
    # Read both files as binary
    file1_data = f1.read()
    file2_data = f2.read()

    # Find the intersection (common bytes)
    common_data = bytearray(min(len(file1_data), len(file2_data)))

    for i in range(len(common_data)):
        if file1_data[i] == file2_data[i]:
            common_data[i] = file1_data[i]

    # Write the intersection to the new file
    intersection.write(common_data)
