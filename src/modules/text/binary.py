def encode(text):
    # Convert each character in the string to its corresponding binary representation
    binary_list = [format(ord(char), "08b") for char in text]
    # Join the binary representations together into a single string
    binary_string = "".join(binary_list)
    return binary_string


def decode(binary):
    # Split the binary string into 8-bit segments
    binary_list = [binary[i : i + 8] for i in range(0, len(binary), 8)]
    # Convert each 8-bit binary segment back to its corresponding character
    decoded_text = "".join(chr(int(binary, 2)) for binary in binary_list)
    return decoded_text
