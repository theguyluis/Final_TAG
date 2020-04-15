# This is all the libraies needed for the game
import pygame
import time
import random
import csv
import serial
import threading

pygame.init()

# Create Clock
clock = pygame.time.Clock()

# Dimensions for game screen
display_width = 1279
display_height = 720

# Images needed to run the game
main_menu_img = pygame.image.load(r'Arts/Main_menu.png')
game_mat_img = pygame.image.load(r'Arts/Playmat_for_project.png')

# Creating the window for the game
window = pygame.display.set_mode((display_width,display_height))

# Array for different sections of the scanners
Prize_Cards = []
Prize_Name = []
Read_Card = []
Active = []
Active_Name = []
Bench = []
benchName =[]
Discard = []
Discard_Name = []
Discard_Active = []
Discard_AName = []
Discard_Bench = []
Discard_BName = []
# Flag to stop the thread for reading cards
read_cards = True
prize_cards = True
# Serial Port connection *Keep in mind each person may need to change this*
port = '/dev/tty.usbmodem141301'
ard = serial.Serial(port,9600,timeout=5)

# Colors needed for items to window
white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
light_red = (255,0,0)
yellow = (200,0,0)
light_yellow = (255,255,0)
green = (35,175,75)
light_green = (0,255,0)
gray = (166,166,166)
light_gray = (200,200,200)

# Font Size options needed for btns and test to screen
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)

# Set the caption of the window
pygame.display.set_caption('Touch and Go')

# Function to read all the items in the CSV file 
def readMyFile(filename):
    PokeC_UID = []
    PokeC_Type = []
    PokeC_Name = []
    PokeC_HP = []
    PokeC_Weakness = []
    PokeC_Resistance = []
    PokeC_Retreat = []

    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            PokeC_UID.append(row[0])
            PokeC_Type.append(row[1])
            PokeC_Name.append(row[2])
            PokeC_HP.append(row[3])
            PokeC_Weakness.append(row[4])
            PokeC_Resistance.append(row[5])
            PokeC_Retreat.append(row[6])
    return PokeC_UID,PokeC_Type,PokeC_Name,PokeC_HP,PokeC_Weakness,PokeC_Resistance,PokeC_Retreat

# This will call the function to read the file once and add everything to the array's 
PokeC_UID,PokeC_type,PokeC_Name,PokeC_HP,PokeC_Weakness,PokeC_Resistance,PokeC_Retreat = readMyFile('test.csv')          

def read_card():
    # if read_cards == True:
    #     print("read_cards = True")
    # if read_cards == False:
    #     print("read_cards = False")
    benchNum = 0
    tmp_name = ""
    #Bench_x = [350,450,550,650,750]
    #j = 0
    while read_cards:
        # This will read the line from serial
        ard_msg = ard.readline()
        # This will strip the end of the line
        new_ard = ard_msg.rstrip('\r\n')
        # This will add the information from the serial line to Read card array
        if new_ard:
            card_info = (new_ard.split(':',2))
            reader = card_info[0]
            UID = card_info[1]
            Read_Card.insert(0,reader)
            Read_Card.insert(1,UID)
            for i in range(len(PokeC_UID)):
                if UID == PokeC_UID[i]:
                    Read_Card.insert(2,PokeC_Name[i])

        if len(Read_Card) > 2:
            # Sets up the Active Card to be played
            if Read_Card[0] == "Reader_0":
                Active.insert(0,Read_Card[1])
                Active_Name.insert(0,Read_Card[2])
            
            # Bench reader
            if Read_Card[0] == "Reader_1":
                if len(Bench) == 0:
                    Bench.insert(0,Read_Card[1])
                if len(benchName) == 0:
                    benchName.insert(0,Read_Card[2])
                if len(Bench) < 4:
                    if not Read_Card[1] in Bench:
                        Bench.append(Read_Card[1])
                        benchName.append(Read_Card[2])

                # if len(benchName) < 5:
                #     if not Read_Card[2] in benchName:
                #         benchName.append(Read_Card[2])

                if len(Bench) == 5:
                    print("bench is full")

                if len(benchName) == 5:
                    print("bench name is full")
                
            # Discard reader
            if Read_Card[0] == "Reader_2":
                if (len(Active)) > 0:
                    if Read_Card[1] == Active[i]:
                        Discard.insert(0,Active[i])
                        Discard_Name.insert(0,Active_Name[i])
                        del Active[i]
                        del Active_Name[i]
                if (len(Bench)) > 0:
                    for i in range(len(Bench)):
                        if Read_Card[1] == Bench[i]:
                            Discard.insert(0,Bench[i])
                            del Bench[i]
                for i in range(len(benchName)):
                    if len(benchName) < 5:
                        if Read_Card[2] == benchName[i]:
                            Discard_Name.insert(0,benchName[i])
                            del benchName[i]
                            
    clock.tick(1)

# Setting up Thread for continous reading cards
thread = threading.Thread(target=read_card)
thread.daemon=True
def read_prize():
    prizeC = 0
    tmp_prize = ""
    while prizeC < 7:
        # This will read the line from serial
        print("read prize")
        prize_msg = ard.readline()
        # This will strip the end of the line
        newP_ard = prize_msg.rstrip('\r\n')
        # This will add the information from the serial line to Read card array
        if newP_ard:
            card_info = (newP_ard.split(':',2))
            readerP = card_info[0]
            UIDP = card_info[1]
            Read_Card.insert(0,readerP)
            Read_Card.insert(1,UIDP)
            for i in range(len(PokeC_UID)):
                if UIDP == PokeC_UID[i]:
                    Read_Card.insert(2,PokeC_Name[i])
        if len(Read_Card) > 2:
            if Read_Card[0] == "Reader_0":
                    if len(Prize_Cards) == 0:
                        Prize_Cards.insert(0,Read_Card[1])
                    if len(Prize_Name) == 0:
                        Prize_Name.insert(0,Read_Card[2])
                    if len(Prize_Cards) < 7:
                        if not Read_Card[1] in Prize_Cards:
                            Prize_Cards.append(Read_Card[1])
                            Prize_Name.append(Read_Card[2])
                            print(len(Prize_Cards))

                    # if len(Prize_Name) < 6:
                    #     if not Read_Card[2] in Prize_Name:
                            

                    if len(Prize_Cards) == 5:
                        print("bench is full")

                    if len(Prize_Name) == 6:
                        print("bench name is full")
                        thread.start()
RP = threading.Thread(target=read_prize)
RP.daemon=True
RP.start()
#thread.start()
# Function for setting up text objects
def textObjects(text, color, size = "small"):
    if size == "small":
        textSurface = smallfont.render(text,True,color)
    if size == "medium":
        textSurface = medfont.render(text,True,color)
    if size == "large":
        textSurface = largefont.render(text,True,color)
    
    return textSurface, textSurface.get_rect()

# This will create the btn object to be placed on screen
def textToBtn(msg,color,btnX,btnY,btnW,btnH,size = "small"):
    textSurf, textRect = textObjects(msg,color,size)
    textRect.center = ((btnX + (btnW/2)), btnY + (btnH/2))
    window.blit(textSurf,textRect)

# This will create the text to screen object
def textToScreen(msg,color,yDisplace = 0,size = "small"):
    textSurf, textRect = textObjects(msg,color,size)
    textRect.center = (int(display_width/2), int(display_height/2) + yDisplace)
    window.blit(textSurf,textRect)

# This will give buttons some actions and color change hovering ober it
def button(text,x,y,width,height,inactive_color,active_color,action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(window,active_color,(x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()

            if action == "play":
                gameLoop()

            if action == "goToMain":
                gameIntro()

            #if action == "read_card":

    else:
        pygame.draw.rect(window,inactive_color,(x,y,width,height))
    textToBtn(text,black,x,y,width,height)

def gameIntro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        window.blit(main_menu_img,(0,0))
        textToScreen("Welcome to Touch and Go!",green,-270,size="large")
        textToScreen("Please enter the IP address below to connect", white,-230,size="small")
        textToScreen("to the host/join to start a match",white,-210,size="small")

        button("play",450,600,100,50,green,light_green,action="play")
        button("quit",650,600,100,50,red,light_red,action="quit")

        pygame.display.update()
        clock.tick(15)

def gameLoop():
    gameExit = False
    gameOver = False
    #RP.start()
    Bench_x = [350,450,550,650,750]
    Prize_x = [90,190,90,190,90,190]
    Prize_y = [280,280,420,420,560,560]
    Bench_Place =[]
    Prize_Place = []
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit= True
                gameOver = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameExit = True
                    gameOver = False
        # mat to the screen
        window.blit(game_mat_img,(0,0))

        if len(Prize_Cards) > 0:
            for i in range(len(Prize_Name)):
                #print(Prize_Name[i])
                prizeCardToPlay = "pokeCards/%s_small.png" %(Prize_Name[i])
                playPrize = pygame.image.load(prizeCardToPlay)
                Prize_Place.insert(i,playPrize)
                window.blit(Prize_Place[i],(Prize_x[i],Prize_y[i]))


        if len(Active) > 0:
            activeCardToPlay = "pokeCards/%s_small.png" %(Active_Name[0])
            playActive = pygame.image.load(activeCardToPlay)
            window.blit(playActive,(550,350))
        
        if len(Bench) > 0:
            for i in range(len(benchName)):
                benchCardToPlay = "pokeCards/%s_small.png" %(benchName[i])
                playBench = pygame.image.load(benchCardToPlay)
                Bench_Place.insert(i,playBench)
                window.blit(Bench_Place[i],(Bench_x[i],550))

        if len(Discard_Name) > 0:
            discardCardToPlay = "pokeCards/%s_small.png" %(Discard_Name[0])
            playDiscard = pygame.image.load(discardCardToPlay)
            window.blit(playDiscard,(915,550))
            # for i in range(len(Active)):
            #     if Discard[0] in Active:
            #         del Active[i]
            #         del Active_Name[i]

            # for i in range(len(Bench)):
            #     if Bench[i] == Discard[0]:
                    
        
        button("Surrender", 1100,50,100,50,red,light_red,action="goToMain")
        button("read card",1100,200,100,50,gray,light_gray,action="read_card")
        pygame.display.update()
        clock.tick(15)
    pygame.quit()
    quit()
gameIntro()
gameLoop()
