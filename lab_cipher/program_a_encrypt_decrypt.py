# Program A: Encryption/Decryption
# Caesar method with a keyword (English alphabet)
# Works with input/output text files and supports key from file.

import string

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def preprocess(text: str) -> str:
    # Remove punctuation; convert to one case; keep spaces (and other whitespace).
    # Punctuation is removed (not replaced).
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator).lower()


def build_keyed_alphabet(keyword: str) -> str:
    kw = "".join(ch for ch in keyword.lower() if ch in ALPHABET)
    seen = set()
    unique = []
    for ch in kw:
        if ch not in seen:
            seen.add(ch)
            unique.append(ch)
    remaining = [ch for ch in ALPHABET if ch not in seen]
    keyed = "".join(unique + remaining)
    if len(keyed) != 26:
        raise ValueError("Invalid keyed alphabet construction.")
    return keyed


def encrypt(text: str, keyword: str) -> str:
    keyed = build_keyed_alphabet(keyword)
    enc_map = {ALPHABET[i]: keyed[i] for i in range(26)}
    out = []
    for ch in text:
        out.append(enc_map.get(ch, ch))
    return "".join(out)


def decrypt(text: str, keyword: str) -> str:
    keyed = build_keyed_alphabet(keyword)
    dec_map = {keyed[i]: ALPHABET[i] for i in range(26)}
    out = []
    for ch in text:
        out.append(dec_map.get(ch, ch))
    return "".join(out)


def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def get_key() -> str:
    print("Key input:")
    print("  1) Enter key from keyboard")
    print("  2) Read key from file")
    choice = input("Choose (1/2): ").strip()

    if choice == "1":
        key = input("Enter key (keyword): ").strip()
        if not key:
            raise ValueError("Key cannot be empty.")

        save = input("Save key to file? (y/n): ").strip().lower()
        if save == "y":
            key_path = input("Key file path to write: ").strip()
            write_text_file(key_path, key)
        return key

    if choice == "2":
        key_path = input("Key file path to read: ").strip()
        key = read_text_file(key_path).strip()
        if not key:
            raise ValueError("Key file is empty.")
        return key

    raise ValueError("Invalid choice.")


def main() -> None:
    print("Program A: Encryption/Decryption")
    print("Modes:")
    print("  1) Encrypt a file")
    print("  2) Decrypt a file")
    mode = input("Choose mode (1/2): ").strip()

    in_path = input("Input text file path: ").strip()
    out_path = input("Output text file path: ").strip()

    key = get_key()

    text = read_text_file(in_path)

    if mode == "1":
        text = preprocess(text)
        result = encrypt(text, key)
        write_text_file(out_path, result)
        print("Done: file encrypted.")

    elif mode == "2":
        result = decrypt(text, key)
        write_text_file(out_path, result)
        print("Done: file decrypted.")

    else:
        raise ValueError("Invalid mode.")


if __name__ == "__main__":
    main()
