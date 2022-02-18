import math

lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowercase_letters = list(lowercase)
uppercase_letters = list(uppercase)
emoji_unicodes = [ '\U0001F353', '\U0001F34F', '\U0001F349', '\U0001F347',
                   '\U0001F36C', '\U0001F36D', '\U0001F36F', '\U00002615',
                   '\U0001F3A0', '\U0001F3A1', '\U00002600', '\U0001F319',
                   '\U0001FA90', '\U00002744', '\U0001F380', '\U0001F33B',
                   '\U0001F337', '\U0001F41E', '\U0001F98B', '\U0001F9A2',
                   '\U0001F989', '\U0001F407', '\U0001F994', '\U0001F3D4',
                   '\U0001F340', '\U0001F335']

'''
# Just to check the emojis and make sure that the number of the emojis is 26
c = 0
for i in emoji_unicodes:
    print(i)
    c += 1

print(c)
'''

# Creating vigenere table consisting of the emojis

vigenere_table = [[0 for i in range(26)] for j in range(26)]
k = 0
for i in range (0, 26):
    for j in range (0, 26):
        vigenere_table[i][j] = emoji_unicodes[(j+k)%26]
    k += 1

#print(vigenere_table)


# For caesar cipher, the rotation will be the length of the key plus the smallest prime number that comes after
# the length and then, mod by 26.

def is_prime(n):
    flag = True
    if n>1:
        for i in range(2, n//2+1):
            if (n%i == 0):
                flag = False
                break
    elif (n == 1 or n <= 0):
        flag = False
    return flag

def next_prime(key):
    key_length = len(key)
    num = key_length + 1
    while True:
        if (is_prime(num)):
            break
        else:
            num += 1

    return num

def encrypt_caesar(text, key):
    rotation = ( next_prime(key) + len(key) ) % 26
    result = ''

    for i in text:
        if (i.islower()):
            ind = ( lowercase_letters.index(i) + rotation ) % 26
            result += lowercase_letters[ind]

        elif (i.isupper()):
            ind = ( uppercase_letters.index(i) + rotation ) % 26
            result += uppercase_letters[ind]

        else:
            result += i

    return result

def decrypt_caesar(text, key):
    rotation = ( next_prime(key) + len(key) ) % 26
    result = ''

    for i in text:
        if (i.islower()):
            ind = ( lowercase_letters.index(i) - rotation )
            if (ind < 0):
                ind += 26
            result += lowercase_letters[ind]

        elif (i.isupper()):
            ind = ( uppercase_letters.index(i) - rotation )
            if (ind < 0):
                ind += 26
            result += uppercase_letters[ind]

        else:
            result += i

    return result

# After Caesar, the text will be encrypted once more using transposition cipher

def encrypt_transposition(text, key):
    key = key.lower()
    col_num = len(key)
    row_num = math.ceil(len(text)/col_num)
    mx = [ [ 0 for i in range(col_num) ] for j in range(row_num) ]

    x = 0
    for i in range(0, row_num):
        for j in range (0, col_num):
            if (x < len(text)):
                mx[i][j] = text[x]
            else:
                mx[i][j] = ' '
            x += 1

    #print(mx)

    key_list = list(key)
    sorted_key_list = sorted(key_list)
    #print(sorted_key_list)
    #print(key_list)

    res = []
    indx = 0
    while indx < len(key_list):
        a = sorted_key_list.index(key_list[indx])
        res.append(a)
        indx += 1
        sorted_key_list[a] = ' '

    #print(res)
    sorted_res = sorted(res)
    #print(sorted_res)

    result = ''
    for i in range(0, len(res)):
        for j in range(0, row_num):
            result += mx[j][res.index(sorted_res[i])]

    return result

def decrypt_transposition(text, key):
    key = key.lower()
    col_num = len(key)
    row_num = math.ceil(len(text) / col_num)
    mx = [[0 for i in range(col_num)] for j in range(row_num)]
    ind = 0
    for i in range (0, col_num):
        for j in range(0, row_num):
            if (ind < len(text)):
                mx[j][i] = text[ind]
                ind += 1
            else:
                mx[j][i] = ' '

    key_list = list(key)
    sorted_key_list = sorted(key_list)
    #print(sorted_key_list)
    #print(key_list)

    res = []
    indx = 0
    while indx < len(key_list):
        a = sorted_key_list.index(key_list[indx])
        res.append(a)
        indx += 1
        sorted_key_list[a] = ' '

    #print(res)
    sorted_res = sorted(res)
    #print(sorted_res)

    result = ''
    for j in range(0, row_num):
        for i in range(0, len(res)):
            result += mx[j][sorted_res.index(res[i])]

    return result

#In the final stage, the text will be encrypted to emojis using vigenere cipher

def encrypt_vigenere(text, key):
    text_chars = list(text)
    key_chars = list(key)
    result = ''
    text = text.lower()
    for i in range(0, len(text_chars)):
        if ( text[i].isalpha() ):
            result += vigenere_table[lowercase_letters.index(text[i])][lowercase_letters.index(key_chars[i%len(key)])]
        else:
            result += text[i]

    #print(result)
    #print(len(result))
    return  result

def decrypt_vigenere(text, key):
    text_chars = list(text)
    key_chars = list(key)
    result = ''
    for i in range(0, len(text_chars)):
        if (text_chars[i].isascii() == False):
            for j in range (0, 26):
                c = vigenere_table[j][lowercase_letters.index(key_chars[i % len(key)])]
                if c == text_chars[i]:
                    result += lowercase_letters[j]
                    continue
        else:
            result += text_chars[i]
            continue

    #print(result)
    return result

def encryption(text, key):
    first = encrypt_caesar(text, key)
    second = encrypt_transposition(first, key)
    final = encrypt_vigenere(second, key)
    return final

def decryption(text, key):
    first = decrypt_vigenere(text, key)
    second = decrypt_transposition(first, key)
    final = decrypt_caesar(second, key)
    return final

if __name__ == "__main__":
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Welcome! \U0000270C')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    while True:
        operation = input("Choose the operation (type 'e' for encryption, 'd' for decryption and 'q' to quit): ")
        if (operation == 'e'):

            text = input("Enter the text to encrypt: ")
            key = input("Enter the key: ")
            for i in key:
                if (i.isalpha() == False):
                    key = key.replace(i, '')
            print(encryption(text, key))

        elif (operation == 'd'):

            text = input("Enter the text to decrypt: ")
            key = input("Enter the key: ")
            for i in key:
                if (i.isalpha() == False):
                    key  = key.replace(i, '')
            print(decryption(text, key))
            print("(If you do not get the desired result, make sure that the cipher text is in correct format (26 unicode emojis) \n"
            ", all the white spaces are included and correct key is entered!)")

        elif (operation == 'q'):
            print("Goodbye! \U0001F44B")
            break
        else:
            print("Wrong operation! ")
            continue
