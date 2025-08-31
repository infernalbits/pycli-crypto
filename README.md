# **PyCLI-Crypto**

PyCLI-Crypto is a powerful and convenient Python command-line application for encrypting and decrypting text and files directly from your terminal. It's designed to be clean and self-contained, managing all its dependencies internally without leaving any leftover files.

## **Features**

* **Encrypt Text or Files**: Securely transform your sensitive data into an encrypted token.  
* **Decrypt Tokens**: Convert encrypted tokens back into their original content.  
* **Zero External Requirements**: The application handles all necessary Python packages within a temporary, self-cleaning virtual environment.  
* **Clean Operation**: Leaves no temporary files or installations on your system.

## **How It Works**

When you run the script, PyCLI-Crypto intelligently sets up a temporary, isolated Python virtual environment. It then installs any required libraries, such as cryptography, into this temporary space. Once your task is complete, this environment and all its contents are automatically removed. This ensures your system remains clean and you don't need to manually install any dependencies.

## **Installation**

No external installation steps are required\! The script is designed to be self-sufficient and will manage its own dependencies upon execution. Clone the repo, move main.py to a dir in your $PATH, make it executable, encrypt all the things...

```
# Clone this repo and cd into it
git clone https://github.com/infernalbits/pycli-crypto.git && cd pycli-crypto

# Move the file to a dir on $PATH
sudo mv main.py /usr/bin/clicrypt

# Make Executable 
sudo chmod +x /usr/bin/clicrypt

# Encrypt all the things (see [Usage](#usage))
clicrypt
```


## **Usage**

PyCLI-Crypto uses command-line flags to determine the action and the data to process.

### **Encryption**

To encrypt data (text or a file), use the \-e or \--encrypt flag. 

You must also specify the data source and supply a password:

\-d (direct data string) or
\-f (path to file)
and
\-p or \--password (strong password will be necessary to decrypt)

```
# Encrypting Text
python main.py -e -d "Your secret message here" -p "YourStrongPassword"

# Encrypting a File
python main.py -e -f /path/to/your/secret_document.txt -p "YourStrongPassword"
```

When encrypting a file, the application will suggest saving the output to a new file with a .enc extension (e.g., secret\_document.txt.enc).

### **Decryption**

To decrypt an encrypted token, use the \-d or \--decrypt flag. 

Just like with encryption, you must specify the data source and supply the password used to encrypt the file:
\-d (a token string) or
\-f (a file containing the token) 
and
\-p or \--password (original password)

```
# Decrypting a Token 
clicrypt -d -d "a1b2c3d4e5f6..." -p "YourStrongPassword"

# (Replace a1b2c3d4e5f6... with your actual token string)

# Decrypting a Token (from a file)
clicrypt -d -f /path/to/your/encrypted_token.enc -p "YourStrongPassword"
```

## **Support the Project**

If PyCLI-Crypto has been useful to you, consider supporting its development\! Your support helps in maintaining and improving this project. Plus, you know...food.

*-Bitcoin-*
bc1q8md5z75qfnt8hs408fh8lx9un3gf5kpjs6mz4a

*-USDT/Tron-* TKRjSD2yWqZeUMtejCj9rYMVdHxyGHdDdt

*-Monero-* 49Lc1XP91UXMnN6DrqfYkPPJ6ZM6JZeu5HfEJuHZZNZcDykdJ1vPDp64PGfbnR1p9ZGG9pPiLTcxL3wwMh8EcBTx5mRdc7g

*-Zcash-* t1g3rW82pScaUN8ZX6qyGjti8s7hZdV7PuF

### **Contributions**

If you have any changes to the projects' source code that you feel are, not only beneficial, but absolutely necessary to the projects future then create a pull request and your changes will be given serious consideration. 

Given the nature and simplicity of the project, minor or superfluous changes will not be accepted without setious security implications/justification. 

However, close mouths don't get fed. Submit your pull request, you never know. Worse case its rejected and you continue to use it in your fork with smug superiority every time you encrypt/decrypt the things.
