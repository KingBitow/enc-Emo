

import os

# Create project structure
project_root = "/mnt/kimi/output/emoji-encoder"
os.makedirs(project_root, exist_ok=True)
os.makedirs(f"{project_root}/static", exist_ok=True)
os.makedirs(f"{project_root}/templates", exist_ok=True)

# 1. Core encoder/decoder module (emoji_codec.py)
core_code = '''"""
Emoji Encoder/Decoder
Encode any text/data as emoji and decode it back.
"""

import base64
import json

# Emoji alphabet - 64 emojis for Base64-like encoding
EMOJI_ALPHABET = [
    '😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣',
    '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰',
    '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜',
    '🤪', '🤨', '🧐', '🤓', '😎', '🥸', '🤩', '🥳',
    '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️',
    '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😤',
    '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱',
    '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫'
]

# Create reverse mapping
EMOJI_TO_BYTE = {emoji: i for i, emoji in enumerate(EMOJI_ALPHABET)}

def encode_bytes(data: bytes) -> str:
    """Encode bytes to emoji string."""
    # First encode as base64 to get ASCII-safe string
    b64 = base64.b64encode(data).decode('ascii')
    # Convert base64 to emoji
    result = []
    for char in b64:
        # Get 6-bit value (0-63)
        val = ord(char)
        if 65 <= val <= 90:  # A-Z
            idx = val - 65
        elif 97 <= val <= 122:  # a-z
            idx = val - 97 + 26
        elif 48 <= val <= 57:  # 0-9
            idx = val - 48 + 52
        elif char == '+':
            idx = 62
        elif char == '/':
            idx = 63
        elif char == '=':
            idx = 0  # Padding
        else:
            continue
        result.append(EMOJI_ALPHABET[idx])
    return ''.join(result)

def decode_bytes(emoji_str: str) -> bytes:
    """Decode emoji string back to bytes."""
    b64_chars = []
    for emoji in emoji_str:
        if emoji not in EMOJI_TO_BYTE:
            continue
        idx = EMOJI_TO_BYTE[emoji]
        # Convert back to base64 char
        if idx < 26:
            char = chr(65 + idx)  # A-Z
        elif idx < 52:
            char = chr(97 + idx - 26)  # a-z
        elif idx < 62:
            char = chr(48 + idx - 52)  # 0-9
        elif idx == 62:
            char = '+'
        else:
            char = '/'
        b64_chars.append(char)
    
    b64_str = ''.join(b64_chars)
    # Add padding if needed
    padding = 4 - (len(b64_str) % 4)
    if padding != 4:
        b64_str += '=' * padding
    
    return base64.b64decode(b64_str)

def encode_text(text: str) -> str:
    """Encode text string to emoji."""
    return encode_bytes(text.encode('utf-8'))

def decode_text(emoji_str: str) -> str:
    """Decode emoji string back to text."""
    return decode_bytes(emoji_str).decode('utf-8')

def encode_file(filepath: str) -> str:
    """Encode file contents to emoji."""
    with open(filepath, 'rb') as f:
        return encode_bytes(f.read())

def decode_to_file(emoji_str: str, output_path: str):
    """Decode emoji string and save to file."""
    data = decode_bytes(emoji_str)
    with open(output_path, 'wb') as f:
        f.write(data)

if __name__ == "__main__":
    # Test
    test = "Hello, World! 🌍"
    encoded = encode_text(test)
    decoded = decode_text(encoded)
    print(f"Original: {test}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
    assert test == decoded
    print("✅ Test passed!")
'''

with open(f"{project_root}/emoji_codec.py", "w") as f:
    f.write(core_code)

print("✅ Created emoji_codec.py")
