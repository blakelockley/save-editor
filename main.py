import savefile

from trainer import *

def main(args):
    filename = args[1]
    
    savefile.set_version("RUBY")
    savefile.load(filename)

    savefile.write(filename)


if __name__ == "__main__":
    import sys
    main(sys.argv)