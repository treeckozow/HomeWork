def printColored(text, color):
    return '<p style="font-size: 50px; color: ' + color + ';">' + text + '</p>'

def printGreen(text):
    return printColored(text, "green")

def printRed(text):
    return printColored(text, "red")

def printBlack(text):
    return printColored(text, "black")