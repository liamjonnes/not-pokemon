# Imports the required modules for the game
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math

CANVAS_WIDTH = 920
CANVAS_HEIGHT = 700
WIDTH = CANVAS_WIDTH
HEIGHT = CANVAS_HEIGHT
BATTLE_ON = False
VERTICAL_DIVIDERS = 10
HORIZONTAL_DIVIDERS = 10
PLAYER_ALIVE = True
map = 0
score = 0
beenHealed = False
IMG_ROT = 0


# A class for creating and manipulating vectors
class Vector:
    # Initialiser
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def getP(self):
        return (self.x, self.y)

    # Returns a copy of the vector
    def copy(self):
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    # Creates a copy of the current vector and adds another
    def __add__(self, other):
        return self.copy().add(other);

    # Negates the vector (makes it point in the opposite direction)
    def negate(self):
        return self.multiply(-1)

    # Creates a copy of the current vector and negates it
    def __neg__(self):
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other):
        return self.add(-other)

    # Creates a copy of the current vector and subtracts another
    def __sub__(self, other):
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    # Creates a copy of the current vector and multiplies it by another
    def __mul__(self, k):
        return self.copy().multiply(k)

    # Copy of the above ^^^^
    def __rmul__(self, k):
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k):
        return self.multiply(1 / k)

    # Creates a copy of the current vector and divides it by another
    def __truediv__(self, k):
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self):
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def getNormalized(self):
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # Returns the squared length of the vector
    def lengthSquared(self):
        return self.x ** 2 + self.y ** 2

    # Reflect this vector on a normal
    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2 * self.dot(normal))
        self.subtract(n)
        return self


# Manages the keyboard input
class Keyboard:
    # Initialises the variables to determine whether a key is pressed
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.run = False

    # If a key is down, set its corresponding variable to True
    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['up']:
            self.up = True
        if key == simplegui.KEY_MAP['down']:
            self.down = True
        if key == simplegui.KEY_MAP['space']:
            self.run = True

    # If a key is up, set its corresponding variable to False
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['up']:
            self.up = False
        if key == simplegui.KEY_MAP['down']:
            self.down = False
        if key == simplegui.KEY_MAP['space']:
            self.run = False


# Creates each map and collisions within the map, and adds any relevant NPCs
class Map:
    # Initialises the maps and collisions
    def __init__(self, ImageWidthHeight):
        global map
        global BATTLE_ON

        self.mushroom = "https://orig00.deviantart.net/d700/f/2008/315/4/e/red_mushroom_by_slashingoverlord.png"
        self.M0LevelUp = Pokeballs(self.mushroom, (256, 256), (590, 460))
        self.M1LevelUp = Pokeballs(self.mushroom, (256, 256), (675, 575))
        self.M2LevelUp = Pokeballs(self.mushroom, (256, 256), (780, 570))
        self.M4LevelUp = Pokeballs(self.mushroom, (256, 256), (725, 290))
        self.M5LevelUp = Pokeballs(self.mushroom, (256, 256), (250, 200))
        self.M6LevelUp = Pokeballs(self.mushroom, (256, 256), (460, 500))

        self.M0LevelUpHB = collision(580, 600, 430, 4700)
        self.M0LevelUp1 = False
        self.M1LevelUpHB = collision(665, 685, 565, 585)
        self.M1LevelUp1 = False
        self.M2LevelUpHB = collision(770, 790, 560, 580)
        self.M2LevelUp1 = False
        self.M4LevelUpHB = collision(715, 735, 280, 300)
        self.M4LevelUp1 = False
        self.M5LevelUpHB = collision(240, 260, 190, 210)
        self.M5LevelUp1 = False
        self.M6LevelUpHB = collision(450, 480, 490, 510)
        self.M6LevelUp1 = False
        self.M3LevelUp1 = False

        # Finaly Boss
        self.enemyRed = [
            Enemy("OnionKnight", random.randint(140, 160), random.randint(130, 150), random.randint(140, 160),
                  random.randint(130, 150), (2, 0)),
            Enemy("WaterBowser", random.randint(140, 160), random.randint(140, 160), random.randint(140, 160),
                  random.randint(150, 170), (8, 0)),
            Enemy("MyMixtape", random.randint(120, 140), random.randint(140, 160), random.randint(150, 170),
                  random.randint(140, 160), (5, 0))]

        # Level Bosses
        self.enemyBoss4 = [Enemy("MeTOO", random.randint(125, 145), random.randint(115, 135), random.randint(125, 145),
                                 random.randint(115, 135), (24, 5)),
                           Enemy("Ditto", random.randint(125, 145), random.randint(125, 145), random.randint(125, 145),
                                 random.randint(135, 155), (0, 6)),
                           Enemy("Diabetes", random.randint(105, 125), random.randint(125, 145),
                                 random.randint(135, 155),
                                 random.randint(125, 145), (23, 5))]

        self.enemyBoss3 = [
            Enemy("PuppyDaddySenpai", random.randint(115, 135), random.randint(105, 125), random.randint(115, 135),
                  random.randint(105, 125), (23, 9)),
            Enemy("RainbowBirb", random.randint(115, 135), random.randint(115, 135), random.randint(115, 135),
                  random.randint(125, 145), (24, 9)),
            Enemy("ArmouredCore", random.randint(95, 115), random.randint(115, 135), random.randint(125, 145),
                  random.randint(115, 135), (22, 9))]

        self.enemyBoss2 = [
            Enemy("Lipstick", random.randint(105, 125), random.randint(95, 115), random.randint(105, 125),
                  random.randint(95, 115), (8, 15)),
            Enemy("BluFsh", random.randint(105, 125), random.randint(105, 125), random.randint(105, 125),
                  random.randint(115, 135), (6, 15)),
            Enemy("Landlord", random.randint(85, 105), random.randint(105, 125), random.randint(115, 135),
                  random.randint(105, 125), (7, 15))]

        self.enemyBoss1 = [Enemy("WetDoggo", random.randint(95, 115), random.randint(85, 105), random.randint(95, 115),
                                 random.randint(85, 105), (8, 5)),
                           Enemy("SpikyDoggo", random.randint(95, 115), random.randint(95, 115),
                                 random.randint(95, 115),
                                 random.randint(105, 125), (9, 5)),
                           Enemy("BurntDogo", random.randint(75, 95), random.randint(95, 115), random.randint(105, 125),
                                 random.randint(95, 115), (10, 5))]

        # Level Trainers
        self.enemyTrainer5 = [Enemy("EdgeLord", 120, 120, 120, 120, (8, 14)),
                              Enemy("CatchTheseHands", 130, 105, 120, 125, (11, 8)),
                              Enemy("LiquidSnek", 130, 100, 180, 100, (4, 5)),
                              Enemy("JoMama", 180, 110, 110, 100, (17, 5)),
                              Enemy("MomsSpaghetti", 125, 120, 120, 125, (10, 15))]

        self.enemyTrainer4 = [Enemy("PunchingBag", 200, 50, 175, 25, (1, 8)),
                              Enemy("American", 110, 100, 140, 80, (13, 11)),
                              Enemy("HeavyMetal", 110, 110, 110, 110, (5, 12)),
                              Enemy("RuleThirtyFour", 90, 120, 90, 120, (6, 11)),
                              Enemy("Thorny", 100, 120, 120, 90, (8, 1))]

        self.enemyTrainer3 = [Enemy("Smerfing", 95, 85, 85, 120, (4, 2)),
                              Enemy("MetaBroke", 100, 100, 100, 100, (0, 15)),
                              Enemy("NotLow", 90, 110, 110, 180, (20, 10)),
                              Enemy("Dumbo", 150, 65, 100, 75, (6, 9)), Enemy("TeenMom", 180, 55, 70, 55, (16, 9))]

        self.enemyTrainer2 = [Enemy("ShuckMe", 125, 50, 150, 50, (12, 8)),
                              Enemy("CrimsonChin", 100, 70, 70, 70, (7, 8)),
                              Enemy("KimK", 70, 20, 100, 100, (23, 4)),
                              Enemy("Shrooms", 85, 85, 85, 85, (10, 11)),
                              Enemy("BrainyBacon", 100, 80, 70, 80, (0, 13))]

        self.enemyTrainer1 = [Enemy("Bork", 50, 70, 50, 70, (8, 2)), Enemy("DayCare", 80, 30, 100, 30, (14, 4)),
                              Enemy("Thicc", 70, 60, 55, 55, (14, 14)),
                              Enemy("HepMe", 80, 75, 60, 45, (23, 7)), Enemy("MrSteelYoBirb", 50, 70, 65, 60, (1, 9))]

        # All starters balanced to 310 base total stats
        self.playerMon = [Player1("OnionKnight", 75, 75, 90, 70, (2, 0)), Player1("MyMixtape", 70, 90, 75, 75, (5, 0)),
                          Player1("WaterBowser", 75, 80, 80, 75, (8, 0)),
                          Player1("StingingPetals", 80, 70, 80, 80, (3, 6)),
                          Player1("CharGrilled", 75, 80, 75, 80, (6, 6)),
                          Player1("Waterbator", 80, 75, 80, 75, (9, 6)),
                          Player1("FeafyIsHere", 70, 85, 70, 85, (3, 10)),
                          Player1("BlazingChicken", 80, 85, 70, 75, (6, 10)),
                          Player1("MySwamp", 85, 85, 80, 60, (9, 10))]

        self.a = Player1("Choose Mon", 1, 1, 1, 1, (6, 5))
        self.b = Enemy("Bork", 1, 1, 1, 1, (0, 0))
        self.a.enemy = self.b
        self.b.player = self.a

        # map = 3  #Change this variable to the map that you want to go to.
        self.begin = True
        self.begin2 = False

        self.url = simplegui.load_image("https://image.ibb.co/jdF3sc/Capture_d_cran_2018_02_28_12_35_14.png")
        self.ImageWidthHeight = ImageWidthHeight
        self.ImageCenter = (ImageWidthHeight[0] / 2, ImageWidthHeight[1] / 2)
        self.CenterDest = (WIDTH / 2, HEIGHT / 2)
        self.DimDest = (WIDTH, HEIGHT)

        self.M0tree1 = collision(540, 590, 280, 380)
        self.M0tree2 = collision(435, 490, 165, 270)
        self.M0tree3 = collision(380, 430, 220, 325)
        self.M0tree4 = collision(595, 648, 165, 270)

        self.M1tree1 = collision(700, 920, 0, 150)
        self.M1tree2 = collision(375, 430, 220, 920)
        self.M1tree3 = collision(485, 600, 220, 920)
        self.M1tree4 = collision(0, 105, 0, 475)
        self.M1tree5 = collision(325, 380, 0, 150)

        self.M2tree1 = collision(100, 160, 475, 490)
        self.M2tree2 = collision(160, 215, 530, 640)
        self.M2tree3 = collision(270, 330, 260, 370)
        self.M2tree4 = collision(160, 225, 0, 45)

        self.M3tree1 = collision(160, 216, 370, 470)
        self.M3tree2 = collision(220, 275, 420, 520)
        self.M3tree3 = collision(325, 380, 370, 470)
        self.M3tree4 = collision(485, 540, 420, 520)
        self.M3tree5 = collision(590, 650, 370, 470)
        self.M3tree6 = collision(700, 750, 370, 470)

        self.M0border1 = collision(0, 646, 0, 155)
        self.M0border2 = collision(0, 150, 0, HEIGHT)
        self.M0border3 = collision(0, WIDTH, 540, HEIGHT)
        self.M0border4 = collision(760, WIDTH, 0, HEIGHT)
        self.M0border5 = collision(700, WIDTH, 0, 100)

        self.M1border1 = collision(756, WIDTH, 0, HEIGHT)
        self.M1border2 = collision(700, 920, 300, 520)
        self.M1border3 = collision(0, 920, 0, 90)
        self.M1border4 = collision(0, 220, 0, 200)
        self.M1border5 = collision(0, 160, 0, 360)
        self.M1border6 = collision(220, 600, 355, 700)
        self.M1border7 = collision(275, 600, 300, 355)
        self.M1border8 = collision(333, 600, 255, 300)
        self.M1border9 = collision(0, 240, 537, 700)

        self.M2border1 = collision(810, 920, 0, 470)
        self.M2border2 = collision(810, 920, 560, 700)
        self.M2border3 = collision(870, 920, 535, 700)
        self.M2border4 = collision(0, 55, 420, 700)
        self.M2border5 = collision(0, 55, 0, 370)
        self.M2border6 = collision(0, 920, 0, 20)
        self.M2border7 = collision(0, 920, 690, 700)
        self.M2border8 = collision(380, 430, 310, 415)

        self.M3border1 = collision(855, 920, 0, 360)
        self.M3border2 = collision(855, 920, 415, 700)
        self.M3border3 = collision(0, 50, 0, 300)
        self.M3border4 = collision(0, 50, 365, 700)
        self.M3border5 = collision(0, 920, 0, 45)
        self.M3border6 = collision(0, 920, 630, 700)

        self.Miborder1 = collision(815, 920, 0, 700)
        self.Miborder2 = collision(0, 115, 0, 700)
        self.Miborder3 = collision(0, 920, 0, 260)
        self.Miborder4 = collision(0, 920, 415, 700)

        self.M4border1 = collision(865, 920, 0, 290)
        self.M4border2 = collision(865, 920, 360, 700)
        self.M4border3 = collision(0, 650, 0, 200)
        self.M4border4 = collision(0, 920, 0, 140)
        self.M4border5 = collision(0, 545, 0, 310)
        self.M4border6 = collision(0, 490, 0, 365)
        self.M4border7 = collision(0, 100, 0, 700)
        self.M4border8 = collision(0, 170, 530, 700)
        self.M4border9 = collision(0, 920, 595, 700)
        self.M4border10 = collision(800, 920, 525, 700)

        self.M5border1 = collision(0, 230, 0, 210)
        self.M5border2 = collision(0, 285, 0, 150)
        self.M5border3 = collision(0, 920, 0, 100)
        self.M5border4 = collision(865, 920, 0, 700)
        self.M5border5 = collision(0, 65, 0, 700)
        self.M5border6 = collision(0, 220, 575, 700)
        self.M5border7 = collision(270, 920, 580, 700)
        self.M5border8 = collision(325, 920, 530, 700)
        self.M5border10 = collision(535, 920, 475, 700)
        self.M5border11 = collision(480, 810, 155, 420)
        self.M5border12 = collision(115, 260, 260, 410)
        self.M5border13 = collision(115, 210, 260, 520)

        self.M6border1 = collision(650, 920, 0, 700)
        self.M6border2 = collision(0, 275, 0, 920)
        self.M6border3 = collision(0, 920, 0, 150)
        self.M6border4 = collision(0, 385, 200, 365)
        self.M6border5 = collision(540, 920, 200, 365)
        self.M6border6 = collision(0, 380, 580, 700)
        self.M6border7 = collision(430, 920, 580, 700)

        self.Ball = "http://pixelartmaker.com/art/797ff81281c7a32.png"
        self.M0Ball1 = Pokeballs(self.Ball, (1700, 1700), (300, 245))
        self.M0Ball2 = Pokeballs(self.Ball, (1700, 1700), (250, 245))
        self.M0Ball3 = Pokeballs(self.Ball, (1700, 1700), (350, 245))

        self.M0BallBorder1 = collision(225, 275, 216, 250)
        self.M0BallBorder2 = collision(275, 330, 216, 250)
        self.M0BallBorder3 = collision(330, 375, 216, 250)

        self.Nurse = "https://orig00.deviantart.net/c2c9/f/2013/094/a/8/joy_by_innermobius-d60e19z.png"
        self.M0Nurse1 = NurseJoy(self.Nurse, (272 / 4, 288 / 4), (730, 135))
        self.M1Nurse1 = NurseJoy(self.Nurse, (272 / 4, 288 / 4), (240, 130))
        self.M2Nurse1 = NurseJoy(self.Nurse, (272 / 4, 288 / 4), (500, 90))
        self.MiNurse1 = NurseJoy(self.Nurse, (272 / 4, 288 / 4), (730, 290))
        self.M4Nurse1 = NurseJoy(self.Nurse, (272 / 4, 288 / 4), (430, 500))
        self.M5Nurse1 = NurseJoy(self.Nurse, (272 / 4, 288 / 4), (80, 300))

        self.Trainer0 = "https://orig00.deviantart.net/c9d6/f/2011/137/2/2/kymotonian_wally_complete_by_rafael_animal-d3gk331.png"
        self.M0Trainer = Trainers(self.Trainer0, (64, 64), (675, 70))
        self.M0TrainerBorder = collision(645, 705, 20, 100)
        self.fight = False

        self.Trainer1 = "https://i.imgur.com/FzG6j3L.png"
        self.M1Trainer = Trainers(self.Trainer1, (64, 64), (65, 500))
        self.M1TrainerBorder = collision(0, 75, 470, 540)
        self.fight1 = False

        self.Trainer2 = "https://i.imgur.com/sQ2Dd0e.png"
        self.M2Trainer = Trainers(self.Trainer2, (64, 64), (565, 500))
        self.M2TrainerBorder = collision(555, 580, 470, 530)
        self.fight2 = False

        self.Trainer21 = "https://i.imgur.com/b4Mtzsv.png"
        self.M21Trainer = Trainers(self.Trainer21, (64, 64), (630, 145))
        self.M21TrainerBorder = collision(580, 680, 120, 160)
        self.fight21 = False

        self.Trainer3 = "https://i.imgur.com/FqzfZzk.png"
        self.M3Trainer = Trainers(self.Trainer3, (64, 64), (280, 610))
        self.M3TrainerBorder = collision(265, 295, 580, 700)
        self.fight3 = False

        self.Trainer31 = "https://i.imgur.com/dky9sEx.png"
        self.M31Trainer = Trainers(self.Trainer31, (64, 64), (785, 215))
        self.M31TrainerBorder = collision(765, 810, 200, 230)
        self.fight31 = False

        self.Trainer4 = "https://i.imgur.com/NOBDCGR.png"
        self.M4Trainer = Trainers(self.Trainer4, (64, 64), (675, 240))
        self.M4TrainerBorder = collision(650, 700, 200, 260)
        self.fight4 = False

        self.Trainer41 = "https://i.imgur.com/NOBDCGR.png"
        self.M41Trainer = Trainers(self.Trainer41, (64, 64), (241, 385))
        self.M41TrainerBorder = collision(220, 255, 370, 400)
        self.fight41 = False

        self.Trainer5 = "https://cdn.discordapp.com/attachments/416163882189717544/421340540722872321/brenddownvec.png"
        self.M5Trainer = Trainers(self.Trainer5, (64, 64), (405, 105))
        self.M5TrainerBorder = collision(385, 430, 0, 125)
        self.fight5 = False

        self.Trainer51 = "https://i.imgur.com/HXZ5hUp.png"
        self.M51Trainer = Trainers(self.Trainer51, (64, 64), (570, 410))
        self.M51TrainerBorder = collision(550, 600, 320, 425)
        self.fight51 = False

        self.Trainer6 = "https://cdn.discordapp.com/attachments/416163882189717544/421339793394237450/redvec.png"
        self.M6Trainer = Trainers(self.Trainer6, (64, 64), (460, 175))
        self.M6TrainerBorder = collision(410, 515, 0, 200)
        self.fight6 = False

        self.M0NurseBorder = collision(700, 755, 100, 164)
        self.M1NurseBorder = collision(220, 265, 90, 150)
        self.M2NurseBorder = collision(475, 525, 50, 110)
        self.MiNurseBorder = collision(700, 750, 260, 300)
        self.M4NurseBorder = collision(400, 460, 470, 530)
        self.M5NurseBorder = collision(0, 120, 270, 330)

        self.M0nextMap = collision(640, 700, -10, 40)
        self.M1nextMap = collision(0, 30, 350, 540)
        self.M2nextMap = collision(0, 30, 350, 540)
        self.M3nextMap = collision(0, 20, 295, 370)
        self.M4nextMap = collision(220, 270, 360, 367)
        self.M5nextMap = collision(375, 435, 100, 102)

        self.M1previousMap = collision(550, 800, 690, 700)
        self.M2previousMap = collision(890, 920, 450, 550)
        self.M3previousMap = collision(885, 920, 300, 420)
        self.MipreviousMap = collision(650, 700, 415, 475)
        self.M4previousMap = collision(895, 920, 250, 370)
        self.M5previousMap = collision(215, 275, 650, 700)
        self.M6previousMap = collision(375, 435, 640, 700)

        self.M2river1 = collision(665, 850, 0, 80)
        self.M2river2 = collision(600, 740, 55, 250)
        self.M2river3 = collision(230, 315, 0, 90)
        self.M2river4 = collision(230, 420, 50, 90)
        self.M2river5 = collision(230, 420, 140, 185)
        self.M2river6 = collision(275, 425, 185, 300)
        self.M2river7 = collision(340, 635, 200, 350)
        self.M2river8 = collision(550, 700, 240, 300)
        self.M2river9 = collision(450, 580, 340, 390)
        self.M2river10 = collision(500, 580, 350, 470)
        self.M2river11 = collision(500, 645, 430, 470)
        self.M2river12 = collision(500, 645, 525, 700)
        self.M2river13 = collision(440, 700, 585, 920)
        self.M2river14 = collision(390, 700, 645, 920)

        self.M3house1 = collision(485, 760, 100, 300)
        self.M3house2 = collision(160, 435, 100, 300)

        self.M3door1 = collision(325, 385, 300, 305)
        self.M3door2 = collision(645, 700, 300, 305)

        self.Mifurniture1 = collision(700, 920, 300, 375)
        self.Mifurniture2 = collision(0, 655, 0, 300)
        self.Mifurniture3 = collision(0, 165, 0, 700)
        self.Mifurniture4 = collision(215, 270, 0, 360)
        self.Mifurniture5 = collision(325, 380, 0, 360)

        self.M0NPC1 = NPCs((470, 345),
                           "https://orig00.deviantart.net/9f10/f/2011/137/a/1/kymotonian_birch_complete_by_rafael_animal-d3gk2yc.png",
                           (256, 256), 0, 0)
        self.M0MPCBorder1 = collision(445, 495, 310, 365)

        self.M1NPC1 = NPCs((731, 200),
                           "https://orig00.deviantart.net/a375/f/2011/137/a/3/kymotonian_bugcatcher_complete_by_rafael_animal-d3gk7fw.png",
                           (256, 256), 0, 1)
        self.M1MPCBorder1 = collision(700, 920, 150, 220)
        self.fight11 = False
        self.M1NPC2 = NPCs((460, 250),
                           "https://orig00.deviantart.net/2416/f/2011/137/e/b/kyle_rival_mother_complete__by_rafael_animal-d3gkcca.png",
                           (256, 256), 0, 3)
        self.M1MPCBorder2 = collision(430, 485, 225, 255)
        self.fight12 = False
        self.M1NPC3 = NPCs((135, 400),
                           "https://orig00.deviantart.net/a375/f/2011/137/a/3/kymotonian_bugcatcher_complete_by_rafael_animal-d3gk7fw.png",
                           (256, 256), 0, 2)
        self.M1MPCBorder3 = collision(100, 160, 360, 400)
        self.fight13 = False

        self.M2NPC1 = NPCs((720, 340),
                           "https://orig00.deviantart.net/1b0f/f/2011/137/d/a/kymotonian_roxanne_complete_by_rafael_animal-d3gkbqi.png",
                           (256, 256), 0, 0)
        self.M2MPCBorder1 = collision(700, 740, 320, 360)
        self.fight24 = False
        self.M2NPC2 = NPCs((250, 610),
                           "https://orig00.deviantart.net/6676/f/2011/137/5/f/kymotonian_norman_complete__by_rafael_animal-d3gk3tf.png",
                           (256, 256), 0, 3)
        self.M2MPCBorder2 = collision(230, 270, 580, 625)
        self.fight22 = False
        self.M2NPC3 = NPCs((340, 160),
                           "https://orig00.deviantart.net/1ce4/f/2011/137/1/b/kyle_hoenn_swimmer_2_complete_by_rafael_animal-d3gk589.png",
                           (254, 254), 0, 3)
        self.M2MPCBorder3 = collision(300, 330, 139, 160)
        self.fight23 = False

        self.M3NPC1 = NPCs((750, 520),
                           "https://orig00.deviantart.net/30aa/f/2011/137/f/a/kymotonian_shop__s_boy_complete_by_rafael_animal-d3gk754.png",
                           (256, 256), 0, 3)
        self.M3MPCBorder1 = collision(720, 775, 475, 535)
        self.M3NPC2 = NPCs((455, 50),
                           "https://orig00.deviantart.net/7bcb/f/2012/304/5/9/young_boy_ow___bw_style_by_putillabarata-d5jjgkf.png",
                           (256, 256), 0, 0)
        self.M3MPCBorder2 = collision(425, 475, 0, 80)
        self.M3NPC3 = NPCs((250, 310),
                           "https://orig00.deviantart.net/ef9e/f/2011/137/4/9/pkmn_rse___normal_boy_1_by_rafael_animal-d3gk6mu.png",
                           (256, 256), 0, 0)
        self.M3MPCBorder3 = collision(230, 275, 300, 335)

        self.M4NPC2 = NPCs((725, 515),
                           "https://orig00.deviantart.net/a784/f/2011/137/4/2/kymotonian_magma_grunt_compl__by_rafael_animal-d3gk4k9.png",
                           (256, 256), 0, 3)
        self.M4MPCBorder2 = collision(700, 740, 485, 535)
        self.fight42 = False

        self.M5NPC2 = NPCs((225, 450),
                           "https://orig00.deviantart.net/a784/f/2011/137/4/2/kymotonian_magma_grunt_compl__by_rafael_animal-d3gk4k9.png",
                           (256, 256), 0, 2)
        self.M5PCBorder2 = collision(210, 250, 410, 460)
        self.fight52 = False
        self.M5NC3 = NPCs((845, 120),
                          "https://orig00.deviantart.net/ee71/f/2012/105/9/c/bw2_girl_overworld__rpgxp__by_rafael_animal-d4w9gsm.png",
                          (256, 256), 0, 1)
        self.M5MCBorder3 = collision(810, 920, 0, 145)
        self.fight53 = False

        self.MiNPC2 = NPCs((415, 320),
                           "https://orig00.deviantart.net/ee71/f/2012/105/9/c/bw2_girl_overworld__rpgxp__by_rafael_animal-d4w9gsm.png",
                           (256, 256), 0, 0)
        self.MiPCBorder2 = collision(380, 425, 300, 350)

    # Draws items relating to the map on the canvas
    def draw(self, canvas):

        if (map == 0):
            canvas.draw_image(
                simplegui.load_image("https://image.ibb.co/jdF3sc/Capture_d_cran_2018_02_28_12_35_14.png"),
                self.ImageCenter, self.ImageWidthHeight, self.CenterDest, self.DimDest)
            self.M0Ball1.draw(canvas)
            self.M0Ball2.draw(canvas)
            self.M0Ball3.draw(canvas)
            self.M0Nurse1.draw(canvas)
            if (self.fight is False):
                self.M0Trainer.draw(canvas)
            if (self.M0LevelUp1 is False):
                self.M0LevelUp.draw(canvas)
            self.M0NPC1.draw(canvas)

        if (map == 1):
            self.url = simplegui.load_image("https://image.ibb.co/kLwidS/Capture_d_e_cran_2018_03_02_a_22_19_59.png")
            self.ImageWidthHeight = (919, 700)
            canvas.draw_image(self.url, self.ImageCenter, self.ImageWidthHeight, self.CenterDest, self.DimDest)
            self.M1Nurse1.draw(canvas)
            if (self.fight1 is False):
                self.M1Trainer.draw(canvas)
            if (self.fight11 is False):
                self.M1NPC1.draw(canvas)
            if (self.fight12 is False):
                self.M1NPC2.draw(canvas)
            if (self.fight13 is False):
                self.M1NPC3.draw(canvas)
            if (self.M1LevelUp1 is False):
                self.M1LevelUp.draw(canvas)

        if (map == 2):
            self.url = simplegui.load_image("https://image.ibb.co/gUcoiS/Capture_d_cran_2018_03_06_14_41_51.png")
            self.ImageWidthHeight = (919, 700)
            canvas.draw_image(self.url, self.ImageCenter, self.ImageWidthHeight, self.CenterDest, self.DimDest)
            self.M2Nurse1.draw(canvas)
            if (self.fight2 is False):
                self.M2Trainer.draw(canvas)
            if (self.fight21 is False):
                self.M21Trainer.draw(canvas)

            if (self.fight24 is False):
                self.M2NPC1.draw(canvas)
            if (self.fight22 is False):
                self.M2NPC2.draw(canvas)
            if (self.fight23 is False):
                self.M2NPC3.draw(canvas)
            if (self.M2LevelUp1 is False):
                self.M2LevelUp.draw(canvas)

        if (map == 3):
            self.url = simplegui.load_image("https://image.ibb.co/gx5o2n/Pokemon_Ville.png")
            self.ImageWidthHeight = (819, 628)
            canvas.draw_image(simplegui.load_image("https://image.ibb.co/gx5o2n/Pokemon_Ville.png"), (819 / 2, 628 / 2),
                              (819, 628), self.CenterDest, self.DimDest)
            if (self.fight3 is False):
                self.M3Trainer.draw(canvas)
            if (self.fight31 is False):
                self.M31Trainer.draw(canvas)
            self.M3NPC1.draw(canvas)
            self.M3NPC2.draw(canvas)
            self.M3NPC3.draw(canvas)
            # if (self.M3LevelUp1 is False):
            #   self.M3LevelUp.draw(canvas)

        if (map == -1):
            self.url = simplegui.load_image("https://image.ibb.co/dLoYJS/sd.png")
            self.ImageWidthHeight = (819, 628)
            canvas.draw_image(simplegui.load_image("https://image.ibb.co/dLoYJS/sd.png"), (815 / 2, 625 / 2),
                              (815, 625), self.CenterDest, self.DimDest)
            self.MiNurse1.draw(canvas)
            self.MiNPC2.draw(canvas)

        if (map == 4):
            self.url = simplegui.load_image("https://image.ibb.co/fZGm7n/Snow.png")
            self.ImageWidthHeight = (1020, 780)
            canvas.draw_image(simplegui.load_image("https://image.ibb.co/fZGm7n/Snow.png"), (1020 / 2, 780 / 2),
                              (1020, 780), self.CenterDest, self.DimDest)
            if (self.fight4 is False):
                self.M4Trainer.draw(canvas)
            if (self.fight41 is False):
                self.M41Trainer.draw(canvas)
            if (self.fight42 is False):
                self.M4NPC2.draw(canvas)
            if (self.M4LevelUp1 is False):
                self.M4LevelUp.draw(canvas)
            self.M4Nurse1.draw(canvas)

        if (map == 5):
            self.url = simplegui.load_image("https://image.ibb.co/cZicDS/Cave.png")
            self.ImageWidthHeight = (1020, 775)
            canvas.draw_image(simplegui.load_image("https://image.ibb.co/cZicDS/Cave.png"), (1020 / 2, 775 / 2),
                              (1020, 775), self.CenterDest, self.DimDest)
            if (self.fight5 is False):
                self.M5Trainer.draw(canvas)
            if (self.fight51 is False):
                self.M51Trainer.draw(canvas)
            if (self.fight52 is False):
                self.M5NPC2.draw(canvas)
            if (self.fight53 is False):
                self.M5NC3.draw(canvas)
            if (self.M5LevelUp1 is False):
                self.M5LevelUp.draw(canvas)
            self.M5Nurse1.draw(canvas)

        if (map == 6):
            self.url = simplegui.load_image("https://image.ibb.co/iESqHn/Hell.png")
            canvas.draw_image(simplegui.load_image("https://image.ibb.co/iESqHn/Hell.png"), (1020 / 2, 775 / 2),
                              (1020, 775), self.CenterDest, self.DimDest)
            if (self.fight6 is False):
                self.M6Trainer.draw(canvas)
            if (self.M6LevelUp1 is False):
                self.M6LevelUp.draw(canvas)

    # Updates the map whenever the method is called
    def update(self, canvas):
        global map
        global BATTLE_ON
        global score
        if (map == 0):

            if (self.M0LevelUp1 is False):
                if (self.M0LevelUpHB.isInside()):
                    self.a.level_up()
                    score = score - 2
                    self.M0LevelUp1 = True

            self.M0tree1.isInside()
            self.M0tree2.isInside()
            self.M0tree3.isInside()
            self.M0tree4.isInside()

            self.M0border1.isInside()
            self.M0border2.isInside()
            self.M0border3.isInside()
            self.M0border4.isInside()
            self.M0border5.isInside()

            if (self.M0BallBorder1.isInside()):
                Pokemon.draw1(canvas)
                if Pokemon.frameIndex1 == (2, 0):
                    self.a = self.playerMon[0]
                elif Pokemon.frameIndex1 == (5, 0):
                    self.a = self.playerMon[1]
                elif Pokemon.frameIndex1 == (8, 0):
                    self.a = self.playerMon[2]
                elif Pokemon.frameIndex1 == (3, 6):
                    self.a = self.playerMon[3]
                elif Pokemon.frameIndex1 == (6, 6):
                    self.a = self.playerMon[4]
                elif Pokemon.frameIndex1 == (9, 6):
                    self.a = self.playerMon[5]
                elif Pokemon.frameIndex1 == (3, 10):
                    self.a = self.playerMon[6]
                elif Pokemon.frameIndex1 == (6, 10):
                    self.a = self.playerMon[7]
                elif Pokemon.frameIndex1 == (9, 10):
                    self.a = self.playerMon[8]
                    # print(Pokemon.frameIndex2)

            if (self.M0BallBorder2.isInside()):
                Pokemon.draw2(canvas)
                if Pokemon.frameIndex2 == (2, 0):
                    self.a = self.playerMon[0]
                elif Pokemon.frameIndex2 == (5, 0):
                    self.a = self.playerMon[1]
                elif Pokemon.frameIndex2 == (8, 0):
                    self.a = self.playerMon[2]
                elif Pokemon.frameIndex2 == (3, 6):
                    self.a = self.playerMon[3]
                elif Pokemon.frameIndex2 == (6, 6):
                    self.a = self.playerMon[4]
                elif Pokemon.frameIndex2 == (9, 6):
                    self.a = self.playerMon[5]
                elif Pokemon.frameIndex2 == (3, 10):
                    self.a = self.playerMon[6]
                elif Pokemon.frameIndex2 == (6, 10):
                    self.a = self.playerMon[7]
                elif Pokemon.frameIndex2 == (9, 10):
                    self.a = self.playerMon[8]
            # print(Pokemon.frameIndex2)

            if (self.M0BallBorder3.isInside()):
                Pokemon.draw3(canvas)
                if Pokemon.frameIndex3 == (2, 0):
                    self.a = self.playerMon[0]
                elif Pokemon.frameIndex3 == (5, 0):
                    self.a = self.playerMon[1]
                elif Pokemon.frameIndex3 == (8, 0):
                    self.a = self.playerMon[2]
                elif Pokemon.frameIndex3 == (3, 6):
                    self.a = self.playerMon[3]
                elif Pokemon.frameIndex3 == (6, 6):
                    self.a = self.playerMon[4]
                elif Pokemon.frameIndex3 == (9, 6):
                    self.a = self.playerMon[5]
                elif Pokemon.frameIndex3 == (3, 10):
                    self.a = self.playerMon[6]
                elif Pokemon.frameIndex3 == (6, 10):
                    self.a = self.playerMon[7]
                elif Pokemon.frameIndex3 == (9, 10):
                    self.a = self.playerMon[8]
                    # print(Pokemon.frameIndex3)

            if (self.M0NurseBorder.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/ikAvYS/undertale_box_1.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))
                self.a.health_reset()

            if (self.M0MPCBorder1.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/dPzkk7/undertale_box_3.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))

            if (self.fight is False):
                if (self.M0TrainerBorder.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyTrainer1)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight = True
                        score = score + 10
                        # print (score)
                        transition.PokeBall.spin = True

            if (self.M0nextMap.isInside()):
                self.begin = True
                map = 1

        if (map == 1):

            if (self.M1LevelUp1 is False):
                if (self.M1LevelUpHB.isInside()):
                    self.a.level_up()
                    score = score - 2
                    # print (self.a.attackStat)
                    self.M1LevelUp1 = True

            if (self.begin is True):
                Player.pos.x = 675
                Player.pos.y = 670

                self.begin = False

            self.M1border1.isInside()
            self.M1border2.isInside()
            self.M1border3.isInside()
            self.M1border4.isInside()
            self.M1border5.isInside()
            self.M1border6.isInside()
            self.M1border7.isInside()
            self.M1border8.isInside()
            self.M1border9.isInside()

            self.M1tree1.isInside()
            self.M1tree2.isInside()
            self.M1tree3.isInside()
            self.M1tree4.isInside()
            self.M1tree5.isInside()

            self.M1previousMap.isInside()

            if (self.fight1 is False):  # Map1 Boss
                if (self.M1TrainerBorder.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyBoss1)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight1 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.fight11 is False):  # Map1 Npc
                if (self.M1MPCBorder1.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyTrainer2)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight11 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.fight12 is False):  # Map1 Npc
                if (self.M1MPCBorder2.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyTrainer2)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight12 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.fight13 is False):  # Map1 Npc
                if (self.M1MPCBorder3.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyTrainer2)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight13 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.M1NurseBorder.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/ikAvYS/undertale_box_1.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))
                self.a.health_reset()

            if (self.M1nextMap.isInside()):
                self.begin = True
                map = 2

        if (map == 2):

            if (self.M2LevelUp1 is False):
                if (self.M2LevelUpHB.isInside()):
                    self.a.level_up()
                    score = score - 2
                    # print (self.a.attackStat)
                    self.M2LevelUp1 = True

            if (self.begin is True):
                Player.pos.x = 900
                Player.pos.y = 500

                self.begin = False

            self.M2border1.isInside()
            self.M2border2.isInside()
            self.M2border3.isInside()
            self.M2border4.isInside()
            self.M2border5.isInside()
            self.M2border6.isInside()
            self.M2border7.isInside()
            self.M2border8.isInside()

            self.M2tree1.isInside()
            self.M2tree2.isInside()
            self.M2tree3.isInside()
            self.M2tree4.isInside()

            self.M2river1.isInside()
            self.M2river2.isInside()
            self.M2river3.isInside()
            self.M2river4.isInside()
            self.M2river5.isInside()
            self.M2river6.isInside()
            self.M2river7.isInside()
            self.M2river8.isInside()
            self.M2river9.isInside()
            self.M2river10.isInside()
            self.M2river11.isInside()
            self.M2river12.isInside()
            self.M2river13.isInside()
            self.M2river14.isInside()

            self.M2previousMap.isInside()

            if (self.fight2 is False):  # Map2 Boss
                if (self.M2TrainerBorder.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyBoss2)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight2 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.fight21 is False):  # Map2 Npc
                if (self.M21TrainerBorder.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyTrainer3)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight21 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.fight24 is False):  # Map2 Npc
                if (self.M2MPCBorder1.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyTrainer3)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight24 = True
                        score = score + 10
                        transition.PokeBall.spin = True
            if (self.fight23 is False):
                if (self.M2MPCBorder3.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyTrainer3)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight23 = True
                        score = score + 10
                        transition.PokeBall.spin = True
            if (self.fight22 is False):  # Map2 Npc
                if (self.M2MPCBorder2.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyTrainer3)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight22 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.M2NurseBorder.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/ikAvYS/undertale_box_1.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))
                self.a.health_reset()

            if (self.M2nextMap.isInside()):
                self.begin = True
                map = 3

        if (map == 3):

            if (self.begin2 is True):
                Player.pos.x = 355
                Player.pos.y = 340

                self.begin2 = False

            if (self.begin is True):
                Player.pos.x = 880
                Player.pos.y = 395

                self.begin = False

            self.M3border1.isInside()
            self.M3border2.isInside()
            self.M3border3.isInside()
            self.M3border4.isInside()
            self.M3border5.isInside()
            self.M3border6.isInside()

            self.M3house1.isInside()
            self.M3house2.isInside()

            self.M3tree1.isInside()
            self.M3tree2.isInside()
            self.M3tree3.isInside()
            self.M3tree4.isInside()
            self.M3tree5.isInside()
            self.M3tree6.isInside()

            self.M3previousMap.isInside()

            if (self.fight3 is False):  # Map3 Npc
                if (self.M3TrainerBorder.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyBoss3)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight3 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.fight31 is False):
                if (self.M31TrainerBorder.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyTrainer4)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight31 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.M3door1.isInside()):
                self.begin = True
                map = -1

            if (self.M3door2.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/iB5usn/undertale_box_1.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))

            if (self.M3nextMap.isInside()):
                self.begin = True
                map = 4

            if (self.M3MPCBorder1.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/fObc2n/undertale_box_7.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))
                if (self.M3LevelUp1 is False):
                    self.a.level_up()
                    score = score - 2
                    # print (self.a.attackStat)
                    self.M3LevelUp1 = True

            if (self.M3MPCBorder2.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/fUgMTS/undertale_box_6.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))
            if (self.M3MPCBorder3.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/b01S2n/undertale_box_5.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))

        if (map == -1):
            if (self.begin is True):
                Player.pos.x = 675
                Player.pos.y = 412

                self.begin = False

            if (self.MipreviousMap.isInside()):
                self.begin2 = True
                map = 3

            self.Miborder1.isInside()
            self.Miborder2.isInside()
            self.Miborder3.isInside()
            self.Miborder4.isInside()

            self.Mifurniture1.isInside()
            self.Mifurniture2.isInside()
            self.Mifurniture3.isInside()
            self.Mifurniture4.isInside()
            self.Mifurniture5.isInside()

            if (self.MiNurseBorder.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/ikAvYS/undertale_box_1.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))
                self.a.health_reset()

            if (self.MiPCBorder2.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/hs9BdS/undertale_box_4.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))

        if (map == 4):

            if (self.M4LevelUp1 is False):
                if (self.M4LevelUpHB.isInside()):
                    self.a.level_up()
                    score = score - 2
                    self.M4LevelUp1 = True

            if (self.begin is True):
                Player.pos.x = 890
                Player.pos.y = 340

                self.begin = False

            self.M4border1.isInside()
            self.M4border2.isInside()
            self.M4border3.isInside()
            self.M4border4.isInside()
            self.M4border5.isInside()
            self.M4border6.isInside()
            self.M4border7.isInside()
            self.M4border8.isInside()
            self.M4border9.isInside()
            self.M4border10.isInside()

            if (self.fight4 is False):  # Map4 Npc
                if (self.M4TrainerBorder.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyTrainer5)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight4 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.fight41 is False):  # Map4 Boss
                if (self.M41TrainerBorder.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyBoss4)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight41 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.fight42 is False):  # Map4 Npc
                if (self.M4MPCBorder2.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyTrainer5)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight42 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.M4nextMap.isInside()):
                self.begin = True
                map = 5

            self.M4previousMap.isInside()

            if (self.M4NurseBorder.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/ikAvYS/undertale_box_1.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))
                self.a.health_reset()

        if (map == 5):

            if (self.M5LevelUp1 is False):
                if (self.M5LevelUpHB.isInside()):
                    self.a.level_up()
                    score = score - 2
                    self.M5LevelUp1 = True

            if (self.begin is True):
                Player.pos.x = 245
                Player.pos.y = 625

                self.begin = False

            self.M5border1.isInside()
            self.M5border2.isInside()
            self.M5border3.isInside()
            self.M5border4.isInside()
            self.M5border5.isInside()
            self.M5border6.isInside()
            self.M5border7.isInside()
            self.M5border8.isInside()
            self.M5border10.isInside()
            self.M5border11.isInside()
            self.M5border12.isInside()
            self.M5border13.isInside()

            if (self.fight5 is False):  # Map5 Boss
                if (self.M5TrainerBorder.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyBoss4)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight41 = True
                        self.fight5 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.fight51 is False):  # Map5 Npc
                if (self.M51TrainerBorder.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyBoss4)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight41 = True
                        self.fight51 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.M5nextMap.isInside()):
                self.begin = True
                map = 6

            self.M5previousMap.isInside()

            if (self.M5NurseBorder.isInside()):
                canvas.draw_image(simplegui.load_image('https://image.ibb.co/ikAvYS/undertale_box_1.png'),
                                  (578 / 2, 152 / 2), (578, 152), (920 / 2, 700 - 150), (578, 152))
                self.a.health_reset()

            if (self.fight53 is False):  # Map5 Npc
                if (self.M5MCBorder3.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyBoss4)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight41 = True
                        self.fight53 = True
                        score = score + 10
                        transition.PokeBall.spin = True

            if (self.fight52 is False):  # Map5 Npc
                if (self.M5PCBorder2.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyBoss4)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight41 = True
                        self.fight52 = True
                        score = score + 10
                        transition.PokeBall.spin = True

        if (map == 6):

            if (self.M6LevelUp1 is False):
                if (self.M6LevelUpHB.isInside()):
                    self.a.level_up()
                    score = score - 2
                    self.M6LevelUp1 = True

            if (self.begin is True):
                Player.pos.x = 400
                Player.pos.y = 625

                self.begin = False

            self.M6border1.isInside()
            self.M6border2.isInside()
            self.M6border3.isInside()
            self.M6border4.isInside()
            self.M6border5.isInside()
            self.M6border6.isInside()
            self.M6border7.isInside()

            if (self.fight6 is False):  # RED
                if (self.M6TrainerBorder.isInside()):
                    transition.update(canvas)
                    if not transition.PokeBall.spin:
                        self.b = random.choice(self.enemyRed)
                        self.a.enemy = self.b
                        self.b.player = self.a
                        self.a.attack_reset()
                        self.a.defence_reset()
                        self.b.attack_reset()
                        self.b.defence_reset()
                        self.b.health_reset()
                        BATTLE_ON = True
                        self.fight6 = True
                        score = score + 50
                        # print(score)
                        transition.PokeBall.spin = True
            else:
                menu.playGame = False
                menu.message = "You Win!"
                menu.messageTwo = "Score: " + str(score)
                menu.messageThree = ""
                menu.messageFour = ""
                self.a.reset_level()
                Map.reset()

    # Resets the map to play again
    def reset(self):
        global score
        global map
        self.fight = False
        self.fight1 = False
        self.fight11 = False
        self.fight12 = False
        self.fight13 = False
        self.fight2 = False
        self.fight21 = False
        self.fight22 = False
        self.fight23 = False
        self.fight24 = False
        self.fight3 = False
        self.fight31 = False
        self.fight4 = False
        self.fight41 = False
        self.fight42 = False
        self.fight5 = False
        self.fight51 = False
        self.fight52 = False
        self.fight53 = False
        self.fight6 = False
        self.M0LevelUp1 = False
        self.M1LevelUp1 = False
        self.M2LevelUp1 = False
        self.M3LevelUp1 = False
        self.M4LevelUp1 = False
        self.M5LevelUp1 = False
        self.M6LevelUp1 = False
        self.begin = False
        score = 0
        map = 0
        Player.pos.x = 300
        Player.pos.y = 340


# Creates the transition between the battles(s) and the map(s)
class PokeBall:
    # Initialises the spinning Pokeball
    def __init__(self, pos):
        self.pos = pos
        self.radius = 100
        self.spin = True
        self.image = simplegui.load_image('https://imgur.com/GF3Dg8s.png')

    # Draws the Pokeball on the canvas
    def draw(self, canvas):
        global IMG_ROT
        IMG_ROT += 0.05
        IMG_DIAMETER = self.radius * 2
        IMG_DIM = 1280
        IMG_WH = (IMG_DIM, IMG_DIM)
        CEN_DEST = self.pos.getP()
        DIM_DEST = (IMG_DIAMETER, IMG_DIAMETER)
        canvas.draw_image(self.image, (IMG_DIM / 2, IMG_DIM / 2), (IMG_WH), (CEN_DEST), (DIM_DEST), IMG_ROT)

    # Updates the Pokeballs radius
    def update(self):
        self.radius += 5

    # Resets the Pokeball
    def reset(self):
        self.radius = 100
        IMG_ROT = 0
        self.spin = False


# The fireball(s) that collide when the frame is started
class FireBall:
    # Initialises the fireball with the specified sprite
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.radius = 60
        self.image = simplegui.load_image('https://imgur.com/TZyNYNu.png')
        self.dimension = 512
        self.imageSize = (self.dimension, self.dimension)
        self.columns = 8
        self.rows = 8

        self.frameWidth = self.imageSize[0] / self.columns
        self.frameHeight = self.imageSize[1] / self.rows
        self.frameCentreX = self.frameWidth / 2
        self.frameCentreY = self.frameHeight / 2
        self.frameIndex = [0, 0]
        self.frameDimension = (self.frameWidth, self.frameHeight)
        self.DimDest = (128, 128)

    # The fireball from the left to the centre
    def LeftToRight(self):
        self.frameIndex[0] = (self.frameIndex[0] + 1) % self.columns
        self.frameIndex[1] = 4

    # The fireball from the right to the centre
    def RightToLeft(self):
        self.frameIndex[0] = (self.frameIndex[0] + 1) % self.columns
        self.frameIndex[1] = 0

    # Draws the fireball on canvas
    def draw(self, canvas):
        self.imageCentre = (self.frameWidth * self.frameIndex[0] + self.frameCentreX,
                            self.frameHeight * self.frameIndex[1] + self.frameCentreY)
        canvas.draw_image(self.image, self.imageCentre, self.frameDimension, self.pos.getP(), self.DimDest)

    # Bounces the fireballs off of the centre point
    def bounce(self, normal):
        self.vel.reflect(normal)

    # Updates the velocity of the fireballs
    def update(self):
        self.pos.add(self.vel)


# The fire blast that ensues the colliding fireballs
class FireBlast:
    # Initialises the fire blast with the provided sprite
    def __init__(self, pos):
        self.pos = pos
        self.radius = 32
        self.image = simplegui.load_image('http://moziru.com/images/drawn-explosion-sprite-1.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.imageSize = (self.width, self.height)
        self.columns = 8
        self.rows = 6

        self.frameWidth = self.imageSize[0] / self.columns
        self.frameHeight = self.imageSize[1] / self.rows
        self.frameCentreX = self.frameWidth / 2
        self.frameCentreY = self.frameHeight / 2
        self.frameIndex = [0, 0]
        self.frameDimension = (self.frameWidth, self.frameHeight)
        self.DimDest = (2688, 2688)

    # Draws the fire blast on canvas
    def draw(self, canvas):
        self.frameIndex[0] = (self.frameIndex[0] + 1) % self.columns
        if self.frameIndex[0] == 0:
            self.frameIndex[1] = (self.frameIndex[1] + 1) % self.rows
        self.imageCentre = (self.frameWidth * self.frameIndex[0] + self.frameCentreX,
                            self.frameHeight * self.frameIndex[1] + self.frameCentreY)
        canvas.draw_image(self.image, self.imageCentre, self.frameDimension, self.pos.getP(), self.DimDest)

    # Determines whether the fire blast is complete or not
    def complete(self):
        complete = self.frameIndex[0] == 7 and self.frameIndex[1] == 5
        return complete


# Rotates a vector but should be in a class
def rotateAnti(v):
    return Vector(-v.y, v.x)


# Creates a line for the fireballs to bounce off of
class Line:
    # Initialises the line
    def __init__(self, point1, point2):
        self.pA = point1
        self.pB = point2
        self.thickness = 3
        self.unit = (self.pB - self.pA).normalize()
        self.normal = rotateAnti(self.unit)

    # Determines the distance to the line from somethings position
    def distanceTo(self, pos):
        posToA = pos - self.pA
        proj = posToA.dot(self.normal) * self.normal
        return proj.length()

    # Determines if something covers the line from its current position
    def covers(self, pos):
        return ((pos - self.pA).dot(self.unit) >= 0 and
                (pos - self.pB).dot(-self.unit) >= 0)


# Animates the fireball explosion upon starting the frame
class Opening:
    # Initialises the fireballs, line, and explosion
    def __init__(self):
        self.FireBallLeft = FireBall(Vector(50, 350), Vector(5, 0))
        self.FireBallRight = FireBall(Vector(870, 350), Vector(-5, 0))
        self.line = Line(Vector(460, 300), Vector(460, 400))
        self.inCollision = False

    # Updates the canvas to include the fireballs
    # Should be renamed as draw; however, doesn't matter
    def update(self, canvas):
        if self.inCollision == False:
            # FireBalls Left => Right
            self.FireBallLeft.draw(canvas)
            self.FireBallLeft.LeftToRight()
            self.FireBallLeft.update()
            # FireBalls Right => Left
            self.FireBallRight.draw(canvas)
            self.FireBallRight.RightToLeft()
            self.FireBallRight.update()

        else:
            if not fb.complete():
                fb.draw(canvas)

        if (self.line.distanceTo(self.FireBallRight.pos) < self.line.thickness + self.FireBallRight.radius and
                self.line.covers(self.FireBallRight.pos)):
            if not self.inCollision:
                self.inCollision = True
        else:
            self.inCollision = False


# Creates the transition between the battle(s) and the map(s)
class Transition:
    # Initialises the Pokeball
    def __init__(self):
        self.PokeBall = PokeBall(Vector(460, 350))
        self.timer = simplegui.create_timer(2100, self.timer_handler)

    # Updates the canvas
    def update(self, canvas):
        if self.PokeBall.spin:
            self.PokeBall.draw(canvas)
            self.PokeBall.update()
            # inter.wheel.vel.negate()
            kbd.right = False
            kbd.left = False
            kbd.up = False
            kbd.down = False
            kbd.run = False
            self.timer.start()

    # The timer handler to determine how long the Pokeball spins for
    def timer_handler(self):
        self.PokeBall.spin = False
        self.PokeBall.reset()
        self.timer.stop()


# Manages the interaction between the player and the keyboard/mouse
class Interaction:
    # Initialises the player and keyboard
    def __init__(self, wheel, keyboard):
        self.wheel = wheel
        self.keyboard = keyboard

    # Updates the velocity of the player depending on which key is pressed
    def update(self):
        if self.keyboard.right:
            Player.nextFrameRight()
            self.wheel.vel.add(Vector(0.25, 0))
        if self.keyboard.left:
            Player.nextFrameLeft()
            self.wheel.vel.add(Vector(-0.25, 0))
        if self.keyboard.up:
            Player.nextFrameUp()
            self.wheel.vel.add(Vector(0, -0.25))
        if self.keyboard.down:
            Player.nextFrameDown()
            self.wheel.vel.add(Vector(0, 0.25))
        if self.keyboard.run:
            self.wheel.vel.multiply(1.09)

    # Draws the menu, battle(s), maps, opening transitions, etc
    def draw(self, canvas):
        opening.update(canvas)
        if fb.complete():
            if not menu.playGame:
                menu.draw(canvas)
                menuButtons.draw(canvas)

            elif BATTLE_ON:
                battle.draw(canvas)

            else:
                inter.update()
                Map.draw(canvas)
                Player.update()
                Player.draw(canvas)
                Map.update(canvas)


# Used to manage the delay at the end of a battle
class Clock1:
    # Sets time to 0
    def __init__(self):
        self.time = 0

    # Increments the time
    def tick(self):
        self.time = self.time + 1 / 60

    # Determines when the transition occurs
    def transition(self, frameDuration):
        self.tick()
        # print(self.time % frameDuration)
        rem = self.time % frameDuration
        return 0 < rem < 0.017  # 0.017 = tick in 60fps so keep it like this or it's broken af


# The collision between the player and an object (NPC/Pokeball/Mushroom) on the map
class collision:
    # Initialiser
    def __init__(self, BoxLeft, BoxRight, BoxTop, BoxBottom):
        self.BoxLeft = BoxLeft
        self.BoxRight = BoxRight
        self.BoxTop = BoxTop
        self.BoxBottom = BoxBottom

    # Determines if the player is within a certain proximity of an object
    def isInside(self):
        if self.BoxLeft <= Player.pos.x <= self.BoxRight and self.BoxTop <= Player.pos.y <= self.BoxBottom:
            if Player.pos.x < (self.BoxLeft + 10):
                Player.pos.x = self.BoxLeft
                return True
            if Player.pos.x > (self.BoxRight - 10):
                Player.pos.x = self.BoxRight
                return True
            if Player.pos.y < (self.BoxTop + 10):
                Player.pos.y = self.BoxTop
                return True
            if Player.pos.y > (self.BoxBottom - 10):
                Player.pos.y = self.BoxBottom
                return True


# The pokeballs for choosing pokemon at the start
class Pokeballs:
    # Takes arguments for the place where the Pokeballs should be
    def __init__(self, url, ImageWidthHeight, CenterDest):
        self.url = simplegui.load_image(url)
        self.ImageWidthHeight = ImageWidthHeight
        self.ImageCenter = (ImageWidthHeight[0] / 2, ImageWidthHeight[1] / 2)
        self.CenterDest = CenterDest
        self.DimDest = (25, 25)

    # Draws the pokeballs on the map with the specified positions
    def draw(self, canvas):
        canvas.draw_image(self.url, self.ImageCenter, self.ImageWidthHeight, self.CenterDest, self.DimDest)


# Creates the sprite for Nurse Joy with a specified URL
class NurseJoy:
    # Takes arguments to intialise where Nurse Joy should go and how large the NPC should be
    def __init__(self, url, ImageWidthHeight, CenterDest):
        self.url = simplegui.load_image(url)
        self.ImageWidthHeight = ImageWidthHeight
        self.ImageCenter = (ImageWidthHeight[0] / 2, ImageWidthHeight[1] / 2)
        self.CenterDest = CenterDest
        self.DimDest = (60, 60)

    # Draws Nurse Joy on the map at the specified place
    def draw(self, canvas):
        canvas.draw_image(self.url, self.ImageCenter, self.ImageWidthHeight, self.CenterDest, self.DimDest)


# Creates the players character
class Character:
    # Initialises the characters sprite
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector()

        self.url = simplegui.load_image("https://i.imgur.com/sCrkzvs.png")

        self.ImageSize = (256, 256)
        self.ImageCenter = (256 / 2, 256 / 2)
        self.colums = 4
        self.rows = 4

        self.frameWidth = self.ImageSize[0] / self.colums
        self.frameHeight = self.ImageSize[1] / self.rows
        self.frameCentreX = self.frameWidth / 2
        self.frameCentreY = self.frameHeight / 2
        self.ImageCenter = (self.frameCentreX, self.frameCentreY)
        self.frameIndex = [0, 0]
        self.ImageWidthHeight = (self.frameWidth, self.frameHeight)

        self.DimDest = (60, 60)

    # Updates the characters velocity
    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.85)

    # Determines the next frame down
    def nextFrameDown(self):
        if c.transition(
                0.2):  # For some reason, probably timer related any other values break the animation. : ¯\_(ツ)_/¯:
            self.frameIndex[0] = (self.frameIndex[0] + 1) % self.colums
            self.frameIndex[1] = 0

    # Determines the next frame up
    def nextFrameUp(self):
        if c.transition(
                0.2):  # For some reason, probably timer related any other values break the animation. : ¯\_(ツ)_/¯:
            self.frameIndex[0] = (self.frameIndex[0] + 1) % self.colums
            self.frameIndex[1] = 3

    # Determines the next frame left
    def nextFrameLeft(self):
        if c.transition(
                0.2):  # For some reason, probably timer related any other values break the animation. : ¯\_(ツ)_/¯:
            self.frameIndex[0] = (self.frameIndex[0] + 1) % self.colums
            self.frameIndex[1] = 1

    # Determines the next frame right
    def nextFrameRight(self):
        if c.transition(
                0.2):  # For some reason, probably timer related any other values break the animation. : ¯\_(ツ)_/¯:
            self.frameIndex[0] = (self.frameIndex[0] + 1) % self.colums
            self.frameIndex[1] = 2

    # Draws the character on the canvas
    def draw(self, canvas):
        self.ImageCenter = (self.frameWidth * self.frameIndex[0] + self.frameCentreX,
                            self.frameHeight * self.frameIndex[1] + self.frameCentreY)
        canvas.draw_image(self.url, self.ImageCenter, self.ImageWidthHeight, self.pos.getP(), self.DimDest)


# Allows the pokemon to choose from a random Pokemon
class RandomPokemon:
    # Initialises the random Pokemon from a sprite
    def __init__(self, Pokemon1, Pokemon2, Pokemon3):
        self.Pokemon1 = Pokemon1
        self.Pokemon2 = Pokemon2
        self.Pokemon2 = Pokemon3
        self.url = simplegui.load_image("https://veekun.com/static/pokedex/downloads/generation-3.png")

        self.StarterPokemon = [(2, 0), (5, 0), (8, 0), (3, 6), (6, 6), (9, 6), (3, 10), (6, 10), (9, 10)]
        self.ImageSize = (1600, 1024)
        self.ImageCenter = (1600 / 2, 1024 / 2)
        self.colums = 25
        self.rows = 16

        self.frameWidth = self.ImageSize[0] / self.colums
        self.frameHeight = self.ImageSize[1] / self.rows
        self.frameCentreX = self.frameWidth / 2
        self.frameCentreY = self.frameHeight / 2
        self.ImageCenter = (self.frameCentreX, self.frameCentreY)
        self.frameIndex1 = self.StarterPokemon[Pokemon1]
        self.frameIndex2 = self.StarterPokemon[Pokemon2]
        self.frameIndex3 = self.StarterPokemon[Pokemon3]

        self.ImageWidthHeight = (self.frameWidth, self.frameHeight)

        self.DimDest = (150, 150)

    # Draws the first random Pokemon
    def draw1(self, canvas):
        self.ImageCenter = (self.frameWidth * self.frameIndex1[0] + self.frameCentreX,
                            self.frameHeight * self.frameIndex1[1] + self.frameCentreY)
        canvas.draw_circle((920 / 2, 700 / 2), 110, 1, "white", "white")
        canvas.draw_image(self.url, self.ImageCenter, self.ImageWidthHeight, (920 / 2, 700 / 2), self.DimDest)

    # Draws the second random Pokemon
    def draw2(self, canvas):
        self.ImageCenter = (self.frameWidth * self.frameIndex2[0] + self.frameCentreX,
                            self.frameHeight * self.frameIndex2[1] + self.frameCentreY)
        canvas.draw_circle((920 / 2, 700 / 2), 110, 1, "white", "white")
        canvas.draw_image(self.url, self.ImageCenter, self.ImageWidthHeight, (920 / 2, 700 / 2), self.DimDest)

    # Draws the third random Pokemon
    def draw3(self, canvas):
        self.ImageCenter = (self.frameWidth * self.frameIndex3[0] + self.frameCentreX,
                            self.frameHeight * self.frameIndex3[1] + self.frameCentreY)
        canvas.draw_circle((920 / 2, 700 / 2), 110, 1, "white", "white")
        canvas.draw_image(self.url, self.ImageCenter, self.ImageWidthHeight, (920 / 2, 700 / 2), self.DimDest)


# Adds trainers to the map
class Trainers:
    # Initialises the trainer with the specified dimensions
    def __init__(self, url, ImageWidthHeight, CenterDest):
        self.url = simplegui.load_image(url)
        self.ImageWidthHeight = ImageWidthHeight
        self.ImageCenter = (ImageWidthHeight[0] / 2, ImageWidthHeight[1] / 2)
        self.CenterDest = CenterDest
        self.DimDest = (60, 60)

    # Adds the trainer to the map at the specified position/place
    def draw(self, canvas):
        canvas.draw_image(self.url, self.ImageCenter, self.ImageWidthHeight, self.CenterDest, self.DimDest)


# Adds NPCs to the map
class NPCs:
    # Initialises the sprite for the NPCs
    def __init__(self, pos, url, ImageWidthHeight, frameIndexX, frameIndexY):
        self.pos = pos
        self.vel = Vector()

        self.url = simplegui.load_image(url)

        self.ImageSize = ImageWidthHeight
        self.ImageCenter = (ImageWidthHeight[0] / 2, ImageWidthHeight[0] / 2)
        self.colums = 4
        self.rows = 4

        self.frameWidth = self.ImageSize[0] / self.colums
        self.frameHeight = self.ImageSize[1] / self.rows
        self.frameCentreX = self.frameWidth / 2
        self.frameCentreY = self.frameHeight / 2
        self.ImageCenter = (self.frameCentreX, self.frameCentreY)
        self.frameIndex = [0, 0]
        self.ImageWidthHeight = (self.frameWidth, self.frameHeight)

        self.DimDest = (60, 60)

        self.frameIndex[0] = frameIndexX
        self.frameIndex[1] = frameIndexY

    # Draws the NPCs on the map
    def draw(self, canvas):
        self.ImageCenter = (self.frameWidth * self.frameIndex[0] + self.frameCentreX,
                            self.frameHeight * self.frameIndex[1] + self.frameCentreY)
        canvas.draw_image(self.url, self.ImageCenter, self.ImageWidthHeight, self.pos, self.DimDest)


# A class that creates the main menu of the game
class Menu:
    # Initialises the welcome messages, and sets playGame to false;
    def __init__(self):
        self.message = "Welcome to Not Pokemon!"
        self.messageTwo = "Click or press 'Play' to begin"
        self.messageThree = ""
        self.messageFour = ""
        self.playGame = False
        self.quitGame = False

        # Below for background image
        self.image = simplegui.load_image(
            'https://orig00.deviantart.net/486e/f/2011/305/c/5/spirit_master_background_by_kymotonian-d4elxyc.png')
        self.imageWidth = self.image.get_width()
        self.imageHeight = self.image.get_height()
        self.centreSource = (self.imageWidth / 2, self.imageHeight / 2)

    # Allows the game to begin - gets rid of the menu screen
    def play(self):
        self.playGame = True
        self.message = ""
        self.messageTwo = "Click or press 'Play' again to begin"
        self.messageThree = ""
        self.messageFour = ""

    # Allows the user to quit the game (frame)
    def quit(self):
        self.message = "You have quit the game!"
        self.messageTwo = ""
        self.messageThree = ""
        self.messageFour = ""
        self.playGame = False
        self.quitGame = True

    # Displays the info of the game
    def getInfo(self):
        self.message = "Made by: Diego Toledano, Juuso Helvio, "
        self.messageTwo = "Malik Rajwani, Liam Jones, "
        self.messageThree = "Patthawi Roddouyboon"
        self.messageFour = ""

    def getGuide(self):
        self.message = "Attack - Attacks the enemy (1 turn)"
        self.messageTwo = "Boost Attack - Boosts the players attack (1 turn)"
        self.messageThree = "Boost Defence - Boosts the players defence (1 turn)"
        self.messageFour = "Use the arrow keys to move and the space key to run"

    # Resets everything to default
    def default(self):
        self.message = "Welcome to Not Pokemon!"
        self.playGame = False
        self.quitGame = False

    # Draws the menu
    def draw(self, canvas):
        if not self.quitGame:
            if not PLAYER_ALIVE:
                if not self.playGame:
                    # The image throws two libpng warnings
                    text_widthOne = frame.get_canvas_textwidth(self.message, 30, 'monospace')
                    text_widthTwo = frame.get_canvas_textwidth(self.messageTwo, 30, 'monospace')
                    text_widthThree = frame.get_canvas_textwidth(self.messageThree, 30, 'monospace')
                    # The image throws two libpng warnings
                    canvas.draw_image(menu.image, menu.centreSource, (menu.imageWidth, menu.imageHeight),
                                      (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2), (CANVAS_WIDTH, CANVAS_HEIGHT))
                    canvas.draw_text(self.message, [CANVAS_WIDTH / 2 - text_widthOne / 2, CANVAS_HEIGHT / 1.5], 30,
                                     "White", "monospace")
                    canvas.draw_text(self.messageTwo, [CANVAS_WIDTH / 2 - text_widthTwo / 2, CANVAS_HEIGHT / 1.4], 30,
                                     "White", "monospace")
                    canvas.draw_text(self.messageThree, [CANVAS_WIDTH / 2 - text_widthThree / 2, CANVAS_HEIGHT / 1.3],
                                     30, "White", "monospace")
            else:
                text_widthOne = frame.get_canvas_textwidth(self.message, 30, 'monospace')
                text_widthTwo = frame.get_canvas_textwidth(self.messageTwo, 30, 'monospace')
                text_widthThree = frame.get_canvas_textwidth(self.messageThree, 30, 'monospace')
                text_widthFour = frame.get_canvas_textwidth(self.messageFour, 30, 'monospace')
                # The image throws two libpng warnings
                canvas.draw_image(menu.image, menu.centreSource, (menu.imageWidth, menu.imageHeight),
                                  (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2), (CANVAS_WIDTH, CANVAS_HEIGHT))
                canvas.draw_text(self.message, [CANVAS_WIDTH / 2 - text_widthOne / 2, CANVAS_HEIGHT / 1.5], 30, "White",
                                 "monospace")
                canvas.draw_text(self.messageTwo, [CANVAS_WIDTH / 2 - text_widthTwo / 2, CANVAS_HEIGHT / 1.4], 30,
                                 "White", "monospace")
                canvas.draw_text(self.messageThree, [CANVAS_WIDTH / 2 - text_widthThree / 2, CANVAS_HEIGHT / 1.3], 30,
                                 "White", "monospace")
                canvas.draw_text(self.messageFour, [CANVAS_WIDTH / 2 - text_widthFour / 2, CANVAS_HEIGHT / 1.6], 30,
                                 "White", "monospace")
        else:
            self.default()  # Not necessarily needed
            frame.stop()

    # Begins the game when the user clicks
    def mouse_handler(self, position):
        global BATTLE_ON
        self.playGame = True
        BATTLE_ON = False
        self.message = "Welcome to Not Pokemon!"
        self.messageTwo = "Click or press 'Play' again to begin"
        self.messageThree = ""
        self.messageFour = ""


# The class for the on-screen menu buttons
class MenuButtons:
    def __init__(self):
        self.play = "Play"
        self.info = "Info"
        self.quit = "Quit"
        self.guide = "Guide"

    # Draws the menu buttons with text
    def draw(self, canvas):
        canvas.draw_polygon([(135, 600), (135, 550), (335, 550), (335, 600)], 1, "White", "White")
        canvas.draw_polygon([(355, 600), (355, 550), (555, 550), (555, 600)], 1, "White", "White")
        canvas.draw_polygon([(575, 600), (575, 550), (775, 550), (775, 600)], 1, "White", "White")
        canvas.draw_polygon([(355, 670), (355, 620), (555, 620), (555, 670)], 1, "White", "White")
        canvas.draw_text(self.play, (195, 585), 30, "Black", "monospace")
        canvas.draw_text(self.info, (415, 585), 30, "Black", "monospace")
        canvas.draw_text(self.quit, (635, 585), 30, "Black", "monospace")
        canvas.draw_text(self.guide, (410, 655), 30, "Black", "monospace")

    # Handles the on-screen menu buttons
    def mouse_handler(self, position):
        if ((position[0] >= 135 and position[1] <= 600) and (position[0] <= 335 and position[1] >= 550)):
            menu.mouse_handler(position)
        elif ((position[0] >= 355 and position[1] <= 600) and (position[0] <= 555 and position[1] >= 550)):
            menu.getInfo()
        elif ((position[0] >= 575 and position[1] <= 600) and (position[0] <= 775 and position[1] >= 550)):
            menu.quit()
        elif ((position[0] >= 355 and position[1] <= 670) and (position[0] <= 555 and position[1] >= 620)):
            menu.getGuide()


# The background image of the battle
class Background:
    def __init__(self):
        # For battlefield
        self.image = simplegui.load_image('https://www.subeimagenes.com/img/bgs-1210457.PNG')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.columns = 3
        self.rows = 4
        self.frameSize = ((self.width // self.columns), (self.height // self.rows))
        self.frameCentre = (self.frameSize[0] / 2, self.frameSize[1] / 2)
        self.frame_index = (0, 0)
        self.center_source = [self.frameSize[i] * self.frame_index[i] + self.frameCentre[i] for i in [0, 1]]

        # For bottom box
        self.box = simplegui.load_image('https://media.giphy.com/media/lUWK158j2nTeU/giphy-facebook_s.jpg')
        self.boxWidth = self.box.get_width()
        self.boxHeight = self.box.get_height()
        self.boxColumns = 1
        self.boxRows = 1
        self.boxFrameSize = ((self.boxWidth // self.boxColumns), (self.boxHeight // self.boxRows))
        self.boxFrameCentre = (self.boxFrameSize[0] / 2, self.boxFrameSize[1] / 2)
        self.boxFrame_index = (0, 0)
        self.boxCenter_source = [self.boxFrameSize[i] * self.boxFrame_index[i] + self.boxFrameCentre[i] for i in [0, 1]]

    # Draws the battle backgrounds on canvas
    def draw(self, canvas):
        canvas.draw_image(self.image, self.center_source, self.frameSize,
                          (CANVAS_WIDTH / 2, (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 4),
                          (CANVAS_WIDTH, (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 8))

        canvas.draw_image(self.box, self.boxCenter_source, self.boxFrameSize,
                          (CANVAS_WIDTH / 2, (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 9),
                          (CANVAS_WIDTH, (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 2))


# The buttons used to determine what actions the user can take/do in battle
class Buttons:
    # Initialises the buttons and their text
    def __init__(self):
        # For bottom box
        self.box = simplegui.load_image('http://play.everafterhigh.com/Static/images/ui/button-wdyfl-sprites.png')
        self.boxWidth = self.box.get_width()
        self.boxHeight = self.box.get_height()
        self.boxColumns = 1
        self.boxRows = 4
        self.boxFrameSize = ((self.boxWidth // self.boxColumns), (self.boxHeight // self.boxRows))
        self.boxFrameCentre = (self.boxFrameSize[0] / 2, self.boxFrameSize[1] / 2)
        self.boxFrame_index = (0, 1)
        self.boxCenter_source = [self.boxFrameSize[i] * self.boxFrame_index[i] + self.boxFrameCentre[i] for i in [0, 1]]
        self.attack = "ATTACK"
        self.aBoost = "BOOST ATTACK"
        self.dBoost = "BOOST DEFENCE"

    # Draws the buttons on canvas
    def draw(self, canvas):
        canvas.draw_image(self.box, self.boxCenter_source, self.boxFrameSize,
                          ((CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 2.5, (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 8.25),
                          ((CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 2.25, (CANVAS_HEIGHT / VERTICAL_DIVIDERS)))

        canvas.draw_image(self.box, self.boxCenter_source, self.boxFrameSize,
                          ((CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 5, (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 8.25),
                          ((CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 2.25, (CANVAS_HEIGHT / VERTICAL_DIVIDERS)))

        canvas.draw_image(self.box, self.boxCenter_source, self.boxFrameSize,
                          ((CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 7.5, (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 8.25),
                          ((CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 2.25, (CANVAS_HEIGHT / VERTICAL_DIVIDERS)))

        attack = (frame.get_canvas_textwidth(self.attack, 20, 'monospace')) / 2
        boostAttack = frame.get_canvas_textwidth(self.aBoost, 20, 'monospace') / 2
        boostDefence = frame.get_canvas_textwidth(self.dBoost, 20, 'monospace') / 2

        canvas.draw_text(self.attack, (
            ((CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 2.25 - attack / 2.5, (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 8.3)),
                         20,
                         'White', 'monospace')
        canvas.draw_text(self.aBoost, (
            ((CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 5 - boostAttack, (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 8.3)), 20,
                         'White', 'monospace')
        canvas.draw_text(self.dBoost, (
            ((CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 7.25 - boostDefence / 1.5,
             (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 8.3)),
                         20, 'White', 'monospace')

    # Handles the on-screen battle buttons
    def mouse_handler(self, position):
        if ((position[0] >= 135 and position[1] <= 610) and (position[0] <= 335 and position[1] >= 545)):
            battle.attack_button()
        elif ((position[0] >= 355 and position[1] <= 610) and (position[0] <= 555 and position[1] >= 545)):
            battle.boost_attack_button()
        elif ((position[0] >= 575 and position[1] <= 610) and (position[0] <= 775 and position[1] >= 545)):
            battle.boost_defence_button()


# Determines which sprite to use
class Sprite:
    def __init__(self, image, columns, rows):
        self.image = simplegui.load_image(image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.columns = columns
        self.rows = rows
        self.frameSize = ((self.width // self.columns), (self.height // self.rows))
        self.enlarged = (self.frameSize[0] * 3, self.frameSize[1] * 3)
        self.frameCentre = (self.frameSize[0] / 2, self.frameSize[1] / 2)

    # Draws the sprite to canvas
    def draw(self, canvas, pos, size, frame_index=(0, 0)):
        center_source = [self.frameSize[i] * frame_index[i] + self.frameCentre[i] for i in [0, 1]]
        size_source = self.frameSize
        center_dest = pos.getP()
        size_dest = size
        canvas.draw_image(self.image, center_source, size_source, center_dest, size_dest)


# A class for creating a sprite for the sheild when then player or enemy's attack is boosted
class Sheild:
    # Loads the sprite
    def __init__(self):
        self.image = simplegui.load_image('https://www.spriters-resource.com/resources/sheets/97/100140.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.columns = 5
        self.rows = 5
        self.frameSize = (self.width // self.columns, self.height // self.rows)
        self.frameCentre = (self.frameSize[0] / 2, self.frameSize[1] / 2)
        self.frameIndex = [0, 0]

    # Draws the sprite on canvas
    def draw(self, canvas, pos, size):
        center_source = [self.frameSize[i] * self.frameIndex[i] + self.frameCentre[i] for i in [0, 1]]
        size_source = self.frameSize
        center_dest = pos.getP()
        size_dest = size
        canvas.draw_image(self.image, center_source, size_source, center_dest, size_dest)

    # Obtains the next frame of the sprite
    def nextFrame(self):
        self.frameIndex[0] = (self.frameIndex[0] + 1) % self.columns

        if self.frameIndex[0] == 0:
            self.frameIndex[1] = (self.frameIndex[1] + 1) % self.rows

    # Resets the sprite
    def reset(self):
        self.frameIndex = [0, 0]

    # Determines if the sprite has finished its animation
    def complete(self):
        complete = self.frameIndex[0] == 1 and self.frameIndex[1] == 3
        if complete:
            self.reset()
        return complete


# The fireball that goes towards the player or enemy
class Fireball:
    # Initialises the sprite for the fireball
    def __init__(self, frameIndex):
        self.image = simplegui.load_image('https://opengameart.org/sites/default/files/fireball_0.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.columns = 8
        self.rows = 8
        self.frameSize = (self.width // self.columns, self.height // self.rows)
        self.frameSizeEnlarged = (self.frameSize[0] * 4, self.frameSize[1] * 4)
        self.frameCentre = (self.frameSize[0] / 2, self.frameSize[1] / 2)
        self.frameIndex = frameIndex
        self.originalFrameIndex = frameIndex
        self.empty = (8, 8)

    # Draws the fireball on the canvas
    def draw(self, canvas, pos, size):
        center_source = [self.frameSize[i] * self.frameIndex[i] + self.frameCentre[i] for i in [0, 1]]
        size_source = self.frameSize
        center_dest = pos.getP()
        size_dest = size
        canvas.draw_image(self.image, center_source, size_source, center_dest, size_dest)

    # Obtains the next frame for the sprite
    def nextFrame(self):
        self.frameIndex[0] = (self.frameIndex[0] + 1) % self.columns

    # Essentially clears the explostion once it reaches its las
    def blank(self):
        self.frameIndex = [10, 10]

    # Resets the sprite ready for its next use
    def reset(self):
        self.frameIndex = self.originalFrameIndex


# The explosion for when the fireball hits a player
class Explosion:
    # Initialises the sprite for the explosion
    def __init__(self):
        self.image = simplegui.load_image('http://moziru.com/images/drawn-explosion-sprite-1.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.columns = 8
        self.rows = 6
        self.frameSize = (self.width // self.columns, self.height // self.rows)
        self.frameSizeEnlarged = (self.frameSize[0] * 1.5, self.frameSize[1] * 1.5)
        self.frameCentre = (self.frameSize[0] / 2, self.frameSize[1] / 2)
        self.frameIndex = [0, 0]

    # Draws the explosion on canvas when the fireball has completed
    def draw(self, canvas, pos, size):
        center_source = [self.frameSize[i] * self.frameIndex[i] + self.frameCentre[i] for i in [0, 1]]
        size_source = self.frameSize
        center_dest = pos.getP()
        size_dest = size
        canvas.draw_image(self.image, center_source, size_source, center_dest, size_dest)

    # Obtains the next frame for the explosion
    def nextFrame(self):
        self.frameIndex[0] = (self.frameIndex[0] + 1) % self.columns
        if self.frameIndex[0] == 0:
            self.frameIndex[1] = (self.frameIndex[1] + 1) % self.rows

    # Determines whether the explosion sprite has finished or not
    def complete(self):
        complete = self.frameIndex[0] == 7 and self.frameIndex[1] == 5
        return complete


# The sprite used to indicate that the player or enemy has boosted their defence
class Sword:
    # Initialises the sprite
    def __init__(self):
        self.image = simplegui.load_image('https://image.ibb.co/dTFXTS/State_Up1.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.columns = 5
        self.rows = 3
        self.frameSize = (self.width // self.columns, self.height // self.rows)
        self.frameCentre = (self.frameSize[0] / 2, self.frameSize[1] / 2)
        self.frameIndex = [0, 0]

    # Draws the sprite on canvas
    def draw(self, canvas, pos, size):
        center_source = [self.frameSize[i] * self.frameIndex[i] + self.frameCentre[i] for i in [0, 1]]
        size_source = self.frameSize
        center_dest = pos.getP()
        size_dest = size
        canvas.draw_image(self.image, center_source, size_source, center_dest, size_dest, 135)

    # Obtains the next frame for the sprite
    def nextFrame(self):
        self.frameIndex[0] = (self.frameIndex[0] + 1) % self.columns
        if self.frameIndex[0] == 0:
            self.frameIndex[1] = (self.frameIndex[1] + 1) % self.rows

    # Resets the sprite
    def reset(self):
        self.frameIndex = [0, 0]

    # Determines if the sprite is complete
    def complete(self):
        complete = self.frameIndex[0] == 4 and self.frameIndex[1] == 2
        if complete:
            self.reset()
        return complete


# The class for the projectile
class Projectile:
    def __init__(self, pos, other):
        self.pos = pos
        self.radius = 20
        self.other = other
        self.vel = self.other.pos.copy().subtract(self.pos)

    # The distance to the ...
    def distance_to(self):
        return (self.pos - self.other.pos).length()

    # Updates the position
    def update(self):
        self.pos.add(self.vel.copy().divide(20))

    def updateWaterFall(self):
        vel = self.other.pos.copy().subtract(self.pos.copy())
        self.pos.add(vel.copy().divide(10))


# Drawing HP bars
class hpBar:
    # Initialises the health bar for the player/enemy
    def __init__(self, pos):
        self.backgroundWidth = 200
        self.maxWidth = 200
        self.height = 50
        self.pos = pos

    # Draws the health bars on the canvas
    def draw(self, canvas, health, maxHealth, colour):
        width = health / maxHealth * self.maxWidth
        if width < 0:
            width = 0
        canvas.draw_polygon([self.pos, (self.pos[0] + self.backgroundWidth, self.pos[1]),
                             (self.pos[0] + self.backgroundWidth, self.pos[1] + self.height),
                             (self.pos[0], self.pos[1] + self.height)], 1, 'White', 'White')
        canvas.draw_polygon(
            [self.pos, (self.pos[0] + width, self.pos[1]), (self.pos[0] + width, self.pos[1] + self.height),
             (self.pos[0], self.pos[1] + self.height)], 1, colour, colour)


# Player in battle
class Player1:
    # Initialises the player during a battle by setting stats
    def __init__(self, name, health, attack, defence, speed, sprite):
        self.name = name
        self.baseHealth = health
        self.baseAttack = attack
        self.baseDefence = defence
        self.baseSpeed = speed

        self.maxHealth = self.baseHealth
        self.health = health
        self.attackStat = self.baseAttack
        self.defenceStat = self.baseDefence
        self.speedStat = self.baseSpeed

        # Base boosts and move
        self.defBoost = 1
        self.attBoost = 1
        self.attacking = False
        self.projectile = False
        self.defending = False
        self.attackboosting = False

        # Drawing and animations
        self.radius = 50
        self.x = (CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 3
        self.y = (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 6.8
        self.pos = Vector(self.x, self.y)
        self.pos_start = Vector(self.x, self.y)
        self.vel = Vector()
        self.sprite = Sprite('https://veekun.com/static/pokedex/downloads/generation-3-back.png', 25, 16)
        self.frame_index = sprite
        self.shield = Sheild()
        self.sword = Sword()
        self.fireball = Fireball([0, 3])
        self.explosion = Explosion()
        self.hpBar = hpBar((self.x * 2, self.y))
        self.textPos = (self.x * 2, self.y - 10)
        self.text = ''
        self.moveOver = False
        self.p = None
        self.nuke = []
        self.nukeExplosion = []
        self.attackMax = False
        self.first = False
        global BATTLE_ON
        # Score
        global beenHealed
        global score

    # Boost attack
    def attack_boost(self):
        if self.attBoost < 3:
            self.attBoost += 0.5

    # Boost defence
    def defence_boost(self):
        if self.defBoost < 3:
            self.defBoost += 0.5

    # Reset attack boost
    def attack_reset(self):
        self.attBoost = 1

    # Reset defence boost
    def defence_reset(self):
        self.defBoost = 1

    # Heals the player by resetting to maxHealth
    def health_reset(self):
        global beenHealed
        global score
        if (beenHealed is False):
            # print ('healing')
            self.health = self.maxHealth
            score = score - 3
            beenHealed = True
        if (beenHealed is True):
            if (c.transition(5)):
                beenHealed = False
                # print ('treueueu')

    # Add to players base stats
    def level_up(self):
        self.maxHealth += random.randint(8, 12)
        self.health = self.maxHealth
        self.attackStat += random.randint(8, 12)
        self.defenceStat += random.randint(8, 12)
        self.speedStat += random.randint(8, 12)

    # Reset all stats to base
    def reset_level(self):
        self.maxHealth = self.baseHealth
        self.health = self.maxHealth
        self.attackStat = self.baseAttack
        self.defenceStat = self.baseDefence
        self.speedStat = self.baseSpeed

    # Returns current health of player
    def alive(self):
        return self.health > 0

    # Attack opponent
    def attack(self, other):

        self.moveOver = True
        self.attacking = True
        self.text = 'Player attacked'
        self.p = Projectile(self.pos.copy(), other)
        other.health = other.health - (
            ((self.attackStat * self.attBoost) / (other.defenceStat * other.defBoost)) * randomModifierPlayer())
        if self.attackMax:
            for x in range(4):
                pPos = other.pos.copy() - Vector(random.randint(-CANVAS_WIDTH, CANVAS_WIDTH),
                                                 random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT * 2))
                p = Projectile(pPos, other)
                e = Explosion()
                self.nuke.append(p)
                self.nukeExplosion.append(e)
            self.attack_reset()
            other.defence_reset()

    # Boost player attack modifier
    def boost_attack(self):
        self.moveOver = True
        self.attackboosting = True
        if self.attBoost <= 3:
            self.attack_boost()
            self.text = 'Player boosted attacked'
        if self.attBoost == 3:
            self.text = 'Player attack maximised'
            self.attackMax = True
            self.first = True

    # Boost player defence modifier
    def boost_defence(self):
        self.moveOver = True
        self.defending = True
        if self.defBoost <= 3:
            self.defence_boost()
            self.text = 'Player boosted defence'
        if self.defBoost == 3:
            self.text = 'Player defence maximised'

    # Drawing player and animations
    def draw(self, canvas):
        self.hpBar.draw(canvas, self.health, self.maxHealth, 'Green')
        canvas.draw_text(self.name, (self.textPos), 24, 'White', 'monospace')
        self.sprite.draw(canvas, self.pos, self.sprite.enlarged, self.frame_index)
        if self.defending:
            self.shield.draw(canvas, self.pos, self.shield.frameSize)
        if self.attackboosting:
            self.sword.draw(canvas, self.pos, self.sword.frameSize)
        if self.attacking:
            if self.attackMax:
                if self.first:
                    self.fireball.frameIndex = [0, 6]
                    self.first = False
                else:
                    for p in self.nuke:
                        self.fireball.draw(canvas, p.pos, self.fireball.frameSizeEnlarged)
                        if p.distance_to() < (self.p.radius + self.enemy.radius):
                            for x in self.nukeExplosion:
                                x.draw(canvas, p.pos, self.explosion.frameSizeEnlarged)
            else:
                self.fireball.reset()
                self.fireball.draw(canvas, self.p.pos, self.fireball.frameSizeEnlarged)
                if self.p.distance_to() < (self.p.radius + self.enemy.radius):
                    self.p.vel = Vector(0, 0)
                    self.explosion.draw(canvas, self.p.pos, self.explosion.frameSizeEnlarged)

    # updating player and animations
    def update(self):
        global BATTLE_ON
        if self.defending:
            if clock.transition(3):
                self.shield.nextFrame()
                if self.shield.complete():
                    self.defending = False
                    self.moveOver = False
        if self.attackboosting:
            if clock.transition(3):
                self.sword.nextFrame()
                if self.sword.complete():
                    self.attackboosting = False
                    self.moveOver = False
        if self.attacking:
            if self.attackMax:
                if self.attackMax:
                    for p in self.nuke:
                        p.updateWaterFall()
                        self.fireball.nextFrame()
                        if p.distance_to() < (self.p.radius + self.enemy.radius):
                            self.fireball.blank()
                    for x in self.nukeExplosion:
                        x.nextFrame()
                        if x.complete():
                            self.fireball.reset()
                            self.attacking = False
                            self.moveOver = False
                            self.attackMax = False
                            if self.enemy.health <= 0:
                                BATTLE_ON = False
            else:
                self.p.update()
                self.fireball.nextFrame()
                if self.p.distance_to() < (self.p.radius + self.enemy.radius):
                    self.explosion.nextFrame()
                    self.fireball.blank()
                    if self.explosion.complete():
                        self.fireball.reset()
                        self.attacking = False
                        self.moveOver = False
                        if self.enemy.health <= 0:
                            BATTLE_ON = False


# Enemy in battle
class Enemy:
    # Initialises the enemy in battle and sets its stats
    def __init__(self, name, health, attack, defence, speed, sprite):
        self.name = name
        self.maxHealth = health
        self.health = health
        self.attackStat = attack
        self.defenceStat = defence
        self.speedStat = speed
        self.defBoost = 1
        self.attBoost = 1
        self.attacking = False
        self.projectile = False
        self.defending = False
        self.attackboosting = False
        self.x = (CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 7.25
        self.y = (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 3.25
        self.pos = Vector(self.x, self.y)
        self.pos_start = Vector(self.x, self.y)
        self.vel = Vector()
        self.sprite = Sprite('https://veekun.com/static/pokedex/downloads/generation-3.png', 25, 16)
        self.frame_index = sprite
        self.radius = 50
        self.fireball = Fireball([0, 7])
        self.explosion = Explosion()
        self.shield = Sheild()
        self.sword = Sword()
        self.hpBar = hpBar((self.x / 4, self.y / 3))
        self.textPos = (self.x / 4, (self.y / 3) - 10)
        self.text = ''
        self.p = None
        self.nuke = []
        self.nukeExplosion = []
        self.attackMax = False
        self.first = False
        self.player_alive = True
        global PLAYER_ALIVE
        global BATTLE_ON

    # Boost attack
    def attack_boost(self):
        if self.attBoost < 3:
            self.attBoost += 0.5

    # Boost defence
    def defence_boost(self):
        if self.defBoost < 3:
            self.defBoost += 0.5

    # Reset attack boost
    def attack_reset(self):
        self.attBoost = 1

    # Reset defence boost
    def defence_reset(self):
        self.defBoost = 1

    # Heals the enemy by resetting to maxHealth
    def health_reset(self):
        self.health = self.maxHealth

    # Attack opponent
    def attack(self, other):
        self.moveOver = True
        self.attacking = True
        self.text = 'Enemy attacked'
        self.p = Projectile(self.pos.copy(), other)
        other.health = other.health - (
            ((self.attackStat * self.attBoost) / (other.defenceStat * other.defBoost)) * randomModifierPlayer())
        if self.attackMax:
            for x in range(4):
                pPos = other.pos.copy() - Vector(random.randint(-CANVAS_WIDTH, CANVAS_WIDTH),
                                                 random.randint(CANVAS_HEIGHT, CANVAS_HEIGHT * 2))
                p = Projectile(pPos, other)
                e = Explosion()
                self.nuke.append(p)
                self.nukeExplosion.append(e)
            self.attack_reset()
            other.defence_reset()

    # Boost attack modifier
    def boost_attack(self):
        self.moveOver = True
        self.attackboosting = True
        if self.attBoost <= 3:
            self.attack_boost()
            self.text = 'Enemy boosted attacked'
        if self.attBoost == 3:
            self.text = 'Enemy attack maximised'
            self.attackMax = True
            self.first = True

    # Boost defence modifier
    def boost_defence(self):
        self.moveOver = True
        self.defending = True
        if self.defBoost >= 3:
            self.text = 'Enemy defence maximised'
        else:
            self.defence_boost()
            self.text = 'Enemy boosted defence'

    # Select random move
    def random_move(self):
        rand_move = random.randint(1, 100)
        if rand_move >= 1 and rand_move <= 30:
            self.attack(self.player)
            self.update()

        elif rand_move >= 31 and rand_move <= 65:
            self.boost_attack()

        elif rand_move >= 66 and rand_move <= 100:
            self.boost_defence()

    def is_alive(self):
        return self.player_alive == True

    # Drawing enemy character
    def draw(self, canvas):
        self.hpBar.draw(canvas, self.health, self.maxHealth, 'Red')
        canvas.draw_text(self.name, (self.textPos), 24, 'White', 'monospace')
        self.sprite.draw(canvas, self.pos, self.sprite.enlarged, self.frame_index)
        if self.defending:
            self.shield.draw(canvas, self.pos, self.shield.frameSize)
        if self.attackboosting:
            self.sword.draw(canvas, self.pos, self.sword.frameSize)
        if self.attacking:
            if self.attackMax:
                if self.first:
                    self.fireball.frameIndex = [0, 6]
                    self.first = False
                else:
                    for p in self.nuke:
                        self.fireball.draw(canvas, p.pos, self.fireball.frameSizeEnlarged)
                        if p.distance_to() < (self.p.radius + self.player.radius):
                            p.vel = Vector(0, 0)
                            for x in self.nukeExplosion:
                                x.draw(canvas, p.pos, self.explosion.frameSizeEnlarged)
            else:
                self.fireball.draw(canvas, self.p.pos, self.fireball.frameSizeEnlarged)
                if self.p.distance_to() < (self.p.radius + self.player.radius):
                    self.p.vel = Vector(0, 0)
                    self.explosion.draw(canvas, self.p.pos, self.explosion.frameSizeEnlarged)

    # Updateing enemy animations
    def update(self):
        if self.defending:
            if clock.transition(3):
                self.shield.nextFrame()
                if self.shield.complete():
                    self.defending = False
        if self.attackboosting:
            if clock.transition(3):
                self.sword.nextFrame()
                if self.sword.complete():
                    self.attackboosting = False
        if self.attacking:
            if self.attackMax:
                if self.attackMax:
                    for p in self.nuke:
                        p.updateWaterFall()
                        self.fireball.nextFrame()
                        if p.distance_to() < (self.p.radius + self.player.radius):
                            self.fireball.blank()
                    for x in self.nukeExplosion:
                        x.nextFrame()
                        if x.complete():
                            self.fireball.reset()
                            self.attacking = False
                            self.attackMax = False
                            if not self.player.alive():
                                self.player_alive = True
                                BATTLE_ON = False
            else:
                self.p.update()
                self.fireball.nextFrame()
                if self.p.distance_to() < (self.p.radius + self.player.radius):
                    self.explosion.nextFrame()
                    self.fireball.blank()
                    if self.explosion.complete():
                        self.fireball.reset()
                        self.attacking = False
                        if not self.player.alive():
                            self.player_alive = True
                            BATTLE_ON = False


# Player vs Enemy battle
class Battle:
    # Initialises the battle
    def __init__(self, player, enemy):
        self.background = Background()
        self.textPlayer = 'Battle Started'
        self.textEnemy = ''
        self.button = Buttons()

    # Method for clicking attack button
    def attack_button(self):
        self.player = Map.a
        self.enemy = Map.b
        if BATTLE_ON and self.player.speedStat == self.enemy.speedStat:
            rand_order = self.rand_first()
            if BATTLE_ON and rand_order == 1:
                self.player.attack(self.enemy)
                self.textPlayer = self.player.text
                if BATTLE_ON:
                    self.enemy.random_move()
                    self.textEnemy = self.enemy.text
            elif BATTLE_ON and rand_order == 0:
                self.enemy.random_move()
                self.textEnemy = self.enemy.text
                if BATTLE_ON:
                    self.player.attack(self.enemy)
                    self.textPlayer = self.player.text

        elif BATTLE_ON and ((self.player.speedStat < self.enemy.speedStat)):
            self.enemy.random_move()
            self.textEnemy = self.enemy.text
            if BATTLE_ON:
                self.player.attack(self.enemy)
                self.textPlayer = self.player.text

        elif BATTLE_ON and ((self.player.speedStat > self.enemy.speedStat)):
            self.player.attack(self.enemy)
            self.textPlayer = self.player.text
            if BATTLE_ON:
                self.enemy.random_move()
                self.textEnemy = self.enemy.text

    # Method for clicking boost attack button
    def boost_attack_button(self):
        self.player = Map.a
        self.enemy = Map.b
        if BATTLE_ON and self.player.speedStat == self.enemy.speedStat:
            rand_order = self.rand_first()
            if BATTLE_ON and rand_order == 1:
                self.player.boost_attack()
                self.textPlayer = self.player.text
                if BATTLE_ON:
                    self.enemy.random_move()
                    self.textEnemy = self.enemy.text
            elif BATTLE_ON and rand_order == 0:
                self.enemy.random_move()
                self.textEnemy = self.enemy.text
                if BATTLE_ON:
                    self.player.boost_attack()
                    self.textPlayer = self.player.text

        elif BATTLE_ON and ((self.player.speedStat > self.enemy.speedStat)):
            self.player.boost_attack()
            self.textPlayer = self.player.text
            if BATTLE_ON:
                self.enemy.random_move()
                self.textEnemy = self.enemy.text

        elif BATTLE_ON and ((self.player.speedStat < self.enemy.speedStat)):
            self.enemy.random_move()
            self.textEnemy = self.enemy.text
            if BATTLE_ON:
                self.player.boost_attack()
                self.textPlayer = self.player.text

    # Method for clicking boost defence button
    def boost_defence_button(self):
        self.player = Map.a
        self.enemy = Map.b
        if BATTLE_ON and self.player.speedStat == self.enemy.speedStat:
            rand_order = self.rand_first()
            if BATTLE_ON and rand_order == 1:
                self.player.boost_defence()
                self.textPlayer = self.player.text
                if BATTLE_ON:
                    self.enemy.random_move()
                    self.textEnemy = self.enemy.text
            elif BATTLE_ON and rand_order == 0:
                self.enemy.random_move()
                self.textEnemy = self.enemy.text
                if BATTLE_ON:
                    self.player.boost_defence()
                    self.textPlayer = self.player.text

        elif BATTLE_ON and ((self.player.speedStat > self.enemy.speedStat)):
            self.player.boost_defence()
            self.textPlayer = self.player.text
            if BATTLE_ON:
                self.enemy.random_move()
                self.textEnemy = self.enemy.text

        elif BATTLE_ON and ((self.player.speedStat < self.enemy.speedStat)):
            self.enemy.random_move()
            self.textEnemy = self.enemy.text
            if BATTLE_ON:
                self.player.boost_defence()
                self.textPlayer = self.player.text

    # Method to get random int for who goes first
    @staticmethod
    def rand_first():
        return random.randint(0, 1)

    # Method for drawing the battle
    def draw(self, canvas):
        self.player = Map.a
        self.enemy = Map.b

        clock.tick()
        self.background.draw(canvas)
        canvas.draw_text(self.textPlayer,
                         ((CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 0.5, (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 9.25),
                         30, 'White', 'monospace')
        enemyTextSize = (frame.get_canvas_textwidth(self.textEnemy, 30, 'monospace'))
        canvas.draw_text(self.textEnemy,
                         (CANVAS_WIDTH - ((CANVAS_WIDTH / HORIZONTAL_DIVIDERS) * 0.5 + enemyTextSize),
                          (CANVAS_HEIGHT / VERTICAL_DIVIDERS) * 9.25), 30, 'White', 'monospace')
        self.enemy.draw(canvas)
        self.player.draw(canvas)
        self.player.update()
        self.enemy.update()
        self.button.draw(canvas)

        if not self.player.alive() and self.enemy.is_alive():
            print(self.enemy.player_alive)
            print(PLAYER_ALIVE)
            text_width = frame.get_canvas_textwidth('BATTLE OVER', 50, 'sans-serif')
            canvas.draw_text('BATTLE OVER', ((CANVAS_WIDTH / 2 - text_width / 2), (CANVAS_HEIGHT / 2)), 50, 'Grey',
                             'sans-serif')
            menu.playGame = False
            menu.message = "Battle Over"
            menu.messageTwo = ""
            self.player.reset_level()
            Map.reset()


# Used for timing?
class Clock:
    def __init__(self):
        self.time = 0

    def tick(self):
        # time> 5000 is to reset time to 0 to prevent overflow
        if self.time > 5000:
            self.time = 0
        self.time += 1

    def transition(self, rate):
        return self.time % rate == 0


# Randomises the players sprite/character
def randomModifierPlayer():
    return random.randint(40, 60)


# Randomises the enemy's sprite/character
def randomModifierEnemy():
    return random.randint(40, 55)


# Handles the mouse clicks for the buttons
def mouse_handler(position):
    if (menu.playGame):
        battle.button.mouse_handler(position)
    else:
        menuButtons.mouse_handler(position)


# Initialises basic items required for gameplay
menu = Menu()
menuButtons = MenuButtons()
c = Clock1()
clock = Clock()
kbd = Keyboard()
opening = Opening()
transition = Transition()
fb = FireBlast(Vector(460, 350))

# Initialises the players, maps, etc
Player = Character(Vector(300, 340))
inter = Interaction(Player, kbd)
Pokemon = RandomPokemon(random.randint(0, 8), random.randint(0, 8), random.randint(0, 8))
Map = Map((920, 700))
battle = Battle(Map.a, Map.b)

# Required to set various things to allow user interaction and to draw on canvas
# Also begins the frame
frame = simplegui.create_frame('Not Pokemon', CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(inter.draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.set_mouseclick_handler(mouse_handler)
frame.start()