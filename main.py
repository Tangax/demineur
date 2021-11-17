import pygame
import random
pygame.init()

"""Constantes"""


"""Classes"""


class Game:
    width = 1000
    height = 1000
    scale = 50
    gheight = int(0.8 * height)  # La hauteur de la zone de jeu uniquement
    rows = width // scale
    cols = height // scale

    imgs = {
        "cell": pygame.transform.scale((pygame.image.load("cell.png")), (scale, scale)),
        "clicked_cell": pygame.transform.scale((pygame.image.load("clicked_cell.png")), (scale, scale)),
        "flag": pygame.transform.scale((pygame.image.load("flag.png")), (scale, scale)),
        "bomb": pygame.transform.scale((pygame.image.load("bomb.png")), (scale, scale))
            }

    font = pygame.font.SysFont("Calibri", int(1.2*scale), True)

    def __init__(self):
        self.win = pygame.display.set_mode((self.width, self.height))
        self.cells = [[Cell(i, j, self.scale) for i in range(self.rows)]
                      for j in range(self.cols)]
        self.display = "jeu"
        self.neighbours()

    def inGrid(self, pos):  # Vérifie si case dans la grille
        if 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols:
            return True
        else:
            return False

    def neighbours(self):  # Compte le nombre de bombes autour
        for i in range(self.rows):
            for j in range(self.cols):
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if self.inGrid((i + k, j + l)):
                            if self.cells[i + k][j + l].isBomb:
                                self.cells[i][j].bombAround += 1

    def click(self, pos):  # Creuse la case
        posx = pos[0]
        posy = pos[1]

        if self.cells[posx][posy].isBomb: #  Si c'est une bomb on arrête
            self.display = "gameover"
            for list_cell in self.cells:
                for cell in list_cell:
                    if cell.isBomb and not(cell.isFlagged):
                        cell.showBomb = True
            return

        if self.cells[posx][posy].isReaveled or self.cells[posx][posy].isFlagged:
            return
        else:
            self.cells[posx][posy].isReaveled = True
            if self.cells[posx][posy].bombAround == 0:
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if self.inGrid((posx + k, posy + l)):
                            self.click((posx + k, posy + l))
            else:
                return

    def flag(self, pos):  # Pose un drapeau sur la case
        if not(self.cells[pos[0]][pos[1]].isReaveled):
            if not(self.cells[pos[0]][pos[1]].isFlagged):
                self.cells[pos[0]][pos[1]].isFlagged = True
            else:
                self.cells[pos[0]][pos[1]].isFlagged = False

    def draw(self):  # Affiche le jeu
        pygame.display.update()
        self.win.fill((200, 200, 200))
        for list_cell in self.cells:
            for cell in list_cell:
                cell.draw(self.win)

    def playing(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                self.click((pos[1] // self.scale, pos[0] // self.scale))
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                self.flag((pos[1] // self.scale, pos[0] // self.scale))

    def gameOver(self):
        pass

    def run(self):  # Lance le jeu
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(144)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if self.display == "jeu":
                    self.playing(event)
                elif self.display == "gameover":
                    self.gameOver()

            self.draw()

        pygame.quit()


class Cell:
    def __init__(self, x, y, scale):
        self.x = x * scale
        self.y = y * scale
        self.scale = scale
        self.isBomb = self.randomBomb()
        self.bombAround = 0
        self.isReaveled = False
        self.isFlagged = False
        self.showBomb = False
        self.clickedBomb = False

    @staticmethod
    def randomBomb():
        seed = random.randint(0, 6)
        if seed == 0:
            return True
        else:
            return False

    def draw(self, win):
        if not self.isReaveled:
            win.blit(Game.imgs["cell"], (self.x, self.y))
        if self.isFlagged:
            win.blit(Game.imgs["flag"], (self.x, self.y))
        if self.isReaveled and not(self.showBomb):
            win.blit(Game.imgs["clicked_cell"], (self.x, self.y))
            if self.isReaveled and self.bombAround != 0:
                textsurface = Game.font.render(str(self.bombAround), False, (255, 0, 0))
                win.blit(textsurface, (self.x, self.y))
        if self.showBomb:
            win.blit(Game.imgs["bomb"], (self.x, self.y))


g = Game()
g.run()
