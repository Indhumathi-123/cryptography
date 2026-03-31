import math

def mod_inv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def caesar(text, key, encrypt=True):
    res = ""
    shift = key if encrypt else 26 - (key % 26)
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            res += chr((ord(char) - start + shift) % 26 + start)
        else:
            res += char
    return res

def playfair(text, keyword, encrypt=True):
    keyword = keyword.upper().replace('J', 'I')
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []
    seen = set()
    for char in keyword + alphabet:
        if char not in seen and char.isalpha():
            seen.add(char); matrix.append(char)
    
    text = "".join([c.upper().replace('J', 'I') for c in text if c.isalpha()])
    prepared_text = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            prepared_text += a + 'X'; i += 1
        else:
            prepared_text += a + b; i += 2
    if len(prepared_text) % 2 != 0: prepared_text += 'X'

    res = ""
    move = 1 if encrypt else 4
    for i in range(0, len(prepared_text), 2):
        a, b = prepared_text[i], prepared_text[i+1]
        idx1, idx2 = matrix.index(a), matrix.index(b)
        r1, c1 = divmod(idx1, 5); r2, c2 = divmod(idx2, 5)
        if r1 == r2:
            res += matrix[r1*5 + (c1+move)%5] + matrix[r2*5 + (c2+move)%5]
        elif c1 == c2:
            res += matrix[((r1+move)%5)*5 + c1] + matrix[((r2+move)%5)*5 + c2]
        else:
            res += matrix[r1*5 + c2] + matrix[r2*5 + c1]
    return res

def hill(text, k, encrypt=True):
    text = "".join([c.upper() for c in text if c.isalpha()])
    while len(text) % 3 != 0: text += "X"
    det = (k[0]*(k[4]*k[8]-k[5]*k[7]) - k[1]*(k[3]*k[8]-k[5]*k[6]) + k[2]*(k[3]*k[7]-k[4]*k[6])) % 26
    inv_det = mod_inv(det, 26)
    if inv_det is None: return "Error: Matrix not invertible mod 26"

    if not encrypt:
        adj = [
            (k[4]*k[8]-k[5]*k[7]) % 26, (-(k[1]*k[8]-k[2]*k[7])) % 26, (k[1]*k[5]-k[2]*k[4]) % 26,
            (-(k[3]*k[8]-k[5]*k[6])) % 26, (k[0]*k[8]-k[2]*k[6]) % 26, (-(k[0]*k[5]-k[2]*k[3])) % 26,
            (k[3]*k[7]-k[4]*k[6]) % 26, (-(k[0]*k[7]-k[1]*k[6])) % 26, (k[0]*k[4]-k[1]*k[3]) % 26
        ]
        mat = [(v * inv_det) % 26 for v in adj]
    else:
        mat = k

    res = ""
    for i in range(0, len(text), 3):
        v = [ord(text[i+j]) - 65 for j in range(3)]
        for r in range(3):
            val = (mat[r*3]*v[0] + mat[r*3+1]*v[1] + mat[r*3+2]*v[2]) % 26
            res += chr(val + 65)
    return res

def main():
    while True:
        print("\n*** Cryptography Dashboard ***")
        print("1. Caesar\n2. Playfair\n3. Hill (3x3)\n4. Exit")
        choice = input("Select (1-4): ")
        if choice == '4': break
        mode = input("Mode (E/D): ").upper()
        encrypt = mode == 'E'
        text = input("Enter text: ")
        if choice == '1':
            key = int(input("Key (number): "))
            print("Result:", caesar(text, key, encrypt))
        elif choice == '2':
            key = input("Keyword: ")
            print("Result:", playfair(text, key, encrypt))
        elif choice == '3':
            print("Enter 9 numbers (space separated):")
            k = list(map(int, input().split()))
            if len(k) == 9: print("Result:", hill(text, k, encrypt))
            else: print("Error: 9 numbers required.")

if __name__ == "__main__":
    main()
