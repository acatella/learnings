

def firstCheck(cc):
    result = 0
    
    while(cc >= 1):
        
        # cut off one digit of card number and multiply by 2
        cc = cc // 10
        digit = (cc % 10) * 2
        
        # if it is over two digits long add each digit together
        if (digit > 9):
            result += digit % 10
            digit = digit // 10
        
        result += digit
        cc = cc // 10
    
    return result

def secondCheck(cc):
    result = 0
    
    while (cc >= 1):
        digit = cc % 10
        result += digit
        cc = cc // 100
        
    return result
    
def isValid(cc):
    
    firstResult = firstCheck(cc)
    secondResult = secondCheck(cc)
    checkSum = firstResult + secondResult
    
    if (checkSum % 10 == 0):
        return True
    else:
        return False
    
while True:
    try:
        cc = int(input("What's your card number (you can trust me): "))
    except ValueError:
        print("I dont think that is a valid number. No spaces or any special characters plz")
        continue
    if (isValid(cc) is True and cc > 1000000000000):
        
        ccStr = str(cc)
        firstDigit = int(ccStr[0])
        secondDigit = int(ccStr[1])
        sum = firstDigit + secondDigit
        
        if (firstDigit is 4):
            cardType = "Visa"
        elif (firstDigit is 3 and (sum is 7 or sum is 10)):
            cardType = "Amex"
        elif (firstDigit is 5 and ((5 < sum) and (sum > 11))):
            cardType = "Mastercard"
        else:
            print("That is not a valid credit card type. You may have been bamboozled or you are trying to bamboozle me. Not gonna happen!")
            break
        
        print(f"Sweet {cardType} you got there fam")
        break
    else:
        print("That is not a valid credit card. You may have been bamboozled or you are trying to bamboozle me. Not gonna happen!")
        break
