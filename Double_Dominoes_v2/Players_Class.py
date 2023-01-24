class Player:
    """
    Player class to store tiles the player holds
    """
    
    def __init__(self, name, user):
        self.name = name
        self.tiles = []
        self.user = user