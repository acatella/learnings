import cs50
import sys

keyword = str(sys.argv[1])

# validate input
if (len(sys.argv) is not 2 or len(keyword) < 1 or keyword.isalpha() is False):
    print("Please enter a secret key")
    exit(1)

keyLen = len(keyword)
iter = 0

print("plaintext: ", end="")
plaintext = cs50.get_string()
output = []

for char in plaintext:
    
    #determine which letter of key to use
    if (iter >= keyLen):
        j = iter % keyLen
    else:
        j = iter
    
    #convert key letter to correct case then make it usable key
    key = ord(keyword[j].upper()) - 65

    code = ord(char)
    newCode = code + key
    if (code > 96 and code < 123):
        if (newCode > 122):
            newCode = newCode - 122 + 96
        output.append(chr(newCode))
        iter += 1
    elif (code > 64 and code < 91):
        if (newCode > 90):
            newCode = newCode - 90 + 64
        output.append(chr(newCode))
        iter += 1
    else:
        output.append(char)
    
    
otptText = "".join(output)
print(otptText)
        
    
    