def bytes_to_binary_string(byte_data):
    """
    Converts a bytes object to a binary string representation.

    Args:
        byte_data: The bytes object to convert.

    Returns:
        A string representing the binary value of the bytes object.
    """
    binary_parts = []
    for byte in byte_data:
        # Convert each byte (integer) to its 8-bit binary representation
        # and remove the "0b" prefix.
        binary_parts.append(bin(byte)[2:].zfill(8))
    return "".join(binary_parts)