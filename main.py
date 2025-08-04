import sys
import os
import shutil
import tempfile
import virtualenv
import subprocess

import modules.argparse_module as args_parser
import modules.fernet_module as fernet

def main():
    """
    Main function to parse arguments and perform encryption or decryption.
    """
    # Parse command-line arguments
    args = args_parser.setup_args()

    # Determine the input data
    input_data = None
    if args.data:
        input_data = args.data.encode('utf-8') # Encode string message to bytes
    elif args.file:
        try:
            with open(args.file, 'rb') as f: # Read file in binary mode
                input_data = f.read()
        except IOError as e:
            print(f"Error: Could not read file '{args.file}'. {e}")
            sys.exit(1)

    if input_data is None:
        print("Error: No data or file content provided for encryption/decryption.")
        sys.exit(1)

    if args.encrypt:
        try:
            encrypted_token = fernet.encrypt_data(input_data, password=args.password)
            print(f"Encrypted token (hex): {encrypted_token.hex()}")

            # If a file was encrypted, suggest saving the output to a new file
            if args.file:
                output_filename = args.file + ".enc"
                try:
                    with open(output_filename, 'wb') as f:
                        f.write(encrypted_token)
                    print(f"Encrypted content saved to: {output_filename}")
                except IOError as e:
                    print(f"Warning: Could not save encrypted content to file. {e}")

        except ValueError as e:
            print(f"Error during encryption: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred during encryption: {e}")
            sys.exit(1)

    elif args.decrypt:
        try:
            # For decryption, the input_data is expected to be a hex string of the token
            token_to_decrypt = bytes.fromhex(input_data.decode('utf-8')) # Decode hex string to bytes
            decrypted_message = fernet.decrypt_data(token_to_decrypt, password=args.password)
            print(f"Decrypted message: {decrypted_message.decode('utf-8')}")

        except ValueError as e:
            print(f"Error: Invalid token format or incorrect password. {e}")
            print("Please ensure the token is a valid hexadecimal string and the correct password is provided.")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred during decryption: {e}")
            sys.exit(1)
            
            
 

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as TEMP:
                  venv_path = os.path.join(TEMP, 'my_venv')
                  
                  try:
                      # Create a virtual environment
                      subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True, capture_output=True)
                      
                      # Get the correct pip executable path inside the new venv
                      pip_executable = os.path.join(venv_path, 'bin', 'pip')
                      if sys.platform == 'win32':
                          pip_executable = os.path.join(venv_path, 'Scripts', 'pip.exe')
                      
                      # Install required packages using the venv's pip
                      subprocess.run([pip_executable, 'install', 'cryptography'], check=True, capture_output=True)
                      
                      # Manually construct the path to the virtual environment's site-packages
                      # This is a more robust way to find the path and avoids the StopIteration error.
                      if sys.platform == 'win32':
                          site_packages_path = os.path.join(venv_path, 'Lib', 'site-packages')
                      else: # Unix-like systems
                          # Find the correct python version subdirectory
                          python_lib_path = os.path.join(venv_path, 'lib')
                          python_version_dir = next(d for d in os.listdir(python_lib_path) if d.startswith('python'))
                          site_packages_path = os.path.join(python_lib_path, python_version_dir, 'site-packages')

                      # Add the virtual environment's site-packages to the Python path
                      # This allows the host script to find the installed packages.
                      sys.path.insert(0, site_packages_path)
                      
                      # Call the main function
                      main()
                      
                  except subprocess.CalledProcessError as e:
                      print(f"Error during virtual environment setup or package installation: {e.stderr.decode('utf-8')}")
                      sys.exit(1)
                  except StopIteration:
                      print("Error: Could not find the 'site-packages' directory inside the virtual environment.")
                      sys.exit(1)
                  except Exception as e:
                      print(f"An unexpected error occurred: {e}")
                      sys.exit(1)
