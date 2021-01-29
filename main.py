import savefile

from menu import Menu

from party import party_menu
from box import box_menu
from trainer import print_trainer_summary, trainer_menu


def main(args):
    filename = args[1]
    
    savefile.set_version("RUBY")
    savefile.load(filename)
    
    print_trainer_summary()
    input("> [Enter] ")

    main_menu = Menu("What would you like to edit?")
    main_menu.add_option("Trainer Info", trainer_menu.show)
    main_menu.add_option("Party Pokemon", party_menu)
    main_menu.add_option("Box Pokemon", box_menu.show)
    main_menu.set_quit_text("[Save and Quit]")
    main_menu.show()
    
    print("Saving changes...")
    savefile.write(filename)


if __name__ == "__main__":
    import sys
    main(sys.argv)