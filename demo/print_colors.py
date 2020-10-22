from denver import ctext

for x in ctext.ColoredText.cloredTextEscapeSequenceFore.keys():
    ctext.print(" ", back=x, end="", style="none")
    print(" "+x)

if __name__ == '__main__':
    pass
