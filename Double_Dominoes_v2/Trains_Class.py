class Train:
    """
    Train class to store the values of played tiles.
    Has a bool status attribute that keeps track of whether a train is open/closed.
    Store is a list which has all the tiles that have been played on it.
    User is a boolean which determines if the train is that of an AI player or user
    """

    def __init__(self, name, display_name):
        self.name = name
        self.display_name = display_name
        self.last_tile = 12
        self.open = False
        self.store = [(12,12)]

    def get_status(self):
        return self.open

    def open_train(self):
        self.open = True

    def close_train(self):
        self.open = False
    

    