from random import randint

def getRandomBark():
    ran = randint(0, 4)
    if ran == 0:
        return "woof"
    elif ran == 1:
        return "bark"
    elif ran == 2:
        return "garuru"
    else:
        return "awoo"

    
