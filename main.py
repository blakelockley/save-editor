import menu
import savefile
from box import BoxMenu
from items import ItemMenu
from party import PartyMenu
from trainer import TrainerMenu, print_trainer_summary


class MainMenu(menu.Menu):
    def build(self):
        self.set_title("What would you like to edit?")
        self.add_option("Trainer Info", TrainerMenu)
        self.add_option("Items", ItemMenu)
        self.add_option("Party Pokemon", PartyMenu)
        self.add_option("Box Pokemon", BoxMenu)
        self.set_quit_text("Save and Quit")

    def select(self, selection):
        selection().show()


def main(args):
    filename = args[1]

    savefile.set_version("RUBY")
    savefile.load(filename)

    print_trainer_summary()
    input("> ")

    MainMenu().show()

    print("Saving changes...")
    savefile.write(filename)


if __name__ == "__main__":
    import sys

    main(sys.argv)
