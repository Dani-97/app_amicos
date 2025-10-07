class MessageBuilderProvider():

    def __init__(self):
        self.message = []
        self.notified_widgets_list = []

    def add_notified(self, notified_widget):
        self.notified_widgets_list.append(notified_widget)

    def __notify_widgets__(self):
        for widget in self.notified_widgets_list:
            widget.update_message(self.message)

    def get_current_message(self):
        return self.message

    def update_message(self, new_message):
        self.message = new_message
        self.__notify_widgets__()

    def add_word_to_message(self, new_word):
        self.message.append(new_word)
        self.__notify_widgets__()

    def remove_last_word_from_message(self):
        self.message = self.message[:-1]
        self.__notify_widgets__()

    def clear_message(self):
        self.message = []
        self.__notify_widgets__()