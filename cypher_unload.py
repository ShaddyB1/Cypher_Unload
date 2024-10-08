import string
import re
import random
import unittest

class CipherTools:
    def __init__(self):
        self.alphabet = string.ascii_lowercase

   
    def caesar_encode(self, message, offset):
        return self._caesar_cipher(message, offset)

    def caesar_decode(self, message, offset):
        return self._caesar_cipher(message, -offset)

    def _caesar_cipher(self, message, offset):
        result = ""
        for char in message.lower():
            if char in self.alphabet:
                index = (self.alphabet.index(char) + offset) % 26
                result += self.alphabet[index]
            else:
                result += char
        return result

    
    def vigenere_encode(self, message, keyword):
        return self._vigenere_cipher(message, keyword, encode=True)

    def vigenere_decode(self, message, keyword):
        return self._vigenere_cipher(message, keyword, encode=False)

    def _vigenere_cipher(self, message, keyword, encode=True):
        result = ""
        keyword = keyword.lower()
        keyword_index = 0
        
        for char in message.lower():
            if char in self.alphabet:
                char_index = self.alphabet.index(char)
                key_char = keyword[keyword_index % len(keyword)]
                key_index = self.alphabet.index(key_char)
                
                if encode:
                    new_index = (char_index + key_index) % 26
                else:
                    new_index = (char_index - key_index) % 26
                
                result += self.alphabet[new_index]
                keyword_index += 1
            else:
                result += char
        
        return result

   
    def playfair_encode(self, message, keyword):
        return self._playfair_cipher(message, keyword, encode=True)

    def playfair_decode(self, message, keyword):
        return self._playfair_cipher(message, keyword, encode=False)

    def _playfair_cipher(self, message, keyword, encode=True):
        
        key = ''.join(dict.fromkeys(keyword.lower() + self.alphabet.replace('j', '')))
        matrix = [list(key[i:i+5]) for i in range(0, 25, 5)]
        
        # Prepare message
        message = message.lower().replace('j', 'i')
        message = re.sub(r'[^a-z]', '', message)
        if len(message) % 2 != 0:
            message += 'x'
        
        result = ""
        for i in range(0, len(message), 2):
            a, b = message[i], message[i+1]
            row1, col1 = self._find_position(matrix, a)
            row2, col2 = self._find_position(matrix, b)
            
            if row1 == row2:
                col1 = (col1 + (1 if encode else -1)) % 5
                col2 = (col2 + (1 if encode else -1)) % 5
            elif col1 == col2:
                row1 = (row1 + (1 if encode else -1)) % 5
                row2 = (row2 + (1 if encode else -1)) % 5
            else:
                col1, col2 = col2, col1
            
            result += matrix[row1][col1] + matrix[row2][col2]
        
        return result

    def _find_position(self, matrix, letter):
        for i, row in enumerate(matrix):
            if letter in row:
                return i, row.index(letter)

   
    def rail_fence_encode(self, message, rails):
        return self._rail_fence_cipher(message, rails, encode=True)

    def rail_fence_decode(self, message, rails):
        return self._rail_fence_cipher(message, rails, encode=False)

    def _rail_fence_cipher(self, message, rails, encode=True):
        fence = [[None] * len(message) for _ in range(rails)]
        rail = 0
        direction = 1

        for i in range(len(message)):
            fence[rail][i] = message[i] if encode else None
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1

        if not encode:
            index = 0
            for i in range(rails):
                for j in range(len(message)):
                    if fence[i][j] is not None:
                        fence[i][j] = message[index]
                        index += 1

        result = []
        rail = 0
        direction = 1
        for i in range(len(message)):
            result.append(fence[rail][i])
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1

        return ''.join(result)

    
    def atbash_encode(self, message):
        return self.atbash_decode(message)  

    def atbash_decode(self, message):
        result = ""
        for char in message.lower():
            if char in self.alphabet:
                index = self.alphabet.index(char)
                result += self.alphabet[25 - index]
            else:
                result += char
        return result

    # Caesar Cipher Brute Force
    def caesar_brute_force(self, message):
        results = []
        for offset in range(26):
            decrypted = self.caesar_decode(message, offset)
            score = self._english_score(decrypted)
            results.append((offset, decrypted, score))
        return sorted(results, key=lambda x: x[2], reverse=True)

    def _english_score(self, text):
        
        common_words = set(['the', 'be', 'to', 'of', 'and', 'in', 'that', 'have'])
        words = text.lower().split()
        return sum(word in common_words for word in words)

   
    def read_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except IOError:
            print(f"Error: Unable to read file '{filename}'.")
        return None

    def write_to_file(self, filename, content):
        try:
            with open(filename, 'w') as file:
                file.write(content)
            print(f"Content successfully written to '{filename}'.")
        except IOError:
            print(f"Error: Unable to write to file '{filename}'.")

   
    def generate_vigenere_key(self, length):
        return ''.join(random.choice(self.alphabet) for _ in range(length))

    def generate_playfair_key(self, length):
        key = ''.join(random.sample(self.alphabet.replace('j', ''), length))
        return key + ''.join(char for char in self.alphabet if char not in key and char != 'j')

class TestCipherTools(unittest.TestCase):
    def setUp(self):
        self.tools = CipherTools()

    def test_caesar_cipher(self):
        message = "hello world"
        offset = 3
        encoded = self.tools.caesar_encode(message, offset)
        self.assertEqual(encoded, "khoor zruog")
        decoded = self.tools.caesar_decode(encoded, offset)
        self.assertEqual(decoded, message)

    def test_vigenere_cipher(self):
        message = "attackatdawn"
        keyword = "lemon"
        encoded = self.tools.vigenere_encode(message, keyword)
        self.assertEqual(encoded, "lxfopvefrnhr")
        decoded = self.tools.vigenere_decode(encoded, keyword)
        self.assertEqual(decoded, message)

    def test_playfair_cipher(self):
        message = "hello world"
        keyword = "keyword"
        encoded = self.tools.playfair_encode(message, keyword)
        decoded = self.tools.playfair_decode(encoded, keyword)
        self.assertEqual(decoded, "helxloworldx")

    def test_rail_fence_cipher(self):
        message = "defendtheeastwallofthecastle"
        rails = 3
        encoded = self.tools.rail_fence_encode(message, rails)
        self.assertEqual(encoded, "dnetldhsatwloteatlfheeeacehos")
        decoded = self.tools.rail_fence_decode(encoded, rails)
        self.assertEqual(decoded, message)

    def test_atbash_cipher(self):
        message = "abcdefghijklmnopqrstuvwxyz"
        encoded = self.tools.atbash_encode(message)
        self.assertEqual(encoded, "zyxwvutsrqponmlkjihgfedcba")
        decoded = self.tools.atbash_decode(encoded)
        self.assertEqual(decoded, message)

    def test_caesar_brute_force(self):
        message = "khoor zruog"
        results = self.tools.caesar_brute_force(message)
        self.assertIn((23, "hello world", 2), results)

    def test_key_generation(self):
        vigenere_key = self.tools.generate_vigenere_key(10)
        self.assertEqual(len(vigenere_key), 10)
        self.assertTrue(all(char in self.tools.alphabet for char in vigenere_key))

        playfair_key = self.tools.generate_playfair_key(10)
        self.assertEqual(len(playfair_key), 25)
        self.assertNotIn('j', playfair_key)

def main():
    tools = CipherTools()
    
    while True:
        print("\nCryptography Tool")
        print("1. Caesar Cipher Encode")
        print("2. Caesar Cipher Decode")
        print("3. Vigenère Cipher Encode")
        print("4. Vigenère Cipher Decode")
        print("5. Playfair Cipher Encode")
        print("6. Playfair Cipher Decode")
        print("7. Rail Fence Cipher Encode")
        print("8. Rail Fence Cipher Decode")
        print("9. Atbash Cipher Encode/Decode")
        print("10. Caesar Cipher Brute Force")
        print("11. Read Message from File")
        print("12. Write Message to File")
        print("13. Generate Vigenère Key")
        print("14. Generate Playfair Key")
        print("15. Run Unit Tests")
        print("16. Exit")
        
        choice = input("Enter your choice (1-16): ")
        
        if choice == '1':
            message = input("Enter the message to encode: ")
            offset = int(input("Enter the offset: "))
            result = tools.caesar_encode(message, offset)
            print("Encoded message:", result)
        elif choice == '2':
            message = input("Enter the message to decode: ")
            offset = int(input("Enter the offset: "))
            result = tools.caesar_decode(message, offset)
            print("Decoded message:", result)
        elif choice == '3':
            message = input("Enter the message to encode: ")
            keyword = input("Enter the keyword: ")
            result = tools.vigenere_encode(message, keyword)
            print("Encoded message:", result)
        elif choice == '4':
            message = input("Enter the message to decode: ")
            keyword = input("Enter the keyword: ")
            result = tools.vigenere_decode(message, keyword)
            print("Decoded message:", result)
        elif choice == '5':
            message = input("Enter the message to encode: ")
            keyword = input("Enter the keyword: ")
            result = tools.playfair_encode(message, keyword)
            print("Encoded message:", result)
        elif choice == '6':
            message = input("Enter the message to decode: ")
            keyword = input("Enter the keyword: ")
            result = tools.playfair_decode(message, keyword)
            print("Decoded message:", result)
        elif choice == '7':
            message = input("Enter the message to encode: ")
            rails = int(input("Enter the number of rails: "))
            result = tools.rail_fence_encode(message, rails)
            print("Encoded message:", result)
        elif choice == '8':
            message = input("Enter the message to decode: ")
            rails = int(input("Enter the number of rails: "))
            result = tools.rail_fence_decode(message, rails)
            print("Decoded message:", result)
        elif choice == '9':
            message = input("Enter the message to encode/decode: ")
            result = tools.atbash_encode(message)
            print("Encoded/Decoded message:", result)
        elif choice == '10':
            message = input("Enter the message to brute force: ")
            results = tools.caesar_brute_force(message)
            print("Top 5 possible decryptions:")
            for offset, decrypted, score in results[:5]:
                print(f"Offset {offset}: {decrypted} (Score: {score})")
        elif choice == '11':
            filename = input("Enter the filename to read from: ")
            content = tools.read_from_file(filename)
            if content:
                print("File content:", content)
        elif choice == '12':
            filename = input("Enter the filename to write to: ")
            content = input("Enter the content to write: ")
            tools.write_to_file(filename, content)
        elif choice == '13':
            length = int(input("Enter the desired key length: "))
            key = tools.generate_vigenere_key(length)
            print(f"Generated Vigenère key: {key}")
        elif choice == '14':
            length = int(input("Enter the desired unique key length (max 25): "))
            if length > 25:
                print("Error: Maximum key length is 25.")
            else:
                key = tools.generate_playfair_key(length)
                print(f"Generated Playfair key: {key}")
        elif choice == '15':
            unittest.main(argv=[''], exit=False)
        elif choice == '16':
            print("Thank you for using the Cryptography Tool. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()