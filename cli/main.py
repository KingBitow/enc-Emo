

# 2. CLI tool (cli.py)
cli_code = '''#!/usr/bin/env python3
"""
Emoji Encoder CLI Tool
Usage:
    python cli.py encode "Hello World"
    python cli.py decode "😀😃😄..."
    python cli.py encode -f input.txt
    python cli.py decode -f emoji.txt -o output.txt
"""

import argparse
import sys
from emoji_codec import encode_text, decode_text, encode_file, decode_to_file

def main():
    parser = argparse.ArgumentParser(
        description="Encode/decode text as emoji",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s encode "Hello World"
  %(prog)s decode "😀😃😄😁😆😅😂"
  %(prog)s encode -f secret.txt -o encoded.txt
  echo "Hello" | %(prog)s encode
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode text to emoji')
    encode_parser.add_argument('text', nargs='?', help='Text to encode')
    encode_parser.add_argument('-f', '--file', help='File to encode')
    encode_parser.add_argument('-o', '--output', help='Output file')
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode emoji to text')
    decode_parser.add_argument('emoji', nargs='?', help='Emoji string to decode')
    decode_parser.add_argument('-f', '--file', help='File containing emoji')
    decode_parser.add_argument('-o', '--output', help='Output file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'encode':
            if args.file:
                result = encode_file(args.file)
            elif args.text:
                result = encode_text(args.text)
            else:
                # Read from stdin
                result = encode_text(sys.stdin.read())
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"✅ Encoded to {args.output}")
            else:
                print(result)
                
        elif args.command == 'decode':
            if args.file:
                with open(args.file, 'r', encoding='utf-8') as f:
                    emoji_str = f.read()
                result = decode_text(emoji_str)
            elif args.emoji:
                result = decode_text(args.emoji)
            else:
                # Read from stdin
                result = decode_text(sys.stdin.read())
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"✅ Decoded to {args.output}")
            else:
                print(result)
                
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

with open(f"{project_root}/cli.py", "w") as f:
    f.write(cli_code)

print("✅ Created cli.py")
