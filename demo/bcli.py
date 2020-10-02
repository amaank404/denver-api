from denver import bcli

cli = bcli.new_cli()

cli.info("This is a test")
cli.good("Works Well")
cli.bad("Might be not as expected")
cli.run("But let's run this")

print("\n\n")

# Number Adder
number = cli.input("Number 1 >")
number2 = cli.input("Number 2 >")

# Lets validate them
if number.isnumeric() and number2.isnumeric():
    cli.good("All the numbers are valid")
else:
    cli.bad("The numbers are supposed to be Integers")
    raise SystemExit(1)

# Lets convert them to integers
cli.info("Conversion to integers started")
number = int(number)
cli.run("Number Converted")
number2 = int(number2)
cli.run("Number 2 Converted")
cli.good("All numbers Converted to integer")

# Lets add them
try:
    result = number + number2
    cli.good("Numbers added")
except:
    cli.bad("Numbers could not be added")
    raise SystemExit(1)

cli.info("Result is", result)
