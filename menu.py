class Menu:
    def __init__(self, *args):
        self.title = "Menu"
        self.quit_text = "Close"
        self.options = []

        self.build_args = args
        self.build(*args)

    # Setters

    def set_title(self, text):
        self.title = text

    def set_quit_text(self, text):
        self.quit_text = text

    def add_option(self, text, option):
        self.options.append((text, option))

    # Overridable Methods

    def build(self, *args):
        pass

    def select(self, selection):
        pass

    def close(self):
        pass

    # Concrete Methods

    def refresh(self):
        self.options = []
        self.build(*self.build_args)

    def clear(self):
        print(chr(27) + "[2J")

    def show(self):
        while True:
            selection = self._loop()

            if selection is None:
                break

            self.select(selection)
            self.refresh()

        self.close()

    def _loop(self):
        self.clear()
        print(self.title)

        pad = len(str(len(self.options) + 1)) + 1
        for (index, option) in enumerate(self.options, 1):
            nth = f"{index})".ljust(pad, " ")
            text, _ = option

            print(f"{nth} {text}")

        print(f"{'q)'.ljust(pad, ' ')} {self.quit_text}")

        while True:
            selection = input("> ")

            if selection == "q":
                return None

            try:
                index = int(selection) - 1
                if not (0 <= index < len(self.options)):
                    raise ValueError

            except ValueError:
                continue

            break

        text, option = self.options[index]
        print(text)

        return option
