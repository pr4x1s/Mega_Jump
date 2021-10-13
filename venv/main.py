import pygame
from pygame.locals import *
import threading
from os import path
from random import randint


class Player:
    def __init__(self, x, y):
        self.jumpCounter = 0
        self.jumping = False
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.sprite = pygame.image.load(path.join("tempplayer.png"))


    def update_position(self):
        self.x += self.xVel
        self.y -= self.yVel

    def addXVel(self, i):
        self.xVel = i

    def addYVel(self, i):
        self.yVel = i

    def platform_check(self):
        pass

    def jump(self):
        self.jumping = True


blockInstances = []


class Block:
    def __init__(self):
        self.isOnScreen = False
        self.x = 0
        self.y = 0
        self.sprite = pygame.Surface((50, 5))
        self.blockType = 0
        global blockInstances
        blockInstances.append(self)
        self.level_number = 0

    def show(self):
        self.isOnScreen = True

    def hide(self):
        self.isOnScreen = False

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_blocktype(self, btype):
        self.blockType = btype


def update():
    pygame.display.flip()


def level_generator(numberOfBlocks):
    blocks = blockInstances
    del blockInstances[0:]
    for i in xrange(numberOfBlocks):
        blocks.append(Block())
    for block in blocks:
        block.level_number = levelNumber
        block.set_x(randint(0, 1850))
        block.set_y(randint(0, 950))
    return blocks


def level_blitter(level):
    currentLevel = levelNumber
    print currentLevel
    for block in level:
        if block.level_number == currentLevel:
            block.show()
            print 'showing'
        else:
            block.hide()
            print 'hiding'
        # update()


def event_handler():
    while done is False:
        clock.tick(90)
        pygame.display.init()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_p:
                    pygame.display.toggle_fullscreen()
                if event.key == pygame.K_w and player.y <= 1000:
                    player.jump()
                if event.key == pygame.K_o:
                    global levelNumber
                    levelNumber += 1
                    level_blitter(level_generator(10))
                # if event.key == pygame.K_a:
                    # player.xVel = -5
                # if event.key == pygame.K_d:
                    # player.xVel = 5
# Alternate event handler
        keys = pygame.key.get_pressed()
        if keys[K_a] and player.x > 10:
            player.x -= 5
        if keys[K_d] and player.x < 1890:
            player.x += 5
# //////////////////////////////////////////////////
        if player.y >= 1001:
            player.jumping = False
            player.y = 1000
            player.yVel = 0
        if player.jumping is True:
            player.yVel = -.04 * (player.jumpCounter - 16)**2 + 10
            if player.yVel > maxVel:
                player.yVel = maxVel
            if player.yVel < minVel:
                player.yVel = minVel
            player.jumpCounter += 1
        else:
            player.jumpCounter = 0
        player.update_position()
        player.xVel = 0
        pygame.time.wait(1)


def display_loop():
    pygame.display.init()
    while done is False:
        try:
            window.fill((255, 255, 255))
            window.blit(player.sprite, (player.x, player.y))
            global blockInstances
            for block in blockInstances:
                if block.isOnScreen:
                    window.blit(block.sprite, (block.x, block.y))
            update()

        except:
            pygame.quit()
            quit()


if __name__ == "__main__":
    levelNumber = 0
    player = Player(100, 1000)
    maxVel = 10
    minVel = -maxVel
    done = False
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Mega Jump")
    pygame.key.set_repeat()
    pygame.mouse.set_visible(False)
    pygame.init()
    eventLoop = threading.Thread(target=event_handler)
    displayLoop = threading.Thread(target=display_loop)
    eventLoop.start()
    displayLoop.start()
    eventLoop.join()
    displayLoop.join()

