import textwrap

# Input binary string (only the binary part, without "a lot of 1" markers)
binary = "11101010111000101110001010100011101110111000111011101011100010001110101011100010111000101010001110"

def decode_bits(bits, width):
    """Attempt to decode bits in chunks of given width."""
    chunks = textwrap.wrap(bits, width)
    try:
        decoded = ''.join(chr(int(chunk, 2)) for chunk in chunks if len(chunk) == width)
    except Exception as e:
        decoded = f"Error: {e}"
    return decoded

def invert_bits(bits):
    return ''.join('1' if b=='0' else '0' for b in bits)

def reverse_bits(bits):
    return bits[::-1]

# Define modifications to try
modifications = {
    "normal": lambda b: b,
    "inverted": invert_bits,
    "reversed": reverse_bits
}

# Define group widths to try
group_widths = [8, 7]

# We'll try adding padding of 0 to 8 bytes (0 to 64 bits of '0's)
padding_options = [i * 8 for i in range(9)]

for mod_name, mod_func in modifications.items():
    mod_bits = mod_func(binary)
    for width in group_widths:
        for pad in padding_options:
            padded_bits = mod_bits + ("0" * pad)
            result = decode_bits(padded_bits, width)
            print(f"Mod: {mod_name}, Width: {width}-bit, Pad: {pad} bits -> {result}")
