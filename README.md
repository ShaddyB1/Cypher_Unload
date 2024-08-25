Cryptography Tool

Description
This Cryptography Tool is a Python-based application that implements various classical ciphers. It provides both a command-line interface for direct interaction and a Flask API for web integration. The tool supports multiple cipher methods including Caesar, Vigenère, Playfair, Rail Fence, and Atbash ciphers.

Features
- Caesar Cipher (encode, decode, brute force)
- Vigenère Cipher (encode, decode)
- Playfair Cipher (encode, decode)
- Rail Fence Cipher (encode, decode)
- Atbash Cipher (encode/decode)
- File handling (read from file, write to file)
- Key generation for Vigenère and Playfair ciphers
- Command-line interface for easy interaction
- Flask API for web integration

Usage

Command-line Interface
To use the command-line interface, run:
```
python cryptography_tool.py
```
Follow the on-screen prompts to select and use different cipher methods.


## Testing
To run the unit tests, choose option 15 from the main menu in the command-line interface, or run:
```
python -m unittest cryptography_tool.py
```

