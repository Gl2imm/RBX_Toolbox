from base64 import urlsafe_b64decode, urlsafe_b64encode


def urlsafe_b64_to_unsigned_int(s: str) -> int:
    """
    Decode urlsafe base64 to unsigned integers.
    """
    while len(s) % 4 != 0:
        s += "="
    return int.from_bytes(urlsafe_b64decode(s), byteorder="big", signed=False)


def unsigned_int_to_urlsafe_b64(i: int) -> str:
    """
    Encode unsigned integers as urlsafe base64 strings.
    """

    def byte_len(n):
        length = 0
        while n > 0:
            length += 1
            n = n >> 8
        return length

    byte_str = int.to_bytes(i, length=byte_len(i), byteorder="big", signed=False)
    return urlsafe_b64encode(byte_str).decode().rstrip("=")
