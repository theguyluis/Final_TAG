# Luis Correia - 100143596
# COMP 4983
# Supervisor - Duane Currie

# The user buckyroberts had some examples on github how to use pygame to create a game
# This code has been derived by his exmaple to understand how to use pygame
# link to the specific code is here: 
# https://github.com/buckyroberts/Source-Code-from-Tutorials/blob/master/Pygame/50_PythonGameDevelopment.py


# This is all the libraies needed for the game
import pygame
import time
import random
import csv
import serial
import threading
import socket

pygame.init()

# Create Clock
clock = pygame.time.Clock()

# Dimensions for game screen
display_width = 1279
display_height = 720

# Images needed to run the game
main_menu_img = pygame.image.load(r'Arts/Main_menu.png')
game_mat_img = pygame.image.load(r'Arts/Playmat_for_project.png')
Lose_Screen_img = pygame.image.load(r'Arts/lose_screen.png')

# Creating the window for the game
window = pygame.display.set_mode((display_width,display_height))

# Array for player different sections of the scanners
Prize_Cards = []
Prize_Name = []
Read_Card = []
Prize_Card = []
Active = []
Active_Name = []
Energy = []
Energy_Name = []
Bench = []
benchName =[]
Discard = []
Discard_Name = []
Discard_Active = []
Discard_Bench = []

# Oppenent arrays to store information from socket
OPrize_Cards = []
OPrize_Name = []
ORead_Card = []
OPrize_Card = []
OActive = []
OActive_Name = []
OEnergy = []
OEnergy_Name = []
OBench = []
ObenchName =[]
ODiscard = []
ODiscard_Name = []
ODiscard_Active = []
ODiscard_Bench = []
message_to_send = ""

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

# This will give buttons some actions and color change hovering over it
def button(text,x,y,width,height,inactive_color,active_color,action = None):
    global c, receive_non_stop
    # player's arrays
    global Prize_Cards, Prize_Name,Read_Card,Prize_Card,Active,Active_Name,Energy,Energy_Name,Bench
    global benchName,Discard,Discard_Name,Discard_Active,Discard_Bench
    # opponent arrays
    global OPrize_Cards, OPrize_Name,ORead_Card,OPrize_Card,OActive,OActive_Name,OEnergy,OEnergy_Name
    global OBench,ObenchName,ODiscard,ODiscard_Name,ODiscard_Active,ODiscard_Bench
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
                # c.close()
                receive_non_stop = False
                # clear all arrays
                del Prize_Cards[:]
                del Prize_Name[:]
                del Read_Card[:]
                del Prize_Card[:]
                del Active[:]
                del Active_Name[:]
                del Energy[:]
                del Energy_Name[:]
                del Bench[:]
                del benchName[:]
                del Discard[:]
                del Discard_Name[:]
                del Discard_Active[:]
                del Discard_Bench[:]
                # oppenent arrays
                del OPrize_Cards[:]
                del OPrize_Name[:]
                del ORead_Card[:]
                del OPrize_Card[:]
                del OActive[:]
                del OActive_Name[:]
                del OEnergy[:]
                del OEnergy_Name[:]
                del OBench[:]
                del ObenchName[:]
                del ODiscard[:]
                del ODiscard_Name[:]
                del ODiscard_Active[:]
                del ODiscard_Bench[:]
                c.close()
                #RC.join()
                #SC.join()
                gameIntro()

            #if action == "read_card":

    else:
        pygame.draw.rect(window,inactive_color,(x,y,width,height))
    textToBtn(text,black,x,y,width,height)

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
c = ''      
def socket_Connection():
    receive_non_stop = True
    s = socket.socket()
    print "Socket successfully created"
    port = 12126
    s.bind(('', port))         
    print "socket binded to %s" %(port) 
    s.listen(5)      
    print "socket is listening" 
    global c
    global receive_non_stop, test
    global OPrize_Cards, OPrize_Name,ORead_Card,OPrize_Card,OActive,OActive_Name,OEnergy,OEnergy_Name
    global OBench,ObenchName,ODiscard,ODiscard_Name,ODiscard_Active,ODiscard_Bench
    test = True
    while test == True: 
        # Establish connection with client. 
        c, addr = s.accept()      
        print 'Got connection from', addr 
        while receive_non_stop == True:
            message = c.recv(1000)
            # This will read the line from serial
            Oard_msg = message
            if message == "stop\r\n":
                receive_non_stop = False
                break
            # This will strip the end of the line
            new_Oard = Oard_msg.rstrip('\r\n')
            # This will add the information from the serial line to Read card array
            if new_Oard:
                card_info = (new_Oard.split(':',2))
                Oreader = card_info[0]
                OUID = card_info[1]
                ORead_Card.insert(0,Oreader)
                ORead_Card.insert(1,OUID)
                for i in range(len(PokeC_UID)):
                    if OUID == PokeC_UID[i]:
                        ORead_Card.insert(2,PokeC_Name[i])
                        ORead_Card.insert(3,PokeC_type[i])

            if len(ORead_Card) > 2:
                # Sets up the Active Card to be played
                if ORead_Card[0] == "Reader_0":
                    if ORead_Card[3] == "Monster":
                        OActive.insert(0,ORead_Card[1])
                        OActive_Name.insert(0,ORead_Card[2])
                    if ORead_Card[3] == "Energy":
                        if len(OEnergy) == 0:
                            OEnergy.insert(0,ORead_Card[1])
                        if len(OEnergy_Name) == 0:
                            OEnergy_Name.insert(0,ORead_Card[2])
                        if len(Energy) < 5:
                            if not ORead_Card[1] in OEnergy:
                                OEnergy.append(ORead_Card[1])
                                OEnergy_Name.append(ORead_Card[2])

                    if len(OBench) == 5:
                        print("bench is full")

                    if len(ObenchName) == 5:
                        print("bench name is full")
                # Bench reader
                if ORead_Card[0] == "Reader_1":
                    if len(OBench) == 0:
                        OBench.insert(0,ORead_Card[1])
                    if len(ObenchName) == 0:
                        ObenchName.insert(0,ORead_Card[2])
                    if len(OBench) < 5:
                        if not ORead_Card[1] in OBench:
                            OBench.append(ORead_Card[1])
                            ObenchName.append(ORead_Card[2])

                    if len(OBench) == 5:
                        print("bench is full")

                    if len(ObenchName) == 5:
                        print("bench name is full")
                    
                # Discard reader
                if ORead_Card[0] == "Reader_2":
                    # Checks to see if the UID is the Active and if add it to the Discard array
                    if ORead_Card[1] in OActive:
                        ODiscard.insert(0,ORead_Card[1])
                        ODiscard_Name.insert(0,ORead_Card[2])
                        OActive.remove(ORead_Card[1])
                        OActive_Name.remove(ORead_Card[2])
                    if not ORead_Card[1] in OActive:
                        pass

                    # Check to see if the UID is on the bench and if add it to the Discard array
                    if ORead_Card[1] in OBench:
                        ODiscard.insert(0,ORead_Card[1])
                        ODiscard_Name.insert(0,ORead_Card[2])
                        OBench.remove(ORead_Card[1])
                        ObenchName.remove(ORead_Card[2])

                    if ORead_Card[1] in OEnergy:
                        ODiscard.insert(0,ORead_Card[1])
                        ODiscard_Name.insert(0,ORead_Card[2])
                        OEnergy.remove(ORead_Card[1])
                        OEnergy_Name.remove(ORead_Card[2])
                    # if the card is not on the bench just pass 
                    if not ORead_Card[1] in OBench:
                        pass
                    if ORead_Card[1] in OPrize_Cards:
                        OPrize_Cards.remove(ORead_Card[1])
                        OPrize_Name.remove(ORead_Card[2])
                    if not ORead_Card[1] in OEnergy:
                        pass
        c.close()
        print("Connection is closed")
        break

# This will read in the serial communication to process the cards         
def read_card():
    benchNum = 0
    tmp_name = ""
    global Prize_Cards, Prize_Name,Read_Card,Prize_Card,Active,Active_Name,Energy,Energy_Name,Bench
    global benchName,Discard,Discard_Name,Discard_Active,Discard_Bench
    global c
    while read_cards:
        # This will read the line from serial
        ard_msg = ard.readline()
        c.send(ard_msg)
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
                    Read_Card.insert(3,PokeC_type[i])

        if len(Read_Card) > 2:
            # Sets up the Active Card to be played
            if Read_Card[0] == "Reader_0":
                if Read_Card[3] == "Monster":
                    Active.insert(0,Read_Card[1])
                    Active_Name.insert(0,Read_Card[2])
                if Read_Card[3] == "Energy":
                    if len(Energy) == 0:
                        Energy.insert(0,Read_Card[1])
                    if len(Energy_Name) == 0:
                        Energy_Name.insert(0,Read_Card[2])
                    if len(Energy) < 5:
                        if not Read_Card[1] in Energy:
                            Energy.append(Read_Card[1])
                            Energy_Name.append(Read_Card[2])

                if len(Bench) == 5:
                    print("bench is full")

                if len(benchName) == 5:
                    print("bench name is full")
            # Bench reader
            if Read_Card[0] == "Reader_1":
                if len(Bench) == 0:
                    Bench.insert(0,Read_Card[1])
                if len(benchName) == 0:
                    benchName.insert(0,Read_Card[2])
                if len(Bench) < 5:
                    if not Read_Card[1] in Bench:
                        Bench.append(Read_Card[1])
                        benchName.append(Read_Card[2])

                if len(Bench) == 5:
                    print("bench is full")

                if len(benchName) == 5:
                    print("bench name is full")
                
            # Discard reader
            if Read_Card[0] == "Reader_2":
                # Checks to see if the UID is the Active and if add it to the Discard array
                if Read_Card[1] in Active:
                    Discard.insert(0,Read_Card[1])
                    Discard_Name.insert(0,Read_Card[2])
                    Active.remove(Read_Card[1])
                    Active_Name.remove(Read_Card[2])
                if not Read_Card[1] in Active:
                    pass

                # Check to see if the UID is on the bench and if add it to the Discard array
                if Read_Card[1] in Bench:
                    Discard.insert(0,Read_Card[1])
                    Discard_Name.insert(0,Read_Card[2])
                    Bench.remove(Read_Card[1])
                    benchName.remove(Read_Card[2])

                if Read_Card[1] in Energy:
                    Discard.insert(0,Read_Card[1])
                    Discard_Name.insert(0,Read_Card[2])
                    Energy.remove(Read_Card[1])
                    Energy_Name.remove(Read_Card[2])
                # if the card is not on the bench just pass 
                if not Read_Card[1] in Bench:
                    pass
                if Read_Card[1] in Prize_Cards:
                    Prize_Cards.remove(Read_Card[1])
                    Prize_Name.remove(Read_Card[2])
                if not Read_Card[1] in Energy:
                    pass
                
    clock.tick(1)

# This funciton will read in the prize cards and store it in the prize cards arrays
def read_prize():
    prizeC = 0
    tmp_prize = ""
    global c
    global RC
    while prizeC < 6:
        # This will read the line from serial
        prize_msg = ard.readline()
        if len(prize_msg) > 0:
            c.send(prize_msg)
        # This will strip the end of the line
        newP_ard = prize_msg.rstrip('\r\n')
        # This will add the information from the serial line to Read card array
        if newP_ard:
            card_info = (newP_ard.split(':',2))
            readerP = card_info[0]
            UIDP = card_info[1]
            Prize_Card.insert(0,readerP)
            Prize_Card.insert(1,UIDP)
            for i in range(len(PokeC_UID)):
                if UIDP == PokeC_UID[i]:
                    Prize_Card.insert(2,PokeC_Name[i])

        # this will add prize cards once scanned from the active region reader
        if len(Prize_Card) > 2:
            if Prize_Card[0] == "Reader_0":
                    if len(Prize_Cards) == 0:
                        Prize_Cards.insert(0,Prize_Card[1])
                    if len(Prize_Name) == 0:
                        Prize_Name.insert(0,Prize_Card[2])
                        prizeC += 1
                    if len(Prize_Cards) < 7:
                        if not Prize_Card[1] in Prize_Cards:
                            Prize_Cards.append(Prize_Card[1])
                            Prize_Name.append(Prize_Card[2])
                            #prizeC += 1
                            
                    if len(Prize_Cards) == 6:
                        print("bench is full")

                    if len(Prize_Name) == 6:
                        print("bench name is full")
                        # this will start the read card thread
                        RC.start()
                        break
    clock.tick(1)

# This will trigger once the opponenet loses all their prize cards
def game_loss():
    loss = True
    while loss:
         # checks in the event if the user quits to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # checks in the event if the user presses "q" to quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #displays lose screen image
        window.blit(Lose_Screen_img,(0,0))
        # displays the button which will allow the user to return the main menu
        button("Main Menu",590,600,100,50,green,light_green,action="goToMain")

        pygame.display.update()
        clock.tick(15)

# This will be triggered once the program has been executed (Main Menu)
def gameIntro():
    intro = True
    while intro:
        # checks in the event if the user quits to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # checks in the event if the user presses "c" to start match
                if event.key == pygame.K_c:
                    intro = False
                # checks in the event if the user presses "q" to quit the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #displays main menu image
        window.blit(main_menu_img,(0,0))
        # displays some text to the screen on top of the main menu image
        textToScreen("Welcome to Touch and Go!",green,-270,size="large")
        textToScreen("Please enter the IP address below to connect", white,-230,size="small")
        textToScreen("to the host/join to start a match",white,-210,size="small")
        # displays the buttons which will start the match or quit the game
        button("play",450,600,100,50,green,light_green,action="play")
        button("quit",650,600,100,50,red,light_red,action="quit")

        pygame.display.update()
        clock.tick(15)

def gameLoop():
    global RC,RP,SC,c
    # Current Player arrays
    global Prize_Cards, Prize_Name,Read_Card,Prize_Card,Active,Active_Name,Energy,Energy_Name,Bench
    global benchName,Discard,Discard_Name,Discard_Active,Discard_Bench
    # Current Oppenent arrays
    global OPrize_Cards, OPrize_Name,ORead_Card,OPrize_Card,OActive,OActive_Name,OEnergy,OEnergy_Name
    global OBench,ObenchName,ODiscard,ODiscard_Name,ODiscard_Active,ODiscard_Bench
    # Setting up Thread for reading prize cards
    RP = threading.Thread(target=read_prize)
    RP.daemon=True
    RP.start()
    # Setting up Thread for continous reading cards
    RC = threading.Thread(target=read_card)
    RC.daemon=True
    # Setting up Thread for socket 
    SC = threading.Thread(target=socket_Connection)
    SC.daemon=True
    SC.start()
    gameExit = False
    gameOver = False
    # Used to track once all the prize cards have been scanned
    # to see if the user loses the game when all the prize cards are gone
    Lose_catch = 0
    # width of the small cards
    Card_width = 98
    # height of the small cards
    Card_height = 139
    # y location for the energy cards on the active region
    EA_y = [300,310,320,330,340]
    # x locations for the bench 
    Bench_x = [350,450,550,650,750]
    # x locations for the opponent bench 
    OBench_x = [250,350,450,550,650]
    # x locations for the prize cards
    Prize_x = [90,190,90,190,90,190]
    # y locations for the prize cards
    Prize_y = [280,280,420,420,560,560]
    # arrays to store extra information for placement on the mat
    Bench_Place =[]
    OBench_Place =[]
    Prize_Place = []

    while not gameExit:
        # checks in the event if the user quits to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit= True
                gameOver = False
            # checks in the event if the user presses "q" to quit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameExit = True
                    gameOver = False
        # mat to the screen
        window.blit(game_mat_img,(0,0))
        #creates the cursor for the game loop 
        GLcur = pygame.mouse.get_pos()
        # displays the prize cards on the mat
        if len(Prize_Cards) > 0:
            for i in range(len(Prize_Name)):
                prizeCardToPlay = "pokeCards/%s_small.png" %(Prize_Name[i])
                playPrize = pygame.image.load(prizeCardToPlay)
                Prize_Place.insert(i,playPrize)
                window.blit(Prize_Place[i],(Prize_x[i],Prize_y[i]))

        # This will allow to show a bigger card over to the side if it is hovering
        if len(Prize_Name) > 0:
            for i in range(len(Prize_Name)):
                if Prize_x[i] + Card_width > GLcur[0] > Prize_x[i] and Prize_y[i] + Card_height > GLcur[1] > Prize_y[i]:
                    PV = "pokeCards/%s.png" %(Prize_Name[i])
                    playPV = pygame.image.load(PV)
                    window.blit(playPV,(1020,150))

        # triggers to lose catch to know the user has all prize cards scanned
        if len(Prize_Cards) == 6:
            Lose_catch = 1

        # displays the energy cards on the active bench 
        if len(Energy) > 0:
            for i in range(len(Energy_Name)):
                eaCardToPlay = "pokeCards/%s_small.png" %(Energy_Name[0])
                playEA = pygame.image.load(eaCardToPlay)
                window.blit(playEA,(550,EA_y[i]))

        # This will allow to show a bigger card over to the side if it is hovering
        if len(Energy_Name) > 0:
            if 550 + Card_width > GLcur[0] > 550 and EA_y[i] + 50 > GLcur[1] > EA_y[i]:
                EV = "pokeCards/%s.png" %(Energy_Name[0])
                playEV = pygame.image.load(EV)
                window.blit(playEV,(1020,150))
        
        # Player side to display cards in this sections
        if len(Active) > 0:
            activeCardToPlay = "pokeCards/%s_small.png" %(Active_Name[0])
            playActive = pygame.image.load(activeCardToPlay)
            window.blit(playActive,(550,350))
        # This will allow to show a bigger card over to the side if it is hovering
        if len(Active_Name) > 0:
            if 550 + Card_width > GLcur[0] > 550 and 350 + Card_height > GLcur[1] > 350:
                AV = "pokeCards/%s.png" %(Active_Name[0])
                playAV = pygame.image.load(AV)
                window.blit(playAV,(1020,150))

        # Oppoenent side to display cards in this section
        if len(OActive) > 0:
            OactiveCardToPlay = "pokeCards/%s_small.png" %(OActive_Name[0])
            OplayActive = pygame.image.load(OactiveCardToPlay)
            window.blit(OplayActive,(450,220))
        # This will allow to show a bigger card over to the side if it is hovering
        if len(OActive_Name) > 0:
            if 450 + Card_width > GLcur[0] > 450 and 220 + Card_height > GLcur[1] > 220:
                OAV = "pokeCards/%s.png" %(OActive_Name[0])
                OplayAV = pygame.image.load(OAV)
                window.blit(OplayAV,(1020,150))

        # Player side to display cards in this sections
        if len(Bench) > 0:
            for i in range(len(benchName)):
                benchCardToPlay = "pokeCards/%s_small.png" %(benchName[i])
                playBench = pygame.image.load(benchCardToPlay)
                Bench_Place.insert(i,playBench)
                window.blit(Bench_Place[i],(Bench_x[i],550))
        # This will allow to show a bigger card over to the side if it is hovering
        if len(benchName) > 0:
            for i in range(len(benchName)):
                if Bench_x[i] + Card_width > GLcur[0] > Bench_x[i] and 550 + Card_height > GLcur[1] > 550:
                    BV = "pokeCards/%s.png" %(benchName[i])
                    playBV = pygame.image.load(BV)
                    window.blit(playBV,(1020,150))

        # Oppoenent side to display cards in this section
        if len(OBench) > 0:
            for i in range(len(ObenchName)):
                ObenchCardToPlay = "pokeCards/%s_small.png" %(ObenchName[i])
                OplayBench = pygame.image.load(ObenchCardToPlay)
                OBench_Place.insert(i,OplayBench)
                window.blit(OBench_Place[i],(OBench_x[i],30))
        # This will allow to show a bigger card over to the side if it is hovering
        if len(ObenchName) > 0:
            for i in range(len(ObenchName)):
                if Bench_x[i] + Card_width > GLcur[0] > Bench_x[i] and 550 + Card_height > GLcur[1] > 550:
                    OBV = "pokeCards/%s.png" %(ObenchName[i])
                    OplayBV = pygame.image.load(OBV)
                    window.blit(OplayBV,(1020,150))
        # displays the discard card
        if len(Discard_Name) > 0:
            discardCardToPlay = "pokeCards/%s_small.png" %(Discard_Name[0])
            playDiscard = pygame.image.load(discardCardToPlay)
            window.blit(playDiscard,(915,550))
        #Oppenent discard
        if len(ODiscard_Name) > 0:
                OdiscardCardToPlay = "pokeCards/%s_small.png" %(ODiscard_Name[0])
                OplayDiscard = pygame.image.load(OdiscardCardToPlay)
                window.blit(OplayDiscard,(90,30))
        # This will allow to show a bigger card over to the side if it is hovering
        if len(ODiscard_Name) > 0:
            if 90 + Card_width > GLcur[0] > 90 and 30 + Card_height > GLcur[1] > 30:
                ODV = "pokeCards/%s.png" %(ODiscard_Name[0])
                OplayDV = pygame.image.load(ODV)
                window.blit(OplayDV,(1020,150))
        
        # Once player loses all prize cards it will delete all the arrays when going to 
        # lose screen            
        if Lose_catch == 1:
            if len(Prize_Cards) == 0:
                gameExit= True
                # clear all arrays
                del Prize_Cards[:]
                del Prize_Name[:]
                del Read_Card[:]
                del Prize_Card[:]
                del Active[:]
                del Active_Name[:]
                del Energy[:]
                del Energy_Name[:]
                del Bench[:]
                del benchName[:]
                del Discard[:]
                del Discard_Name[:]
                del Discard_Active[:]
                del Discard_Bench[:]
                # clear all opponent arrays
                del OPrize_Cards[:]
                del OPrize_Name[:]
                del ORead_Card[:]
                del OPrize_Card[:]
                del OActive[:]
                del OActive_Name[:]
                del OEnergy[:]
                del OEnergy_Name[:]
                del OBench[:]
                del ObenchName[:]
                del ODiscard[:]
                del ODiscard_Name[:]
                del ODiscard_Active[:]
                del ODiscard_Bench[:]
                game_loss()
        # Surrender button that is placed on the screen to go back to main menu
        button("Surrender", 1095,50,100,50,red,light_red,action="goToMain")
        pygame.display.update()
        clock.tick(15)
    pygame.quit()
    quit()
gameIntro()
gameLoop()
