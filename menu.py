class Menu:
    
    def __init__(self, title):
        self.title = title
        self.options = []
        self.quit_text = "[Quit]"
        self.repeat_flag = True
        self.callback = None

    def set_quit_text(self, text):
        self.quit_text = text

    def set_repeat_flag(self, flag):
        self.repeat_flag = flag

    def set_callback(self, callback):
        self.callback = callback

    def add_option(self, text, value):
        self.options.append((text, value))

    def show(self):
        while True: 
            selection = self.loop()
            
            if selection is None:
                break
            
            if self.callback is not None:
                self.callback(selection)
            else:
                selection()

            if not self.repeat_flag:
                break

    def loop(self):
        self.clear()
        print(self.title)
        
        for (index, option) in enumerate(self.options, 1):
            text, _ = option
            print(f"{index}) {text}")

        print(f"q) {self.quit_text}")

        while True:
            selection = input("> ")
                
            if (selection == "q"):
                return None

            try:
                index = int(selection) - 1
                if not (0 <= index < len(self.options)):
                    raise ValueError
                  
            except Exception as e:
                print(e)
                continue

            break
        
        text, option = self.options[index]
        print(text)
        
        return option
            
    def clear(self):
        print(chr(27) + "[2J")

