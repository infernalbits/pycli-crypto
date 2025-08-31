import argparse
import os

def setup_args():
    """
    Sets up the argument parser for the encryption/decryption tool.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Encrypt/Decrypt tool using Fernet symmetric encryption.\n\n"
                    "For secure key management, you can:\n"
                    "1. Provide a password using --password/-p.\n"
                    "2. Set the FERNET_KEY environment variable (e.g., export FERNET_KEY=\"<your_base64_key>\").\n"
                    "   If a password is provided, it takes precedence over FERNET_KEY.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Mutually exclusive group for --encrypt and --decrypt flags
    operation_group = parser.add_mutually_exclusive_group(required=True)
    operation_group.add_argument(
        "-e", "--encrypt",
        action="store_true",
        help="Encrypt the provided message or file content."
    )
    operation_group.add_argument(
        "-d", "--decrypt",
        action="store_true",
        help="Decrypt the provided token."
    )

    # Mutually exclusive group for input data (direct string vs. file)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "data",
        nargs="?", # Makes the argument optional, but required by the group
        help="Message to encrypt or token (in hex format) to decrypt.\n"
             "Example for encrypt: python main.py --encrypt \"Hello World\"\n"
             "Example for decrypt: python main.py --decrypt \"<hex_token>\""
    )
    input_group.add_argument(
        "-f", "--file",
        type=str,
        help="Path to a file whose content should be encrypted. Cannot be used with decrypt (-d) or 'data' argument."
    )

    # Optional argument for password-based key derivation
    parser.add_argument(
        "-p", "--password",
        type=str,
        help="Password to derive the encryption/decryption key. If not provided,\n"
             "the script will look for a FERNET_KEY environment variable."
    )

    args = parser.parse_args()

    # Additional validation:
    # If encrypt is chosen and a file is provided, ensure the file exists
    if args.encrypt and args.file:
        if not os.path.exists(args.file):
            parser.error(f"Error: The specified file '{args.file}' does not exist.")
        if not os.path.isfile(args.file):
            parser.error(f"Error: The specified path '{args.file}' is not a file.")

    # If decrypt is chosen, ensure 'data' is provided (as file input is only for encryption)
    if args.decrypt and args.file:
        parser.error("Error: --file/-f option is only for encryption. For decryption, provide the token directly.")

    return args

