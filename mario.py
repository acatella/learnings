import cs50

while True:
    try:
        height = int(input("height: "))
    except ValueError:
        print("What? How can that be a height??")
        continue
    if (height > 23 or height <= 0):
        print("I can only print a positive number of rows up to 23 rows tall...")
        continue
    else:
        break

for i in range(height):
    diff = height - 1 - i
    spaces = ""
    xes = ""
    output = ""
    
    for j in range(diff):
        spaces += " "
    
    for k in range(i + 1):
        xes += "X"
    
    output = spaces + xes + "  " + xes
    print (output)
    

