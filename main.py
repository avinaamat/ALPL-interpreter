from interpreter import Interpreter
import sys


def main():
    if len(sys.argv) > 1:
        interpreter = Interpreter(sys.argv[1])
        interpreter.run()
    else:
        raise Exception("No file was given to run")


if __name__ == "__main__":
    main()
