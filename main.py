import pygame
#from pygame.locals import  *
import time
from random import randint, randrange

# colors

black = (0, 0, 0)
textcolor1 = (255, 32, 23)
textcolor2 = (23, 32, 255)
textcolorBlock = (0, 0, 235)
sunset = (253,72,47)
green = (100,255,100)
brightblue = (47,228,253)
orange = (255,113,0)
yellow = (255,236,0)
purple = (252,67,255)




pygame.init ()

#frame width and height
surfaceWidth = 800
surfaceHeight = 500

surface = pygame.display.set_mode ((surfaceWidth, surfaceHeight))
#surface = pygame.display.set_mode ((surfaceWidth, surfaceHeight),FULLSCREEN)
pygame.display.set_caption ("Flappy bird")
clock = pygame.time.Clock ()

# loading image-- use a image with transparent background

img = pygame.image.load ("bird.png")
background = pygame.image.load("background.jpg")
# getting height and width of  bird
imageWidth = img.get_width ()
imageHeight = img.get_height ()


#displaying current score and current level
def score(count,level):

    smallText = pygame.font.Font ("freesansbold.ttf", 20)

    score = "score: " + str(count) + "   level:"+str(level)
    titleTextSurface, titleTextRectangle = makeTextObjs (score, smallText, sunset)
    titleTextRectangle.center = surfaceWidth / 2, 20
    # to put text on screen
    surface.blit (titleTextSurface, titleTextRectangle)


# drawing obstacles(blocks)
def blocks(x_block, y_block, blockWidth, blockHeight, gap,color):

    pygame.draw.rect (surface, color, [x_block, y_block, blockWidth, blockHeight])
    pygame.draw.rect (surface, color,[x_block, y_block + blockHeight + gap, blockWidth, surfaceHeight - gap - blockHeight])

    # to get ring like shape at the tip of block(height =10 width =original +10)
    pygame.draw.rect (surface, textcolorBlock, [x_block - 5, blockHeight - 10, blockWidth + 10, 30])
    pygame.draw.rect (surface, textcolorBlock, [x_block - 5, y_block + blockHeight + gap, blockWidth + 10, 30])


# reply or quit function
#it pauses the game untill a key is pressed
def replay_or_quit():
    for event in pygame.event.get ([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit ()
            quit ()

        elif event.type == pygame.KEYDOWN:
            continue

        return event.key

    return None

#small function to render text
def makeTextObjs(text, font, color):
    textSurface = font.render (text, True, color)
    return textSurface, textSurface.get_rect ()


# this function is used to display messages on screen
def msgsurface(text):
    smallText = pygame.font.Font ("freesansbold.ttf", 20)
    largeText = pygame.font.Font ("freesansbold.ttf", 50)

    titleTextSurface, titleTextRectangle = makeTextObjs (text, largeText, textcolor1)
    titleTextRectangle.center = surfaceWidth / 2, surfaceHeight / 2
    # to put text on screen
    surface.blit (titleTextSurface, titleTextRectangle)

    smallTextSurface, smallTextRectangle = makeTextObjs ("Press any key to continue", smallText, textcolor2)
    # here 100 is added to height so that the small text appears a little below the   large text
    smallTextRectangle.center = surfaceWidth / 2, ((surfaceHeight / 2) + 100)

    #reading high score
    hscore = open ("score.log", 'r')
    high_score = hscore.read ()
    hscore.close ()

    highscoresurface, highscoreRectangle = makeTextObjs ("Highscore: " +high_score , smallText, textcolor2)
    # here 100 is added to height so that the small text appears a little below the   large text
    highscoreRectangle.center = surfaceWidth / 2, ((surfaceHeight / 2) + 150)

    surface.blit (smallTextSurface, smallTextRectangle)
    surface.blit (highscoresurface, highscoreRectangle)



    # updating the screen to make text appear
    pygame.display.update ()
    time.sleep (1)

    # waiting for user to make a choice
    #if a user press a key than game restarts
    while replay_or_quit () == None:
        clock.tick ()
    main ()


# gameover function
def gameOver(finalscore):

    #reading highscore
    hscore = open ("score.log", 'r')
    high_score = hscore.read ()
    hscore.close ()
    #if high score is less than current score than write current score as highscore to log file
    if high_score =="" or (int(high_score) < int(finalscore)) :

        writescore=open("score.log","w")
        writescore.write(str(finalscore))
        writescore.close()
    msgsurface ("Game Over")



#this function is used at the start of game to display highscore and start screen
def gameStart():
	#here we read high score from a log file and if a file doesnot exist we create a new one
    try:
        #reading highscore
        hscore = open ("score.log", 'r')
        high_score = hscore.read ()
        hscore.close ()
    except:
        writescore = open ("score.log", "w")
        writescore.write (str (0))
        writescore.close ()

    #this function displays the message on the screen
    msgsurface ("Press Up arrow to move the bird")


# image function
# x and y are co-ordinates.coordinates are measured from top left
def image(x, y, img):
    surface.blit (img, (x, y))


def main():
	#x and y deonote positions of bird
    x = 200
    y = 150
    #y_move is movement speed for bird  
    y_move = 0

    #x_block and y_block determine the positions of block
    x_block = surfaceWidth
    y_block = 0
    blockWidth = 80
    #block  height is randomed between 100 and  around half of surface height
    blockHeight1 = randint (100, int(surfaceHeight / 1.5)-100)
    # blockHeight2 = randint(0,int(surfaceHeight/1.5))
    # blockHeight3 = randint(0,int(surfaceHeight/1.5))

    #current score holds the current score
    current_score = 0
    

    i=1
    level=0

    #gap is the distance between blocks
    gap = int(imageHeight*4)
    #movement speed of block
    block_move = 4

    game_over = False

    while not game_over:
    	#responding to events such as key up and quit button
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                game_over = True

            # setting key controls
            # if up key is pressed move up 4 positions vertically
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -4
            # if up key is released move down 4 positions vertically
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = 4
        #y is vertical position ,here it is decreased or incresed depending on key pressed
        y += y_move

        # image function takes coordinates(position) and image
        #here we are setting background
        image(0,0,background)

        # drawing bird
        image(x, y, img)



        # drawing blocks
        blocks(x_block, y_block, blockWidth, blockHeight1, gap,green)
        # blocks(x_block+400,y_block,blockWidth,blockHeight2,gap)
        # blocks(x_block+800,y_block,blockWidth,blockHeight3,gap)
        #here we are decreasing the x position of block so that the blocks can move towards the bird
        x_block -= block_move

        # loading the score on the screen
        score (current_score,level)

        #if the position of bird hits the upper or lower boundary of the frame -->gameover
        if y > surfaceHeight - imageHeight or y < 0:
            gameOver(current_score)

        # recreating the blocks after the current block disappears
        if x_block < (-1 * blockWidth):
            x_block = surfaceWidth
            blockHeight1 = randint (0, int (surfaceHeight / 1.5))
            # blockHeight2 = randint (0, int (surfaceHeight / 1.5))
            # blockHeight3 = randint (0, int (surfaceHeight / 1.5))

        # crash logic
        # if bird is below the block level
 		#if bird is enters the block region
        if x + imageWidth > x_block:
            print (" bird is below the  upper block region")
            # bird is within the block
            if x < x_block + blockWidth:
                print (" bird is within the block region ")
                # crash condition1
                #if bird hits the upper boundary
                #here +15 is adjustment --->not necessary
                if y < blockHeight1+15:
                    print ("bird crosses upper boundary")
                    if x - imageWidth < blockWidth + x_block:
                        print ("bird crashed into upper boundary")
                        gameOver (current_score)
        #if bird is above the lower block
        if x + imageWidth > x_block:
            print(" bird is above the lower block region")
            if y + imageHeight > blockHeight1 + gap:
            	#crash condition 2
                print(" bird is below the  lower block region")
                if x < x_block + blockWidth:
                    print(" bird crashed into lower boundary")
                    gameOver(current_score)
        
        #score logic  
        # +40 and +i*20 are for adjustment ---not needed
        if x < x_block+40 and x > x_block - block_move+i*20:
           current_score += 1

		

        #difficulty logic
        #when the score increases increase the speed and decrease the gap
        if 20 <= current_score < 40:
            block_move = 8
            if x_block < (-.99 * blockWidth):
                gap = int(imageHeight * 3)
                level = "I"

        if 40 <= current_score < 60:
            block_move = 10
            if x_block < (-.99 * blockWidth):
                gap = int (imageHeight * 2.5)
                level = "II"

        if 60 <= current_score < 100:
            block_move = 11
            if x_block < (-.99 * blockWidth):
                gap = int (imageHeight * 2)
                level = "IV"

        if current_score > 100:
            block_move=12
            level = "V"




        pygame.display.update ()
        clock.tick (60)




# starting the game
gameStart()
main ()
pygame.quit ()
quit ()
