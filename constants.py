class Constants():
    EMPTY = 0
    WALL = 1
    RIGHT_PATH = 2
    TRIED = 3
    TRIED2 = 4
    TRAVELER = 5
    DESTINATION = 6
    BOMB = 7
    WEIGHTEDNOD = 8
    FAKE_TRAVELER = 9
    HORIZONTAL = 0
    VERTICAL = 1

    weightedNodeVal = 2

    @staticmethod
    def increaseWeight():
        __class__.weightedNodeVal += 1
    
    @staticmethod
    def decreaseWeight():
        if(__class__.weightedNodeVal > 0):
            __class__.weightedNodeVal -= 1