import sys

def say_hello(name):
    print(f"Hello, {name}!")

# Organizes and calls all other functions. 
# Can see what is being called in what order. 
def main():
    # This is different from the script in b.py 
    # If you run it without an argument, will return IndexError.
    # Must run py c.py Name 
    # if you put sys.argv[0], would use c.py as the arugment. 
    name = sys.argv[1]
    say_hello(name)

if __name__ == "__main__":
    main()