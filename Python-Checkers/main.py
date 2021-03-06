import turtle
import random
import time
import P1
import P2
import copy

SLOW_DOWN=False
GRAPHICS=True
STEP=False
QUIT_GAME = False

def drawSquare(t,color):
    t.color("black")
    t.fillcolor(color)
    t.begin_fill()
    for num in range(4):
        t.forward(1)
        t.right(90)
    t.end_fill()

def drawRow(t,color1,color2):
    for i in range(4):
        drawSquare(t,color1)
        t.forward(1)
        drawSquare(t,color2)
        t.forward(1)

def drawChecker(t,row,col,color,kingFlag):
    y=row-1
    x=col+.5
    t.color("dimgray",color)
    t.up()
    t.goto(x,y)
    t.down()
    t.begin_fill()
    t.circle(.5)
    t.end_fill()
    #draw the concentric circles in the checker
    for i in range(1,5):
        t.up()
        t.goto(x,y+(i*.1))
        t.down()
        if i==4 and kingFlag:
            t.begin_fill()
            t.color("yellow")
        t.circle(.5-(i*.1))
        if i==4 and kingFlag:
            t.end_fill()
            t.color("dimgray")

def drawBoard(bob):
    c1="gray"
    c2="red"
    for x in range(8):
        drawRow(bob,c1,c2)
        bob.up()
        bob.goto(0,x+1)
        bob.down()
        #switch c1 and c2 colors
        temp=c1
        c1=c2
        c2=temp
    drawLabels(bob)

def drawLabels(t):
    offset=0
    t.color("white")
    for line in "ABCDEFGH":
        for cell in range(0,8,2):
            t.up()
            t.goto(offset+cell+.82,ord(line)-65+.02)
            t.down()
            t.write(line+str(cell+offset))
        if offset==0:
            offset=1
        else:
            offset=0
    t.color("black")

def drawLabel(t,row,col):
    t.color("white")
    t.up()
    t.goto(col+.82,row+.02)
    t.down()
    t.write(chr(row+65)+str(col))
    t.color("black")

def printBoard(board):
    for row in range(8):
        for col in range(8):
            print("",board[row][col],end="")
        print()
    print()

def populateBoardsWithCheckers(t,board):
    offset=0
    if GRAPHICS:t.color("red")
    for row in range(0,3):
        for col  in range(0,8,2):
            if GRAPHICS:drawChecker(t,row,col+offset,"red",False)
            board[row][col+offset]="r"
        if offset==0:
            offset=1
        else:
            offset=0
    offset=1
    if GRAPHICS:t.color("black")
    for row in range(5,8):
        for col in range(0,8,2):
            if GRAPHICS:drawChecker(t,row,col+offset,"black",False)
            board[row][col+offset]="b"
        if offset==1:
            offset=0
        else:
            offset=1

def listValidMoves(board,player):
    possibleMoves=[]
    validRange=[0,1,2,3,4,5,6,7] #list(range(8))
    if player=="b":
        playerTokens=["b","B"]
        moveRowInc=-1
    else:
        playerTokens=["r","R"]
        moveRowInc=1
    kingTokens=["B","R"]
    for row in range(8): #For every row
        for col in range(8):  #For every square in a row
            if board[row][col] in playerTokens: #If the board contains either a regular or king checker of the given player
                if board[row][col] not in kingTokens: #if checker is NOT a king
                    for colInc in [-1,1]: #for each diagonal square in the correct row direction
                        if row+moveRowInc in validRange and col+colInc in validRange and board[row+moveRowInc][col+colInc] =='e':
                            possibleMoves.append(chr(row+65)+str(col)+":"+chr(row+65+moveRowInc)+str(col+colInc))
                else:  #checker is a king
                    for rowInc in [-1,1]: #for each row direction (forward and backward)
                        for colInc in [-1,1]: #for each diagonal square in each row direction
                            if row+rowInc in validRange and col+colInc in validRange and board[row+rowInc][col+colInc] =='e':
                                possibleMoves.append(chr(row+65)+str(col)+":"+chr(row+65+rowInc)+str(col+colInc))              
    return possibleMoves

def listSingleJumps(board,player):
    possibleSingleJumps=[]
    validRange=[0,1,2,3,4,5,6,7] #list(range(8))
    if player=="b":
        playerTokens=["b","B"]
        rowInc=-1
        enemyTokens=["r","R"]
    else:
        playerTokens=["r","R"]
        rowInc=1
        enemyTokens=["b","B"]
    kingTokens=["B","R"]
    for row in range(8):
        for col in range(8):
            if board[row][col] in playerTokens:
                if board[row][col] not in kingTokens:  #if checker is NOT a king
                    for colInc in [-1,1]:
                        if row+rowInc in validRange and col+colInc in validRange and board[row+rowInc][col+colInc] in enemyTokens:                        
                            colJumpInc=2 * colInc
                            rowJumpInc=2 * rowInc
                            if row+rowJumpInc in validRange and col + colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e":
                                possibleSingleJumps.append(chr(row+65)+str(col)+":"+chr(row+65+rowJumpInc)+str(col+colJumpInc))
                else: #checker is a king
                    for rowIncs in [-1,1]: #for each row direction (forward and backward)
                        for colInc in [-1,1]:
                            if row+rowIncs in validRange and col+colInc in validRange and board[row+rowIncs][col+colInc] in enemyTokens:                        
                                colJumpInc=2 * colInc
                                rowJumpInc=2 * rowIncs
                                if row+rowJumpInc in validRange and col + colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e":
                                    possibleSingleJumps.append(chr(row+65)+str(col)+":"+chr(row+65+rowJumpInc)+str(col+colJumpInc))
    return possibleSingleJumps

def listMultipleJumps(board,player,jumpsList):
    newJumps=expandJumps(board,player,jumpsList)
    while newJumps != jumpsList:
        jumpsList=newJumps[:]
        newJumps=expandJumps(board,player,jumpsList)
    return newJumps


def expandJumps(board,player,oldJumps):
    INCs=[1,-1]
    VALID_RANGE=[0,1,2,3,4,5,6,7]
    if player=="b":
        playerTokens=["b","B"]
        rowInc=-1
        opponentTokens=["r","R"]
    else:
        playerTokens=["r","R"]
        rowInc=1
        opponentTokens=["b","B"]
    newJumps=[]
    for oldJump in oldJumps:
        row=ord(oldJump[-2])-65
        col=int(oldJump[-1])
        newJumps.append(oldJump)
        startRow=ord(oldJump[0])-65
        startCol=int(oldJump[1])
        if board[startRow][startCol] not in ["R","B"]: #not a king
            for colInc in INCs:
                jumprow=row+rowInc
                jumpcol=col+colInc
                torow=row+2*rowInc
                tocol=col+2*colInc
                if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                and board[jumprow][jumpcol] in opponentTokens and board[torow][tocol]=='e':
                    newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                    if oldJump in newJumps:
                        newJumps.remove(oldJump)
        else: #is a king
            for colInc in INCs:
                for newRowInc in INCs:
                    jumprow=row+newRowInc
                    jumpcol=col+colInc
                    torow=row+2*newRowInc
                    tocol=col+2*colInc
                    if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                    and board[jumprow][jumpcol] in opponentTokens and (board[torow][tocol]=='e' or oldJump[0:2]==chr(torow+65)+str(tocol)) \
                    and ((oldJump[-2:]+":"+chr(torow+65)+str(tocol)) not in oldJump) and ((chr(torow+65)+str(tocol)+':'+oldJump[-2:] not in oldJump)) and (chr(torow+65)+str(tocol)!=oldJump[-5:-3]):
                        newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                        if oldJump in newJumps:
                            newJumps.remove(oldJump)
    return newJumps          
               
def swapPlayer(player):
    if player=="b":
        player="r"
        playerColor="red"
    else:
        player="b"
        playerColor="black"
    return player,playerColor

def setupGame(inFileName):
    #Set up graphics for game
    if GRAPHICS:
        wn=turtle.Screen()
        wn.setworldcoordinates(-2,9,10,-2)
        bob=turtle.Turtle()
        bob.hideturtle()
        wn.tracer(False)
        drawBoard(bob)
    #Set up logical and graphical checkers
    row=["e","e","e","e","e","e","e","e"]
    board=[]
    for i in range(8):
        board.append(row[:])
    if inFileName == "":
        if GRAPHICS:
            populateBoardsWithCheckers(bob,board)
        else:
            populateBoardsWithCheckers(None,board)
        if random.randint(0,1)==1:
            player="b"
        else:
            player="r"
    else:
        inFile=open(inFileName,'r')
        for rowIndex in range(8):
            line=inFile.readline()[:-1]
            for colIndex in range(8):
                if line[colIndex] in ["r","b","R","B"]:
                    board[rowIndex][colIndex]=line[colIndex]
                    if line[colIndex] in ["r","R"]:
                        if GRAPHICS:drawChecker(bob,rowIndex,colIndex,"red",line[colIndex]=="R")
                    else: #black checker
                        if GRAPHICS:drawChecker(bob,rowIndex,colIndex,"black",line[colIndex]=="B")
        player=inFile.readline()[0]
        inFile.close()
    #printBoard(board)
    if GRAPHICS:
        wn.tracer(True)
        return wn,bob,board,player
    else:
        return None,None,board,player
    
def parseMove(move):
    FROM=move[0:2]
    FROMRow=ord(FROM[0])-65
    FROMCol=int(FROM[1])
    TO=move[3:5]
    TORow=ord(TO[0])-65
    TOCol=int(TO[1])
    return FROMRow,FROMCol,TORow,TOCol

def removeCheckerGraphicalAndLogical(bob,FROMCol,FROMRow,board):
    if GRAPHICS:
        bob.up()
        bob.goto(FROMCol,FROMRow)
        bob.down()
        drawSquare(bob,"gray") #empty the graphical square
        drawLabel(bob,FROMRow,FROMCol) #relabel the emptied square
    playerBoardToken=board[FROMRow][FROMCol] #copy the player token from the logical board, could be "b" or "B" or "r" or "R"
    board[FROMRow][FROMCol]='e' #set the logical board location to empty
    return playerBoardToken

def placeCheckerGraphicalAndLogical(bob,TOCol,TORow,board,playerToken):
    #Logical board update first
    if playerToken == "r" and TORow==7:  #if a kinging move for red
        board[TORow][TOCol]=playerToken.upper()
    elif playerToken == "b" and TORow==0: #if a kinging move for black
        board[TORow][TOCol]=playerToken.upper()
    else: #all non-kinging moves place checker in logical board
        board[TORow][TOCol]=playerToken
    #Now graphical board update
    if GRAPHICS:
        if board[TORow][TOCol] =="b":
            drawChecker(bob,TORow,TOCol,"black",False)
        elif board[TORow][TOCol] =="B":
            drawChecker(bob,TORow,TOCol,"black",True) #True is King
        elif board[TORow][TOCol] =="r":
            drawChecker(bob,TORow,TOCol,"red",False)
        elif board[TORow][TOCol] =="R": #could have used else, but elif for reading clarity
            drawChecker(bob,TORow,TOCol,"red",True) #True is King

def win(board):
    rmove=listValidMoves(board,"r")
    rjump=listSingleJumps(board,"r")
    rjump=listMultipleJumps(board,"r",rjump)
    bmove=listValidMoves(board,"b")
    bjump=listSingleJumps(board,"b")
    bjump=listMultipleJumps(board,"b",bjump)
    if len(rmove)==0 and len(rjump)==0:
        return [True,"black"]
    if len(bmove)==0 and len(bjump)==0:
        return [True,"red"]
    return [False,""]

def saveGame(fileName,board,player):
    outFile=open(fileName,'w')
    outLine=""
    for row in board:
        for ch in row:
            outLine+=ch
        outFile.write(outLine+"\n")
        outLine=""
    outFile.write(player)
    outFile.close()
    print("Game file saved to",fileName)         

def checkersMain(inFileName,redWinCount,blackWinCount):
    wn,bob,board,player=setupGame(inFileName)
    gameOver=False
    if player=="b":
        move = P1.getValidMove(copy.deepcopy(board),player) #get the first move
    else:
        move = P2.getValidMove(copy.deepcopy(board),player) #get the first move
    while move.lower() != "quit" and not gameOver:   #Start alternate play
        if player=="b":
            playerColor="black"
        else:
            playerColor="red"
        if GRAPHICS:wn.tracer(False)
        if STEP:input("Press return to watch the selected move for "+playerColor+" ")
        FROMRow,FROMCol,TORow,TOCol=parseMove(move) #parse move into locations
        if abs(FROMRow-TORow)==1: #move, not a jump
            if SLOW_DOWN: time.sleep(1)
            playerToken=board[FROMRow][FROMCol] #save the player form current location (regular checker or king)
            removeCheckerGraphicalAndLogical(bob,FROMCol,FROMRow,board) #remove the checker to be moved
            if SLOW_DOWN: time.sleep(.5)
            placeCheckerGraphicalAndLogical(bob,TOCol,TORow,board,playerToken) #place the moved checker in its new location
        else: #jump, not a move
            reps=move.count(":")
            for i in range(reps):
                FROMRow,FROMCol,TORow,TOCol=parseMove(move)
                playerToken=board[FROMRow][FROMCol] #save the player form current location (regular checker or king)
                if GRAPHICS:wn.tracer(False)
                if SLOW_DOWN:
                    time.sleep(1)
                removeCheckerGraphicalAndLogical(bob,FROMCol,FROMRow,board) #remove the checker to be moved
                if SLOW_DOWN:
                    time.sleep(.5)
                placeCheckerGraphicalAndLogical(bob,TOCol,TORow,board,playerToken) #place the jumping checker in its new location
                if SLOW_DOWN:
                    wn.tracer(True)
                    time.sleep(1)
                    wn.tracer(False)
                removeCheckerGraphicalAndLogical(bob,(FROMCol+TOCol)//2,(FROMRow+TORow)//2,board) #remove the jumped checker
                if SLOW_DOWN:
                    time.sleep(.5)
                if GRAPHICS:wn.tracer(True)
                move=move[3:]
        if GRAPHICS:wn.tracer(True)
        #printBoard(board)
        player,playerColor=swapPlayer(player)
        gameOver,winningPlayer=win(board)
        if not gameOver:
            if player=="b":
                start=time.time()
                move = P1.getValidMove(copy.deepcopy(board),player) #get the first move
                stop=time.time()
            else:
                start=time.time()
                move = P2.getValidMove(copy.deepcopy(board),player) #get the first move
                stop=time.time()
        #if stop-start>1.0:
            #print("Match forfeited by",PlayerColor)
            #return redWinCount,blackWinCount        
    if move.lower() != "quit":
        #print(winningPlayer +" won the game in a smashing victory!")
        if winningPlayer=="red":
            redWinCount+=1
        else:
            blackWinCount+=1
        return redWinCount,blackWinCount
    else:
        fileName=input("Enter a file name to save the current state of the game, or just hit enter to quit without saving the game => ")
        if fileName != "":
            saveGame(fileName,board,player)
        global QUIT_GAME
        QUIT_GAME = True
        return redWinCount,blackWinCount




#----------------Testing-----------------------
blackWinCount=0
totalGames=10
redWinCount=0

for i in range(totalGames):
    redWinCount,blackWinCount=checkersMain("",redWinCount,blackWinCount)
    if QUIT_GAME:
        break
    print(redWinCount,blackWinCount)
print("Red wins =",redWinCount,"    Black wins =",blackWinCount)
print("%5.2f%% %5.2f%%" %((redWinCount/totalGames*100),(blackWinCount/totalGames*100)))

#checkersMain("",redWinCount,blackWinCount)


#MP13 (see #14 - #17, everything else is just extra... extra credit?)

#---Heuristic #14: Take a sacrificing move ---
#checkersMain("tests/HeuristicsTest - Sacrifices.txt",redWinCount,blackWinCount)
    #Move either H3:G4 or H3:G2 to see that it will always choose the sacrifice.
    #It sees that it will gain material and it makes the move.
    
#checkersMain("tests/HeuristicsTest - Sacrifices2.txt",redWinCount,blackWinCount)
    #The sacrifice functionality also works for "unblocking" a checker.
    #Move H7:G6 to see red deviously unblock its own piece as a sacrificing move.

#checkersMain("tests/HeuristicsTest - Sacrifices3.txt",redWinCount,blackWinCount)
    #Move either H3:G2 or H3:G4. Notice how red chooses not just any sacrifice, but the best one (C6:D5).
    #Move the black king again to see another sacrifice.



#---Heuristic #15: Find and take tradeoff moves when ahead or when no safe moves ---
#checkersMain("tests/HeuristicsTest - Tradeoffs.txt",redWinCount,blackWinCount)
    #As you can see, red is up in material.
    #Move B7:C6 to see red force a crazy tradeoff.
    #It'll set up a double jump tradeoff (because I have kings as being worth 2 checkers)
    #Then move E0:D1 (only move) to see red force another tradeoff to win.

#checkersMain("tests/HeuristicsTest - Tradeoffs2.txt",redWinCount,blackWinCount)
    #This example shows how the automatic player "looks ahead" 4 moves to see
    #if it's a sac move (meaning it gains material), or if it will be jumped back at the end.
    #Move H1:G0 to see it happen. It recognizes it as a tradeoff.



#---Heuristic #16: take best option when no safe moves (instead of random choice) ---
#checkersMain("tests/HeuristicsTest - BestRemainingMoves.txt",redWinCount,blackWinCount)
    #Move C6:D7 to fully block in the red king.
    #Notice how red, when presented with no safe moves, will not give up its king.

#checkersMain("tests/HeuristicsTest - BestRemainingMoves2.txt",redWinCount,blackWinCount)
    #Move H5:G4. Once again, red has no safe option.
    #In response, red refuses to allow a double jump with either E2:F1 or E2:F3.
    #It chooses D7:E6, which gives up only one piece, and hopefully frees up some future moves.



#---Heuristic #17: take safe jumps over "unsafe" ones ---
#checkersMain("tests/HeuristicsTest - SafeJumps.txt",redWinCount,blackWinCount)
    #Move the black king in the bottom-left corner
    #Notice how red chooses the "safe" jump (C0:E2) over the jump that results in being jumped back.




#End MP13, extra stuff below


#---Heuristic #18: take best jumps (kind of a rewrite of former heuristics, so I'd call it a bonus) ---
#checkersMain("tests/HeuristicsTest - TakeBestJump.txt",redWinCount,blackWinCount)
    #Move F7:E6, notice how red always chooses H7:F5:D7 since it gains most material (again, kings being worth 2).
    #Then move H1:G2, notice the jump (instead of jumping the black king).
    #Then B5:C6



#---Heuristic #19: Have kings do "encroaching" moves ---
#checkersMain("tests/HeuristicsTest - Encroach.txt",redWinCount,blackWinCount)
    #Move the black checkers around. Watch how the red king intentionally moves toward them.
    #But it still keeps enough distance to always be safe.
    #I imagine this to be more of an endgame thing.



#---Heuristic #20: When 1 or 2 enemy checkers left, find and take trapping moves ---
#checkersMain("tests/HeuristicsTest - LastTrap.txt",redWinCount,blackWinCount)
    #Move black king into the top left corner or into a board edge.
    #Red king follows closely and tries to find a trapping move.
    #For example, move black king into A0. Red should follow and move into C0, C2, or A2.



#---Heuristic #21: Avoid enemy sacs ---
#checkersMain("tests/HeuristicsTest - AvoidEnemySacs.txt",redWinCount,blackWinCount)
    #Okay, so move H5:G4. Red now evaluates every safe move it has and sees if it will result in an enemy sac.
    #B3:C4 would be bad for red, so it avoids that move, taking any other moves available.
    #In this case, red always goes for C6:D7, because it moves into a side column.



#---Heuristic #22: Avoid enemy tradeoffs if down in material ---   
#checkersMain("tests/HeuristicsTest - AvoidEnemyTradeoffs.txt",redWinCount,blackWinCount)
    #Notice how red is down in material; it does not desire to trade off its pieces.
    #Move A0:B1. Notice how red will never let black's G6 checker force a tradeoff.
    #Red always chooses E4:F3 or D5:E6.



#---Heuristic #23: Avoid moving into a square that then forces a bad jump next turn ---   
#checkersMain("tests/HeuristicsTest - AvoidForcedBadJump.txt",redWinCount,blackWinCount)
    #Move black king.
    #Red has the ability to become a king, but should it go to either H3 or H5?
    #As black, move H1:G0. Notice that if red were to go to H3, the game would be lost for red.
    #Black would just allow H3:F1, then it would jump G0:E2 to win.
    #This heuristic makes sure red avoids this.
    #Notice that red always goes to H5.

#checkersMain("tests/HeuristicsTest - AvoidForcedBadJump2.txt",redWinCount,blackWinCount)
    #Move black king.
    #Notice how red never goes C6:D7, because that would allow black to capitalize with a double jump.
    #(G0:H1, red goes D7:F5, then black with G6:E4:C2).



#---Heuristic #24: Avoid moving into a square that then forces a tradeoff next turn when down in material ---
#checkersMain("tests/HeuristicsTest - AvoidForcedTradeoff.txt",redWinCount,blackWinCount)
    #Move black king.
    #Similarly, red denies C6:D7 because red is down in material, and C6:D7 would force a tradeoff.



#     REMOVED    #---Heuristic #25: Don't block or avoid an enemy jump that would result in a gain of material for you ---
           #checkersMain("HeuristicsTest - AllowEnemyJumps.txt",redWinCount,blackWinCount)



#---Heuristic #26: Keep home row intact if enemy trying to king ---
#checkersMain("tests/HeuristicsTest - DisallowKinging.txt",redWinCount,blackWinCount)
    #Move the black king around. Notice how red refuses to move its home row piece.
    #It is preoccupied blocking the black checker from kinging.


#---Heuristic #27: At endgame, avoid death squares ---
#checkersMain("tests/HeuristicsTest - Endgame.txt",redWinCount,blackWinCount)
#checkersMain("tests/HeuristicsTest - Endgame2.txt",redWinCount,blackWinCount)
#checkersMain("tests/HeuristicsTest - Endgame3.txt",redWinCount,blackWinCount)

#checkersMain("",redWinCount,blackWinCount)

            
