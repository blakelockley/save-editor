import savefile

from trainer import print_trainer_summary, trainer_menu
from party import party_menu

def clear():
    print(chr(27) + "[2J")

def main(args):
    filename = args[1]
    
    savefile.set_version("RUBY")
    savefile.load(filename)
    
    print_trainer_summary()

    should_continue = True
    while should_continue:
        
        print()
        print("What would you like to edit?")
        
        options = [
            ("Trainer Info", trainer_menu),
            ("Party Pokemon", party_menu),
            ("Box Pokemon", lambda: print("...")),
            ("Items", lambda: print("...")),
        ]

        for (index, option) in enumerate(options):
            text, _ = option
            print(f"{index + 1}) {text}")
        
        print("q) Save and Quit")

        while True:
            try:
                selection = input("> ")
                clear()
                
                if (selection == "q"):
                    should_continue = False
                    break

                index = int(selection) - 1
                if not (0 <= index < len(options)):
                    raise ValueError
            
                text, fn = options[index]

                print(text)
                fn()

                break
            
            except Exception as e:
                print(e)
                print("Invalid input...")

    print("Saving changes...")
    savefile.write(filename)


if __name__ == "__main__":
    import sys
    main(sys.argv)