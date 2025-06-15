from itertools import product

# Convert a seq of bits to a string of cap letters
def bits_to_string(bit_seq):
    chars = []
    for i in range(0, len(bit_seq), 8):
        byte = bit_seq[i:i+8]
        if len(byte) < 8:
            break  # Stop if we don't have enough bits for a full byte
        char = chr(int(''.join(str(bit) for bit in byte), 2))
        if 'A' <= char <= 'Z':  # Check if it's caps
            chars.append(char)
        else:
            return ''  # Return an empty string if it's not a valid letter
    return ''.join(chars)

# Generate the LFSR seq
def lfsr_seq(n, initial_state, coef): # Initial state; s0,s1,...,sn-1 #tap seq; coef a0,a1,...,an-1
    state = initial_state
    while True:
        yield state[0]
        next_bit = sum(s & t for s, t in zip(state, coef)) % 2
        state = state[1:] + (next_bit,)

def brute_force_lfsr(ciphertext):
    n_values = range(5, 8) # Adjusted to also check the 7
    found_solutions = []  # List to store found solutions

    for n in n_values:
        for initial_state in product([0, 1], repeat=n):
            for coef in product([0, 1], repeat=n):
                if sum(coef) == 0:
                    continue
                key_stream = lfsr_seq(n, initial_state, coef)
                key_bits = [next(key_stream) for _ in range(len(ciphertext))]
                plaintext_bits = [c ^ k for c, k in zip(ciphertext, key_bits)]
                plaintext = bits_to_string(plaintext_bits)
                
                if plaintext:
                    print(f'Found plaintext: {plaintext} with n={n}, state={initial_state}, coef={coef}')
                    found_solutions.append((plaintext, initial_state, coef))

    return found_solutions

# Ciphertext from textfile
ciphertext = [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0]  # Short example

# Calling brute force function
plaintext, state, coef = brute_force_lfsr(ciphertext)

if plaintext:
    print(f'The plaintext is: {plaintext}')
else:
    print('No valid plaintext found.')