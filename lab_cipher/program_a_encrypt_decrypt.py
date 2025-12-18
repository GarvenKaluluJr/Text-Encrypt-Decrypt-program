# Program A: Encryption/Decryption
# Caesar method with a keyword (English alphabet)

# Used to access punctuation characters
import string  

# Constant containing the English lowercase alphabet
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def preprocess(text: str) -> str:
    """
    Preprocess input text before encryption:
    - remove punctuation symbols,
    - convert all letters to lowercase,
    - keep spaces and other whitespace characters unchanged.
    """
    # Create a translation table that removes all punctuation characters
    translator = str.maketrans("", "", string.punctuation)
    # Apply translation and convert text to lowercase
    return text.translate(translator).lower()


def build_keyed_alphabet(keyword: str) -> str:
    """
    Build a keyed substitution alphabet based on the given keyword.
    Duplicate letters are removed, and remaining alphabet letters
    are appended in normal order.
    """
    # Keep only alphabetic characters from the keyword
    kw = "".join(ch for ch in keyword.lower() if ch in ALPHABET)

    seen = set()      # Set to track already used characters
    unique = []       # List of unique characters in keyword order

    # Add unique characters from the keyword
    for ch in kw:
        if ch not in seen:
            seen.add(ch)
            unique.append(ch)

    # Add remaining alphabet letters not present in the keyword
    remaining = [ch for ch in ALPHABET if ch not in seen]

    # Construct the final keyed alphabet
    keyed = "".join(unique + remaining)

    # Sanity check: keyed alphabet must contain exactly 26 letters
    if len(keyed) != 26:
        raise ValueError("Invalid keyed alphabet construction.")

    return keyed


def encrypt(text: str, keyword: str) -> str:
    """
    Encrypt the given text using a Caesar cipher with a keyword-based alphabet.
    """
    # Build keyed alphabet
    keyed = build_keyed_alphabet(keyword)

    # Create mapping from normal alphabet to keyed alphabet
    enc_map = {ALPHABET[i]: keyed[i] for i in range(26)}

    # List to accumulate encrypted characters
    out = []  

    # Replace each character using the encryption map
    for ch in text:
        out.append(enc_map.get(ch, ch))  # Non-alphabet characters remain unchanged

    return "".join(out)


def decrypt(text: str, keyword: str) -> str:
    """
    Decrypt the given text using a Caesar cipher with a keyword-based alphabet.
    """
    # Build keyed alphabet
    keyed = build_keyed_alphabet(keyword)

    # Create reverse mapping from keyed alphabet to normal alphabet
    dec_map = {keyed[i]: ALPHABET[i] for i in range(26)}

    # List to accumulate decrypted characters
    out = []  

    # Replace each character using the decryption map
    for ch in text:
        out.append(dec_map.get(ch, ch))  # Non-alphabet characters remain unchanged

    return "".join(out)


def read_text_file(path: str) -> str:
    """
    Read and return the entire content of a text file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text_file(path: str, content: str) -> None:
    """
    Write the given content to a text file.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def get_key() -> str:
    """
    Obtain the encryption/decryption key either from the keyboard
    or from a file. Optionally save the key to a file.
    """
    print("Key input:")
    print("  1) Enter key from keyboard")
    print("  2) Read key from file")

    # Read user's choice
    choice = input("Choose (1/2): ").strip()

    if choice == "1":
        # Read key from keyboard
        key = input("Enter key (keyword): ").strip()
        if not key:
            raise ValueError("Key cannot be empty.")

        # Ask whether to save the key to a file
        save = input("Save key to file? (y/n): ").strip().lower()
        if save == "y":
            key_path = input("Key file path to write: ").strip()
            write_text_file(key_path, key)

        return key

    if choice == "2":
        # Read key from file
        key_path = input("Key file path to read: ").strip()
        key = read_text_file(key_path).strip()
        if not key:
            raise ValueError("Key file is empty.")

        return key

    # Invalid input handling
    raise ValueError("Invalid choice.")


def main() -> None:
    """
    Main program entry point.
    Handles user interaction, file input/output,
    and encryption or decryption process.
    """
    print("Program A: Encryption/Decryption")
    print("Modes:")
    print("  1) Encrypt a file")
    print("  2) Decrypt a file")

    # Select program mode
    mode = input("Choose mode (1/2): ").strip()

    # Input and output file paths
    in_path = input("Input text file path: ").strip()
    out_path = input("Output text file path: ").strip()

    # Obtain encryption/decryption key
    key = get_key()

    # Read input file
    text = read_text_file(in_path)

    if mode == "1":
        # Preprocess text before encryption
        text = preprocess(text)
        result = encrypt(text, key)
        write_text_file(out_path, result)
        print("Done: file encrypted.")

    elif mode == "2":
        # Decrypt text without preprocessing
        result = decrypt(text, key)
        write_text_file(out_path, result)
        print("Done: file decrypted.")

    else:
        raise ValueError("Invalid mode.")


# Run the program only if this file is executed directly
if __name__ == "__main__":
    main()
