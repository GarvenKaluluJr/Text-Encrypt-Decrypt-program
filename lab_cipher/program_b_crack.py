# Program B: Cracking
# Frequency analysis + automatic correction using a dictionary.

# Used for random swapping of letter mappings during optimization
import random  

# Constant containing the English lowercase alphabet
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# Standard English letter frequency order (most frequent to least frequent)
EN_FREQ_ORDER = "etaoinshrdlucmfwypvbgkjqxz"


def read_text_file(path: str) -> str:
    """
    Read and return the entire contents of a text file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text_file(path: str, content: str) -> None:
    """
    Write the given content to a text file.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_dictionary(path: str) -> set[str]:
    """
    Load a dictionary file into a set.
    Only alphabetic lowercase words are kept.
    """
    words = set()  # Set for fast membership testing
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            w = line.strip().lower()
            # Keep only non-empty alphabetic words
            if w and w.isalpha():
                words.add(w)
    return words


def letter_frequencies(text: str) -> dict[str, int]:
    """
    Count the frequency of each letter in the given text.
    """
    # Initialize all letter counts to zero
    counts = {ch: 0 for ch in ALPHABET}

    # Count occurrences of each alphabet letter
    for ch in text.lower():
        if ch in counts:
            counts[ch] += 1

    return counts


def initial_mapping_by_frequency(ciphertext: str) -> dict[str, str]:
    """
    Build an initial substitution mapping based on letter frequency analysis.
    """
    # Compute letter frequencies in the ciphertext
    counts = letter_frequencies(ciphertext)

    # Sort cipher letters by descending frequency
    cipher_order = sorted(ALPHABET, key=lambda c: counts[c], reverse=True)

    mapping = {}          # Cipher to plain letter mapping
    used_plain = set()    # Track which plain letters are already used

    # Assign most frequent cipher letters to most frequent English letters
    for i, ciph_ch in enumerate(cipher_order):
        if i < 26:
            plain_ch = EN_FREQ_ORDER[i]
        else:
            plain_ch = None

        # Add mapping if the plain letter has not been used yet
        if plain_ch and plain_ch not in used_plain:
            mapping[ciph_ch] = plain_ch
            used_plain.add(plain_ch)

    # Fill remaining cipher letters with unused plain letters
    remaining_plain = [ch for ch in ALPHABET if ch not in used_plain]
    for ciph_ch in ALPHABET:
        if ciph_ch not in mapping:
            mapping[ciph_ch] = remaining_plain.pop(0)

    return mapping


def apply_mapping(ciphertext: str, cipher_to_plain: dict[str, str]) -> str:
    """
    Apply a cipher-to-plain mapping to the ciphertext.
    """
    # List to collect decrypted characters
    out = []  

    for ch in ciphertext.lower():
        if ch in cipher_to_plain:
            out.append(cipher_to_plain[ch])
        else:
            # Keep non-alphabet characters unchanged
            out.append(ch)

    return "".join(out)


def recognized_long_word_count(text: str, dictionary: set[str]) -> int:
    """
    Count recognized long words (> 5 letters) in the text.
    Long words are considered more reliable for correctness.
    """
    count = 0

    # Split text into whitespace-separated tokens
    for token in text.split():
        # Count only long alphabetic words present in the dictionary
        if len(token) > 5 and token.isalpha() and token in dictionary:
            count += 1

    return count


def improve_mapping_with_corrections(ciphertext: str,
                                    dictionary: set[str],
                                    mapping: dict[str, str],
                                    attempts: int = 20000) -> dict[str, str]:
    """
    Improve the initial mapping by randomly swapping letter assignments.
    A change is accepted only if it increases the recognized-word count.
    """
    # Store the current best mapping
    best = dict(mapping)

    # Apply the current best mapping
    best_plain = apply_mapping(ciphertext, best)

    # Evaluate initial score
    best_score = recognized_long_word_count(best_plain, dictionary)

    letters = list(ALPHABET)  # List of letters for random sampling

    for _ in range(attempts):
        # Randomly choose two letters to swap
        a, b = random.sample(letters, 2)

        # Create a candidate mapping by swapping two letters
        candidate = dict(best)
        candidate[a], candidate[b] = candidate[b], candidate[a]

        # Apply candidate mapping and evaluate it
        candidate_plain = apply_mapping(ciphertext, candidate)
        candidate_score = recognized_long_word_count(candidate_plain, dictionary)

        # Accept the candidate only if it improves the score
        if candidate_score > best_score:
            best = candidate
            best_score = candidate_score
        # Otherwise, the change is discarded automatically

    return best


def main() -> None:
    """
    Main program entry point for cracking the cipher text.
    """
    print("Program B: Cracking (frequency analysis + correction + dictionary)")

    # Read file paths from the user
    in_path = input("Encrypted text file path: ").strip()
    out_path = input("Output (cracked) text file path: ").strip()
    dict_path = input("Dictionary file path: ").strip()

    # Load encrypted text
    ciphertext = read_text_file(in_path)

    # Require sufficient text length for reliable frequency analysis
    if len(ciphertext) < 1000:
        raise ValueError("Encrypted text must contain at least 1000 characters.")

    # Load dictionary
    dictionary = load_dictionary(dict_path)

    # Initial decryption using frequency-based substitution
    mapping = initial_mapping_by_frequency(ciphertext)
    first_plain = apply_mapping(ciphertext, mapping)
    first_score = recognized_long_word_count(first_plain, dictionary)

    # Improve mapping using automatic corrections
    improved = improve_mapping_with_corrections(ciphertext, dictionary, mapping, attempts=20000)
    final_plain = apply_mapping(ciphertext, improved)
    final_score = recognized_long_word_count(final_plain, dictionary)

    # Use improved result only if it is actually better
    if final_score <= first_score:
        final_plain = first_plain

    # Write cracked text to output file
    write_text_file(out_path, final_plain)
    print("Done: cracked text written to output file.")


# Run the program only if executed directly
if __name__ == "__main__":
    main()
