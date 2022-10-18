import random

def generateString(length):
    characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    result = ''
    while length:
        character = characters[random.randint(0, 61)]
        result += str(character)
        length -= 1

    return result

def createCode():
    access_code = generateString(4) + "-" + generateString(4) + "-" + generateString(4) + "-" + generateString(4)
    return access_code