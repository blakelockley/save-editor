import savefile

from trainer import *

def main(args):
    filename = args[1]
    
    savefile.set_version("RUBY")
    savefile.load(filename)
    print("Starting changes...\n")
    
    # Trainer
    
    name = get_trainer_name()
    new_name = input(f"Set name ({name}): ")
    if len(new_name) > 0:
        print("Changing name to...", new_name)
        set_trainer_name(new_name)
    
    gender = get_trainer_gender()
    new_gender = input(f"Set gender M/F ({gender}): ")
    if len(new_gender) > 0:
        print("Changing gender to...", new_gender)
        set_trainer_gender(new_gender)

    print("\nCompleted changes.")
    savefile.write(filename)


if __name__ == "__main__":
    import sys
    main(sys.argv)