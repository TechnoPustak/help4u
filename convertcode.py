import string
alphabet_string = string.ascii_lowercase
alphabet_list = list(alphabet_string)
symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '_', ';', ':', '(', ')',
           '{', '}', '[', ']' ,'/', '<', '>', ',', '.', '?', '+']

def convertcode(txt):
    result = ''
    for pos, j in enumerate(txt):
        if j in alphabet_list:
            index = alphabet_list.index(j)
            if pos % 2 == 0:
                if j == 'z':
                    result+='a'
                else:
                    result += alphabet_list[index+1]
            else:
                result += alphabet_list[index-1]
        elif j.isdigit():
            j = int(j)
            if pos%2==0:
                if  j == 9:
                    j = 0
                else:
                    j += 1
            else:
                if j == 0:
                    j = 9
                else:
                    j -= 1
            result += str(j)
        elif j in symbols:
            index = symbols.index(j)
            if pos % 2 == 0:
                if j == '+':
                    result+='!'
                else:
                    result += symbols[index+1]
            else:
                result += symbols[index-1]
        else:
            result += j
    return result

def decodecode(txt):
    result = ''
    for pos, j in enumerate(txt):
        if j in alphabet_list:
            index = alphabet_list.index(j)
            if pos % 2 == 0:
                result += alphabet_list[index-1]
            else:
                if j == 'z':
                    result+='a'
                else:
                    result += alphabet_list[index+1]
        elif j.isdigit():
            j = int(j)
            if pos%2==0:
                if j == 0:
                    j = 9
                else:
                    j -= 1
            else:
                if  j == 9:
                    j = 0
                else:
                    j += 1
            result += str(j)
        elif j in symbols:
            index = symbols.index(j)
            if pos % 2 == 0:
                result += symbols[index-1]
            else:
                if j == '+':
                    result+='!'
                else:
                    result += symbols[index+1]
        else:
            result += j
    return result

if __name__ == '__main__':
    pass

