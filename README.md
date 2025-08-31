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

No external installation steps are required\! The script is designed to be self-sufficient and will manage its own dependencies upon execution.


bash```

git clone https://github.com/infernalbits/pycli-crypto && cd pycli-crypto

mv main.py ~/bin/clicrypt
chmod +x ~/bin/clicrypt


```


## **Usage**

PyCLI-Crypto uses command-line flags to determine the action and the data to process.

### **Encryption**

To encrypt data (text or a file), use the \-e or \--encrypt flag. You must also specify the data source with \-d (for direct data) or \-f (for a file path), and provide a password with \-p or \--password.  
**Encrypting Text**  
`python main.py -e -d "Your secret message here" -p "YourStrongPassword"`

**Encrypting a File**  
`python main.py -e -f /path/to/your/secret_document.txt -p "YourStrongPassword"`

When encrypting a file, the application will suggest saving the output to a new file with a .enc extension (e.g., secret\_document.txt.enc).

### **Decryption**

To decrypt an encrypted token, use the \-d or \--decrypt flag. Just like with encryption, you must specify the data source with \-d (for a token string) or \-f (for a file containing the token) and the original password with \-p or \--password.  
**Decrypting a Token (from the command line)**  
`python main.py -d -d "a1b2c3d4e5f6..." -p "YourStrongPassword"`

*(Replace a1b2c3d4e5f6... with your actual token string)*  
**Decrypting a Token (from a file)**  
`python main.py -d -f /path/to/your/encrypted_token.enc -p "YourStrongPassword"`

## **Support the Project**

If PyCLI-Crypto has been useful to you, consider supporting its development\! Your support helps in maintaining and improving this project.
