class BTNode:
    def __init__(self, node_message):
        self.message = node_message
        self.no_node = None
        self.yes_node = None

    def query(self):
        if self.is_question():
            print(self.message)
            print("Enter 'y' for yes and 'n' for no: ")
            user_input = self.get_yes_or_no()
            if user_input == 'y':
                self.yes_node.query()
            else:
                self.no_node.query()
        else:
            self.on_query_object()

    def on_query_object(self):
        print(f"Are you thinking of a(n) {self.message}?")
        print("Enter 'y' for yes and 'n' for no: ")
        user_input = self.get_yes_or_no()
        if user_input == 'y':
            print("The Computer Wins")
        else:
            self.update_tree()

    def update_tree(self):
        print("You win! What were you thinking of?")
        user_object = input()
        print(f"Please enter a question to distinguish a(n) {self.message} from {user_object}: ")
        user_question = input()
        print(f"If you were thinking of a(n) {user_object}, what would the answer to that question be?")
        user_input = self.get_yes_or_no()
        if user_input == 'y':
            self.no_node = BTNode(self.message)
            self.yes_node = BTNode(user_object)
        else:
            self.yes_node = BTNode(self.message)
            self.no_node = BTNode(user_object)
        print("Thank you my knowledge has been increased")
        self.set_message(user_question)

    def is_question(self):
        return self.no_node is not None or self.yes_node is not None

    def get_yes_or_no(self):
        user_input = ' '
        while user_input != 'y' and user_input != 'n':
            user_input = input()[0].lower()
        return user_input

    # Mutator Methods
    def set_message(self, node_message):
        self.message = node_message

    def get_message(self):
        return self.message

    def set_no_node(self, node):
        self.no_node = node

    def get_no_node(self):
        return self.no_node

    def set_yes_node(self, node):
        self.yes_node = node

    def get_yes_node(self):
        return self.yes_node


# Example usage:
if __name__ == "__main__":
    root_node = BTNode("Is it a living thing?")
    root_node.set_no_node(BTNode("Rock"))
    root_node.set_yes_node(BTNode("Dog"))

    root_node.query()
