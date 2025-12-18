Text Encryption, Decryption, and Cracking Project

This project implements a complete text encryption system and a cracking tool. It consists of two working programs written for the English language and designed to run on any computer using file-based input and output.

The first part of the project encrypts and decrypts text files using a Caesar cipher with a keyword. Before any encryption or decryption, the program requests a key. The key can be entered from the keyboard or read from a file, which is useful for long keys. The program also allows saving the key to a file. The source text is always read from a text file, and the result (encrypted or decrypted text) is written to a separate output file.

Before encryption, the text is preprocessed according to the required rules: all punctuation is removed, all letters are converted to a single case, and spaces are preserved. The encryption and decryption both use the same Caesar cipher with a keyword, operating on the English alphabet only.

The second part of this project cracks encrypted text without knowing the key. It uses letter frequency analysis combined with a dictionary-based automatic correction mechanism. The encrypted input text is read from a file and must contain at least 1000 characters to ensure reliable frequency analysis. A dictionary is used for automatic word recognition; it can either be downloaded from the internet or generated from a large book by extracting words, sorting them, and removing duplicates.

The cracking process works as follows: an initial substitution is performed based on letter frequency analysis, then an automatic correction step is applied to improve accuracy because real text frequencies differ from theoretical ones. After each correction, the program checks whether the number of recognized dictionary words has increased. If it has not, the correction is undone and another variant is tried. Longer words (more than five letters) are prioritized during recognition because short words are more likely to be misidentified.

Both encryption/decryption and cracking operate strictly through files: input text from a file, output to another file, and keys from the keyboard or a key file. 
Libraries needed: pip install random and string!
Language supported: English only.
