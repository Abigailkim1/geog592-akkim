import argparse 

def say_hello(name, times):
    for i in range(times):
        print(f"Hello, {name}!")

# py c.py --help prints the help messages.
# Positional arguemnts, the order matters. 
# --times is a named argument, can put in any order 
# py c.py --times 5 Abigail still works. 
def main():
    parser = argparse.ArgumentParser(
        description = "A program that greets soemeone."
    )
    parser.add_argument("name", help="Name of person to greet")
    # Argument for how many times the greeting should print.
    parser.add_argument(
        "--times", type=int, default=1,
        help="Number of greetings (default: 1)"
    )
    args = parser.parse_args()
    say_hello(args.name, args.times)

if __name__ == "__main__":
    main()
