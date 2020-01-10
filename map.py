# Mr. Riley's map class v1.90208
#
# How to use Mr. Riley's map class...
# 1.) from map import *
# 2.) create a map instance: map = Map()
# 3.) draw/redraw the map inside the game loop: map.draw(roomList, itemList, currentlocation)
# Don't wanna show yer item locations? Do this: map.draw(roomList, False, currentlocation)


from turtle import *
import math


class Map(Turtle):
    def __init__(self):
        Turtle.__init__(self)
        self.speed(0)
        self.penup()
        self.screen = Screen()
        self.size = 400  # map window size
        self.mapBorder = 20
        self.roomSize = 20
        self.roomBorder = 2
        self.startingLocation = None
        self.columnHeight = 100
        self.screen.setup(self.size, self.size)
        self.screen.tracer(0)
        self.screen.bgcolor("black")
        self.roomColor = "white"
        self.startTextColor = "green"
        self.bigStarColor = "blue"
        self.littleStarColor = "orange"
        self.screen.register_shape(
            "bigStar",
            (
            (-10, -6.5),
            (10, 0),
            (-10, 6.5),
            (2.5, -10),
            (2.5, 10),
            (-10, -6.5)
            ),
        )
        self.littleStarSize = 4
        self.screen.register_shape(
            "littleStar",
            (
                (-10 / self.littleStarSize, -6.5 / self.littleStarSize),
                (10 / self.littleStarSize, 0),
                (-10 / self.littleStarSize, 6.5 / self.littleStarSize),
                (2.5 / self.littleStarSize, -10 / self.littleStarSize),
                (2.5 / self.littleStarSize, 10 / self.littleStarSize),
                (-10 / self.littleStarSize, -6.5 / self.littleStarSize),
            ),
        )
        # reveal instance variables
        self.revealDistance = 2
        self.revealWallColor = "gray"
        self.mappedRooms = []
        self.mappedItems = []
        for i in range(1999):
            self.mappedRooms.append(None)
            self.mappedItems.append(False)

    def setBackgroundColor(self, color="black"):
        self.screen.bgcolor(color)

    def setRoomColor(self, color="white"):
        self.roomColor = color

    def setRevealWallColor(self, color="gray"):
        self.revealWallColor = color

    def setBigStarColor(self, color="red"):
        self.bigStarColor = color

    def setLittleStarColor(self, color="gold"):
        self.littleStarColor = color

    def setTextColor(self, color):
        self.startTextColor = color

    # if there is no starting location, set it
    def setStartingLocation(self, myLocation):
        if self.startingLocation is None:
            self.startingLocation = myLocation

    # transfer rooms within the reveal distance from the rooms array to the mapped rooms array
    def mapTheSurroundingArea(self, myLocation, rooms, roomItems):
        for row in range(
            myLocation % self.columnHeight - self.revealDistance,
            myLocation % self.columnHeight + self.revealDistance + 1,
        ):
            for col in range(
                myLocation // self.columnHeight * self.columnHeight
                - self.revealDistance * self.columnHeight,
                myLocation // self.columnHeight * self.columnHeight
                + self.revealDistance * self.columnHeight
                + self.columnHeight,
                self.columnHeight,
            ):
                try:
                    self.mappedRooms[row + col] = rooms[row + col]
                    self.mappedItems[row + col] = roomItems[row + col]
                except:
                    pass

    # if there is a room here, stamp a square at the current row and column
    def drawRoom(self, row, column, roomArray):
        try:
            if roomArray[column * self.columnHeight + row]:
                self.color(self.roomColor)
                self.shape("square")
                self.goto(
                    -self.size / 2
                    + (self.roomSize / 2)
                    + column * (self.roomSize + self.roomBorder)
                    + self.mapBorder,
                    self.size / 2
                    - (self.roomSize / 2)
                    - row * (self.roomSize + self.roomBorder)
                    - self.mapBorder,
                )
                self.stamp()
        except:
            pass

    # if there is a revealed wall here, stamp a square at the current row and column
    def drawRevealedWall(self, row, column, roomArray):
        try:
            if roomArray[column * self.columnHeight + row] is False:
                self.color(self.revealWallColor)
                self.shape("square")
                self.goto(
                    -self.size / 2
                    + (self.roomSize / 2)
                    + column * (self.roomSize + self.roomBorder)
                    + self.mapBorder,
                    self.size / 2
                    - (self.roomSize / 2)
                    - row * (self.roomSize + self.roomBorder)
                    - self.mapBorder,
                )
                self.stamp()
        except:
            pass

    # if there is an item here, stamp a little star at the current row and column
    def drawLittleStar(self, row, column, itemArray):
        try:
            if itemArray[column * self.columnHeight + row]:
                self.color(self.littleStarColor)
                self.shape("littleStar")
                # self.goto(-self.size/2+(self.roomSize/2)+column*(self.roomSize+self.roomBorder)+self.mapBorder,self.size/2-(self.roomSize/2)-row*(self.roomSize+self.roomBorder)-self.mapBorder)
                self.stamp()
        except:
            pass

    # if there the startingLocation is here, write Start at the current row and column
    def drawStart(self, row, column, _startingLocation):
        if _startingLocation == column * self.columnHeight + row:
            self.color(self.startTextColor)
            self.back(self.roomSize / 2)
            self.write("Start", font=("Arial", 7, "normal"))
            self.forward(self.roomSize / 2)

    # if the currentlocation is here, stamp a big star at the current row and column
    def drawBigStar(self, row, column, myLocation):
        if myLocation == column * self.columnHeight + row:
            self.color(self.bigStarColor)
            self.shape("bigStar")
            self.stamp()

    # use the draw method to draw and redraw the map
    def draw(self, rooms, roomItems, myLocation):
        rowWidth = int(math.ceil(len(rooms) / self.columnHeight))
        self.penup()
        self.clear()
        self.setStartingLocation(myLocation)
        for row in range(self.columnHeight):
            for column in range(rowWidth):
                self.drawRoom(row, column, rooms)
                self.drawLittleStar(row, column, roomItems)
                self.drawStart(row, column, self.startingLocation)
                self.drawBigStar(row, column, myLocation)
        self.screen.update()

    # use the reveal method (instead of draw) to SLOWLY draw and reveal the map
    def reveal(self, rooms, roomItems, myLocation):
        self.mapTheSurroundingArea(myLocation, rooms, roomItems)
        rowWidth = int(math.ceil(len(rooms) / self.columnHeight))
        self.penup()
        self.clear()
        self.setStartingLocation(myLocation)
        for row in range(self.columnHeight):
            for column in range(rowWidth):
                self.drawRoom(row, column, self.mappedRooms)
                self.drawRevealedWall(row, column, self.mappedRooms)
                self.drawLittleStar(row, column, self.mappedItems)
                self.drawStart(row, column, self.startingLocation)
                self.drawBigStar(row, column, myLocation)
        self.screen.update()
