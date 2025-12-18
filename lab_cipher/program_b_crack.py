# Program B: Cracking
# Frequency analysis + automatic correction using a dictionary.
# Reads ciphertext from file and writes cracked text to another file.

import random

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
EN_FREQ_ORDER = "etaoinshrdlucmfwypvbgkjqxz"


def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_dictionary(path: str) -> set[str]:
    words = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            w = line.strip().lower()
            if w and w.isalpha():
                words.add(w)
    return words


def letter_frequencies(text: str) -> dict[str, int]:
    counts = {ch: 0 for ch in ALPHABET}
    for ch in text.lower():
        if ch in counts:
            counts[ch] += 1
    return counts


def initial_mapping_by_frequency(ciphertext: str) -> dict[str, str]:
    counts = letter_frequencies(ciphertext)
    cipher_order = sorted(ALPHABET, key=lambda c: counts[c], reverse=True)

    mapping = {}
    used_plain = set()

    for i, ciph_ch in enumerate(cipher_order):
        if i < 26:
            plain_ch = EN_FREQ_ORDER[i]
        else:
            plain_ch = None

        if plain_ch and plain_ch not in used_plain:
            mapping[ciph_ch] = plain_ch
            used_plain.add(plain_ch)

    # Fill remaining cipher letters with remaining plain letters
    remaining_plain = [ch for ch in ALPHABET if ch not in used_plain]
    for ciph_ch in ALPHABET:
        if ciph_ch not in mapping:
            mapping[ciph_ch] = remaining_plain.pop(0)

    return mapping


def apply_mapping(ciphertext: str, cipher_to_plain: dict[str, str]) -> str:
    out = []
    for ch in ciphertext.lower():
        if ch in cipher_to_plain:
            out.append(cipher_to_plain[ch])
        else:
            out.append(ch)
    return "".join(out)


def recognized_long_word_count(text: str, dictionary: set[str]) -> int:
    # Long words (> 5 letters) are treated as reliable recognitions.
    count = 0
    for token in text.split():
        if len(token) > 5 and token.isalpha() and token in dictionary:
            count += 1
    return count


def improve_mapping_with_corrections(ciphertext: str,
                                    dictionary: set[str],
                                    mapping: dict[str, str],
                                    attempts: int = 20000) -> dict[str, str]:
    # Each accepted correction must increase recognized-word count;
    # otherwise it is undone and another correction is tried.
    best = dict(mapping)
    best_plain = apply_mapping(ciphertext, best)
    best_score = recognized_long_word_count(best_plain, dictionary)

    letters = list(ALPHABET)

    for _ in range(attempts):
        a, b = random.sample(letters, 2)

        candidate = dict(best)
        candidate[a], candidate[b] = candidate[b], candidate[a]

        candidate_plain = apply_mapping(ciphertext, candidate)
        candidate_score = recognized_long_word_count(candidate_plain, dictionary)

        if candidate_score > best_score:
            best = candidate
            best_score = candidate_score
        # else: automatically undo by discarding candidate

    return best


def main() -> None:
    print("Program B: Cracking (frequency analysis + correction + dictionary)")

    in_path = input("Encrypted text file path: ").strip()
    out_path = input("Output (cracked) text file path: ").strip()
    dict_path = input("Dictionary file path: ").strip()

    ciphertext = read_text_file(in_path)
    if len(ciphertext) < 1000:
        raise ValueError("Encrypted text must contain at least 1000 characters.")

    dictionary = load_dictionary(dict_path)

    # First substitution step: frequency-based mapping
    mapping = initial_mapping_by_frequency(ciphertext)
    first_plain = apply_mapping(ciphertext, mapping)
    first_score = recognized_long_word_count(first_plain, dictionary)

    # Automatic correction step (must increase recognized words, otherwise undone)
    improved = improve_mapping_with_corrections(ciphertext, dictionary, mapping, attempts=20000)
    final_plain = apply_mapping(ciphertext, improved)
    final_score = recognized_long_word_count(final_plain, dictionary)

    # After correction, ensure recognized-word count increased; otherwise revert to first result
    if final_score <= first_score:
        final_plain = first_plain

    write_text_file(out_path, final_plain)
    print("Done: cracked text written to output file.")


if __name__ == "__main__":
    main()
