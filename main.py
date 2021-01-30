import menu
import savefile
from box import BoxMenu, WipeBoxMenu
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
        self.add_option("Wipe ALL Box Data", WipeBoxMenu)
        self.set_quit_text("Save and Quit")

    def select(self, selection):
        selection().show()


def main(args):
    filename = args[1]

    savefile.load(filename)

    print_trainer_summary()
    input("> ")

    MainMenu().show()

    print("Saving changes...")
    savefile.write(filename)


if __name__ == "__main__":
    import sys

    main(sys.argv)
