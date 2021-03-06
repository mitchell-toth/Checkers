import random
import copy

DEBUG = False


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

def findCrownRowMovesOrJumps(board,player,movesList):
    kingingList=[]
    for move in movesList.copy():
        FROM=move[0:2]
        FROMRow=ord(FROM[0])-65
        FROMCol=int(FROM[1])
        TO=move[-2:]
        TORow=TO[0]
        if player=="r":
            kingRow="H"
        else:
            kingRow="A"
        if board[FROMRow][FROMCol]==player and TORow==kingRow:
            kingingList.append(move)
            #movesList=movesList[:movesList.index(move)]+movesList[movesList.index(move)+1:]
            movesList.remove(move)
    return kingingList


def findBlockingMoves(board,player,enemyJumpsList,enemyCrowningJumps,enemyCrowningMoves,movesList,jumpsList):
    movesListCopy = movesList.copy()
    jumpsListCopy = jumpsList.copy()
    movesThatBlockEnemyJumps = []
    preferredMovesThatBlockEnemyJumps = []
    jumpsThatBlockEnemyJumps = []
    preferredJumpsThatBlockEnemyJumps = []
    if len(enemyJumpsList) > 0:
        enemyEndingSquare = "a"
        endingSquare = "b"
        for enemyMove in enemyJumpsList.copy():
            FROMRow,FROMCol,TORow,TOCol=parseMove(enemyMove[:5])
            enemyEndingSquare = enemyMove[-2:]
            idealEnemyEndingSquare = enemyMove[3:5]
            jumpedChecker = chr(((FROMRow+TORow)//2)+65) + str((FROMCol+TOCol)//2)
            enemyStartingSquare = enemyMove[:2]
            for move in movesListCopy:
                FROMRow2,FROMCol2,TORow2,TOCol2=parseMove(move)
                currentChecker = move[:2]
                endingSquare = move[-2:]
                if endingSquare == enemyEndingSquare and currentChecker != jumpedChecker: #second part avoids self-block
                    movesThatBlockEnemyJumps.append(move)
                if endingSquare == idealEnemyEndingSquare and currentChecker != jumpedChecker:
                    preferredMovesThatBlockEnemyJumps.append(move)

            for jump in jumpsListCopy:
                endingSquare = jump[-2:]
                idealEndingSquare = jump[3:5]
                if endingSquare == enemyEndingSquare:
                    jumpsThatBlockEnemyJumps.append(jump)
                if endingSquare == idealEndingSquare:
                    preferredJumpsThatBlockEnemyJumps.append(jump)

            if len(enemyMove) > 5: #if multiple jump, block jump not just at end
                enemyMoveAsAList = enemyMove.split(":")
                for square in range(1,len(enemyMoveAsAList)-1): #middle squares
                    for move in movesListCopy:
                        endingSquare = move[-2:]
                        if endingSquare == enemyMoveAsAList[square]: 
                            if move not in movesThatBlockEnemyJumps:
                                movesThatBlockEnemyJumps.append(move)

                    for jump in jumpsListCopy:
                        endingSquare = jump[-2:]
                        if endingSquare == enemyMoveAsAList[square]:
                            jumpsThatBlockEnemyJumps.append(jump)
                
    movesThatBlockEnemyCrowningJumps = []
    jumpsThatBlockEnemyCrowningJumps = []
    if len(enemyCrowningJumps) > 0:
        enemyEndingSquare = "a"
        endingSquare = "b"
        for enemyMove in enemyCrowningJumps:
            enemyEndingSquare = enemyMove[-2:]
            for move in movesListCopy:
                endingSquare = move[-2:]
                if endingSquare == enemyEndingSquare:
                    movesThatBlockEnemyCrowningJumps.append(move)
                    if move in movesList:
                        movesList.remove(move)
            for jump in jumpsListCopy:
                endingSquare = jump[-2:]
                if endingSquare == enemyEndingSquare:
                    jumpsThatBlockEnemyCrowningJumps.append(jump)
                    if jump in jumpsList:
                        jumpsList.remove(jump)
            if len(enemyMove) > 5: #if multiple jump, block jump not just at end
                enemyMoveAsAList = enemyMove.split(":")
                for square in range(1,len(enemyMoveAsAList)-1): #middle squares
                    for move in movesListCopy:
                        endingSquare = move[-2:]
                        if endingSquare == enemyMoveAsAList[square]:
                            movesThatBlockEnemyCrowningJumps.append(move)
                            if move in movesList:
                                movesList.remove(move)
                    for jump in jumpsListCopy:
                        endingSquare = jump[-2:]
                        if endingSquare == enemyMoveAsAList[square]:
                            jumpsThatBlockEnemyCrowningJumps.append(jump)
                            if jump in jumpsList:
                                jumpsList.remove(jump)
                
    movesThatBlockEnemyCrowningMoves = []
    jumpsThatBlockEnemyCrowningMoves = []
    if len(enemyCrowningMoves) > 0:
        enemyEndingSquare = "a"
        endingSquare = "b"
        for enemyMove in enemyCrowningMoves:
            enemyEndingSquare = enemyMove[-2:]
            for move in movesListCopy:
                endingSquare = move[-2:]
                if endingSquare == enemyEndingSquare:
                    movesThatBlockEnemyCrowningMoves.append(move)
                    if move in movesList:
                        movesList.remove(move)
            for jump in jumpsListCopy:
                endingSquare = jump[-2:]
                if endingSquare == enemyEndingSquare:
                    jumpsThatBlockEnemyCrowningMoves.append(jump)
                    if jump in jumpsList:
                        jumpsList.remove(jump)

    #printDebugInfo("movesThatBlockEnemyJumps",movesThatBlockEnemyJumps,False)
    #printDebugInfo("preferredMovesThatBlockEnemyJumps",preferredMovesThatBlockEnemyJumps,False)

    return movesThatBlockEnemyJumps,preferredMovesThatBlockEnemyJumps,jumpsThatBlockEnemyJumps,preferredJumpsThatBlockEnemyJumps,movesThatBlockEnemyCrowningJumps,jumpsThatBlockEnemyCrowningJumps,movesThatBlockEnemyCrowningMoves,jumpsThatBlockEnemyCrowningMoves


def findUniqueUnion(list1, list2):
    uniqueJunction = []
    for move1 in list1:
        for move2 in list2:
            if move1 == move2 and (move1 not in uniqueJunction):
                uniqueJunction.append(move1)
    return uniqueJunction


def parseMove(move):
    FROM=move[0:2]
    FROMRow=ord(FROM[0])-65
    FROMCol=int(FROM[1])
    TO=move[3:5]
    TORow=ord(TO[0])-65
    TOCol=int(TO[1])
    return FROMRow,FROMCol,TORow,TOCol


#-----Heuristic 8: find and prefer longest jumps available-----
def findLongestJumpsOf(aJumpsList):
    longestJumps = []
    longestLength = 0
    for jump in aJumpsList:
        if len(jump) > 5 and len(jump) > longestLength:
            longestLength = len(jump)
    for jump in aJumpsList:
        if len(jump) == longestLength:
            longestJumps.append(jump)

    if longestJumps != []:
        return longestJumps
    else:  #no longest jumps, return jumps list as is
        return aJumpsList


#-----Heuristic 9: find and prefer jumps that jump enemy kings-----
def findJumpsThatJumpEnemyKingsIn(board,aJumpsList):
    jumpsThatJumpAnEnemyKing = []
    kingTokens = ["R","B"]
    for jump in aJumpsList:
        reps = jump.count(":")
        Jump = jump
        for i in range(reps):
            FROMRow,FROMCol,TORow,TOCol=parseMove(Jump)
            if board[(FROMRow+TORow)//2][(FROMCol+TOCol)//2] in kingTokens and jump not in jumpsThatJumpAnEnemyKing:
                jumpsThatJumpAnEnemyKing.append(jump)
            Jump=Jump[3:]
    return jumpsThatJumpAnEnemyKing


#-----Heuristic 10: prefer moves that get to a side column-----
def findSideColumnMoves(board,movesList):
    regularTokens = ["r","b"]
    sideColumnMoves = []
    sideColumns = [0,7]
    for move in movesList:
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        if board[FROMRow][FROMCol] in regularTokens: #only regular pieces
            if TOCol in sideColumns:
                sideColumnMoves.append(move)
    return sideColumnMoves


#-----Heuristic 11: keep home row checkers in place when there's only normal moves to be had-----
def movesNotInvolvingHomeRowCheckers(board,player,movesList):
    regularTokens = ["r","b"]
    movesThatDontMessWithHomeRow = movesList.copy()
    if player == "r":
        homeRow = 0
    else:
        homeRow = 7
    for move in movesList.copy():
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        if board[FROMRow][FROMCol] in regularTokens: #only regular pieces
            if FROMRow == homeRow:
                movesThatDontMessWithHomeRow.remove(move)
    return movesThatDontMessWithHomeRow


#-----Heuristic 12: Don't move to a space that lets the opponent jump you in some way-----
def findSafeMoves(board,player,movesList):
    endangeredSquares,immediatelyThreatenedCheckers = findEndangeredCheckers(board,player)
    safeMoves = movesList.copy()
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"

    enemyJumpsList=listSingleJumps(board,opponentPlayer)
    enemyJumpsList=listMultipleJumps(board,opponentPlayer,enemyJumpsList)
    #numEnemyJumps = len(enemyJumpsList)
    numEnemyJumps = 0
    for jump in enemyJumpsList:
        numEnemyJumps += len(jump)
    
    for move in movesList.copy():
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        oneMoveInFutureBoard = copy.deepcopy(board)
        playerToken = board[FROMRow][FROMCol]
        oneMoveInFutureBoard[FROMRow][FROMCol] = "e"
        oneMoveInFutureBoard[TORow][TOCol] = playerToken

        newEndangeredSquares,immediatelyThreatenedCheckers = findEndangeredCheckers(oneMoveInFutureBoard,player)
        for square in endangeredSquares:
            if square in newEndangeredSquares:
                newEndangeredSquares.remove(square)
        if len(newEndangeredSquares) > 0:  #if new threat is there
            safeMoves.remove(move)
            
    return safeMoves


#-----Heuristic 13: Move an endangered checker to a safe square if it can't be blocked-----
def findEndangeredCheckers(board,player):
    immediatelyThreatenedCheckers = []
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"
    enemyJumpsList=listSingleJumps(board,opponentPlayer)
    enemyJumpsList=listMultipleJumps(board,opponentPlayer,enemyJumpsList)
    endangeredCheckers = []
    for jump in enemyJumpsList:
        reps = jump.count(":")
        Jump = jump
        temp = 0
        for i in range(reps):
            FROMRow,FROMCol,TORow,TOCol=parseMove(Jump)
            jumpedChecker = board[(FROMRow+TORow)//2][(FROMCol+TOCol)//2]
            if jumpedChecker not in endangeredCheckers:
                endangeredCheckers.append(chr(((FROMRow+TORow)//2)+65)+str((FROMCol+TOCol)//2))
                if temp == 0:  #if first go-around
                    immediatelyThreatenedCheckers.append(chr(((FROMRow+TORow)//2)+65)+str((FROMCol+TOCol)//2))
            Jump=Jump[3:]
            temp = 1
    #print("Endangered checkers:",endangeredCheckers)
    return endangeredCheckers, immediatelyThreatenedCheckers

def findSafeMovesForEndangeredCheckers(board,player,movesList):
    movesToAvoidImmediateJump = []
    prioritizedAvoidingMoves = []
    endangeredCheckers,immediatelyThreatenedCheckers = findEndangeredCheckers(board,player)
    for move in movesList.copy():
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        FROMChecker = chr(FROMRow+65)+str(FROMCol)
        if FROMChecker in endangeredCheckers:
            movesToAvoidImmediateJump.append(move)
            if FROMChecker in immediatelyThreatenedCheckers:
                prioritizedAvoidingMoves.append(move)

    safeMovesToAvoidBeingJumped = findSafeMoves(board,player,movesToAvoidImmediateJump)
    prioritizedAvoidingMoves = findSafeMoves(board,player,prioritizedAvoidingMoves)
    #print("Safe avoiding moves:",safeMovesToAvoidBeingJumped,"Good avoiding moves:",prioritizedAvoidingMoves)
    return safeMovesToAvoidBeingJumped, prioritizedAvoidingMoves



#-----Heuristic 14: find and take positive sacrifice moves-----
#                   AND
#-----Heuristic 15: find tradeoff moves-----
def findSacrificesAndTradeoffs(board,player,movesList):
    infoDict = {}
    unsafeMoves = []
    sacrificeMoves = []
    tradeoffMoves = []
    badSacrificeMoves = []
    specialSacrificeMoves = []
    movesToConsider = []
    tradeoffMovesToDelete = []
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"
    ownJumpsList=listSingleJumps(board,player)
    ownJumpsList=listMultipleJumps(board,player,ownJumpsList)
    
    safeMoves = findSafeMoves(board,player,movesList.copy())
    startingOwnNumPieces = numPiecesLeft(board,player)
    startingEnemyNumPieces = numPiecesLeft(board,opponentPlayer)
    endangeredSquares,immediatelyThreatenedCheckers = findEndangeredCheckers(board,player)
    #printBoard(board)
    for move in movesList:
        if not move in safeMoves:
            movesToConsider.append(move)
    #printDebugInfo("sacrificeMoves",sacrificeMoves,True)

    for move in movesToConsider.copy():
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        futureBoard = copy.deepcopy(board)
        playerToken = futureBoard[FROMRow][FROMCol]
        futureBoard[FROMRow][FROMCol] = "e"
        futureBoard[TORow][TOCol] = playerToken
        newEndangeredSquare,immediatelyThreatenedCheckers = findEndangeredCheckers(futureBoard,player)
        for square in endangeredSquares:
            if square in newEndangeredSquare or square == move[3:]:
                newEndangeredSquare.remove(square)
        #theSquareToBeJumped = chr(((FROMRow+TORow)//2)+65) + str((FROMCol+TOCol)//2)
        #if len(newEndangeredSquare) > 0:
            #theSquareToBeJumped = newEndangeredSquare
        #else:
            #theSquareToBeJumped = "blah"
        for theSquareToBeJumped in newEndangeredSquare:
        #printDebugInfo("theSquareToBeJumped",theSquareToBeJumped,True)
        #printBoard(futureBoard)

            futureEnemyJumpsList=listSingleJumps(futureBoard,opponentPlayer)
            futureEnemyJumpsList=listMultipleJumps(futureBoard,opponentPlayer,futureEnemyJumpsList)

            jumpsInvolvingTheSquare = []
            for jump in futureEnemyJumpsList:
                reps = jump.count(":")
                Jump = jump
                for i in range(reps):
                    FROMRow,FROMCol,TORow,TOCol=parseMove(Jump)
                    jumpSquare = chr(((FROMRow+TORow)//2)+65) + str((FROMCol+TOCol)//2)
                    #input(jumpSquare)
                    #print(jumpSquare,theSquareToBeJumped,jumpsInvolvingTheSquare)
                    if jumpSquare == theSquareToBeJumped and jump not in jumpsInvolvingTheSquare:
                        jumpsInvolvingTheSquare.append(jump)
                    Jump=Jump[3:]
            #printDebugInfo("jumpsInvolvingTheSquare",jumpsInvolvingTheSquare,True)

            for jump1 in jumpsInvolvingTheSquare:
                futureBoard2 = copy.deepcopy(futureBoard)
                reps = jump1.count(":")
                Jump = jump1
                for i in range(reps):
                    FROMRow2,FROMCol2,TORow2,TOCol2=parseMove(Jump)
                    enemyToken = futureBoard2[FROMRow2][FROMCol2]
                    futureBoard2[FROMRow2][FROMCol2] = "e"
                    futureBoard2[(FROMRow2+TORow2)//2][(FROMCol2+TOCol2)//2] = "e"
                    futureBoard2[TORow2][TOCol2] = enemyToken
                    Jump=Jump[3:]
                newOwnNumPieces = numPiecesLeft(futureBoard2,player)
                #printBoard(futureBoard2)

                futureOwnJumpsList=listSingleJumps(futureBoard2,player)
                futureOwnJumpsList=listMultipleJumps(futureBoard2,player,futureOwnJumpsList)
                
                theSquareToBeJumped = str(jump[-2:])
                #printDebugInfo("theSquareToBeJumped",theSquareToBeJumped,True)
                jumpsInvolvingTheSquare = []
                for jump in futureOwnJumpsList:
                    if not jump in ownJumpsList and len(jump) > len(jump1):  #if new jump choice
                        specialSacrificeMoves.append(move)
                    reps = jump.count(":")
                    Jump = jump
                    for i in range(reps):
                        FROMRow3,FROMCol3,TORow3,TOCol3=parseMove(Jump)
                        jumpedSquare = chr(((FROMRow3+TORow3)//2)+65) + str((FROMCol3+TOCol3)//2)
                        if jumpedSquare == theSquareToBeJumped and jump not in jumpsInvolvingTheSquare:
                            jumpsInvolvingTheSquare.append(jump)
                        Jump=Jump[3:]
                #printDebugInfo("jumpsInvolvingTheSquare",jumpsInvolvingTheSquare,True)

                if len(jumpsInvolvingTheSquare) == 0:  #if no response jump, remove move
                    badSacrificeMoves.append(move)
                    tradeoffMovesToDelete.append(move)

                else:  #else, do more checks
                    for jump in jumpsInvolvingTheSquare:
                        futureBoard3 = copy.deepcopy(futureBoard2)
                        reps = jump.count(":")
                        Jump = jump
                        for i in range(reps):
                            FROMRow3,FROMCol3,TORow3,TOCol3=parseMove(Jump)
                            ownToken = futureBoard3[FROMRow3][FROMCol3]
                            futureBoard3[FROMRow3][FROMCol3] = "e"
                            futureBoard3[(FROMRow3+TORow3)//2][(FROMCol3+TOCol3)//2] = "e"
                            futureBoard3[TORow3][TOCol3] = ownToken
                            Jump=Jump[3:]
                            
                        theSquareToBeJumped = str(jump[-2:])
                        futureEnemyJumpsList=listSingleJumps(futureBoard3,opponentPlayer)
                        futureEnemyJumpsList=listMultipleJumps(futureBoard3,opponentPlayer,futureEnemyJumpsList)

                        jumpsInvolvingTheSquare = []
                        for jump in futureEnemyJumpsList:
                            reps = jump.count(":")
                            Jump = jump
                            for i in range(reps):
                                FROMRow4,FROMCol4,TORow4,TOCol4=parseMove(Jump)
                                jumpedSquare = chr(((FROMRow4+TORow4)//2)+65) + str((FROMCol4+TOCol4)//2)
                                if jumpedSquare == theSquareToBeJumped and jump not in jumpsInvolvingTheSquare:
                                    jumpsInvolvingTheSquare.append(jump)
                                Jump=Jump[3:]
                                
                        if jumpsInvolvingTheSquare == []:  #if no enemy comeback
                            newEnemyNumPieces = numPiecesLeft(futureBoard3,opponentPlayer)
                            numOwnPiecesLost = startingOwnNumPieces - newOwnNumPieces
                            numEnemyPiecesLost = startingEnemyNumPieces - newEnemyNumPieces
                            theJuicyDifference = numEnemyPiecesLost - numOwnPiecesLost
                            #printDebugInfo("numOwnPiecesLost",numOwnPiecesLost,False)
                            #printDebugInfo("numEnemyPiecesLost",numEnemyPiecesLost,True)
                            if numOwnPiecesLost < numEnemyPiecesLost and not move in sacrificeMoves:
                                sacrificeMoves.append(move)
                                if move in infoDict:
                                    if infoDict[move] > theJuicyDifference:
                                        infoDict[move] = theJuicyDifference
                                else:
                                    infoDict[move] = theJuicyDifference
                            elif numOwnPiecesLost == numEnemyPiecesLost and not move in tradeoffMoves:
                                tradeoffMoves.append(move)
                            if numOwnPiecesLost != numEnemyPiecesLost:
                                if move in tradeoffMoves:
                                    tradeoffMovesToDelete.append(move)
                            if numOwnPiecesLost > numEnemyPiecesLost:
                                badSacrificeMoves.append(move)
                                
                        else:  #if enemy comeback
                            for jump in jumpsInvolvingTheSquare:
                                futureBoard4 = copy.deepcopy(futureBoard3)
                                reps = jump.count(":")
                                Jump = jump
                                for i in range(reps):
                                    FROMRow4,FROMCol4,TORow4,TOCol4=parseMove(Jump)
                                    enemyToken = futureBoard4[FROMRow4][FROMCol4]
                                    futureBoard4[FROMRow4][FROMCol4] = "e"
                                    futureBoard4[(FROMRow4+TORow4)//2][(FROMCol4+TOCol4)//2] = "e"
                                    futureBoard4[TORow4][TOCol4] = enemyToken
                                    Jump=Jump[3:]

                                newEnemyNumPieces = numPiecesLeft(futureBoard4,opponentPlayer)
                                newOwnNumPieces = numPiecesLeft(futureBoard4,player)
                                numOwnPiecesLost = startingOwnNumPieces - newOwnNumPieces
                                numEnemyPiecesLost = startingEnemyNumPieces - newEnemyNumPieces
                                theJuicyDifference = numEnemyPiecesLost - numOwnPiecesLost

                                if numOwnPiecesLost < numEnemyPiecesLost and not move in sacrificeMoves:
                                    sacrificeMoves.append(move)
                                    if move in infoDict:
                                        if infoDict[move] > theJuicyDifference:
                                            infoDict[move] = theJuicyDifference
                                    else:
                                        infoDict[move] = theJuicyDifference
                                elif numOwnPiecesLost == numEnemyPiecesLost and not move in tradeoffMoves:
                                    tradeoffMoves.append(move)
                                    if not move in sacrificeMoves:
                                        sacrificeMoves.append(move)
                                if numOwnPiecesLost != numEnemyPiecesLost:
                                    if move in tradeoffMoves:
                                        tradeoffMovesToDelete.append(move)
                                if numOwnPiecesLost > numEnemyPiecesLost:
                                    badSacrificeMoves.append(move)
                                

    bestSacs = []
    bestDifference = 0
    for move in infoDict:
        if infoDict[move] > bestDifference:
            bestDifference = infoDict[move]
    for move in infoDict:
        if infoDict[move] == bestDifference:
            bestSacs.append(move)

    for move in tradeoffMoves.copy():
        if move in tradeoffMovesToDelete:
            tradeoffMoves.remove(move)
    for move in specialSacrificeMoves:
        if move not in sacrificeMoves:
            sacrificeMoves.append(move)
    for move in sacrificeMoves.copy():
        if move in badSacrificeMoves or move in tradeoffMoves:
            sacrificeMoves.remove(move)
    for move in bestSacs.copy():
        if move in badSacrificeMoves or move in tradeoffMoves:
            bestSacs.remove(move)

    #printDebugInfo("bestSacs",bestSacs,False)
    return sacrificeMoves,bestSacs,tradeoffMoves


def numPiecesLeft(board,player):
    playerTokenCount = 0
    for row in range(8):
        for col in range(8):
            if board[row][col] == player:
                playerTokenCount += 1
            elif board[row][col] == player.upper():  #kings worth double
                playerTokenCount += 2
    return playerTokenCount

def printBoard(board):
    for row in range(8):
        for col in range(8):
            print("",board[row][col],end="")
        print()
    print()

def printDebugInfo(name,value,doInput):
    print(str(name)+": "+str(value))
    if doInput:
        input()


#-----Heuristic 15 (continued): prioritize tradeoff moves when ahead-----
def doTradeoffs(board,player):
    doTradeoffs = False
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"
    ownNumPieces = numPiecesLeft(board,player)
    enemyNumPieces = numPiecesLeft(board,opponentPlayer)
    if ownNumPieces > enemyNumPieces:
        doTradeoffs = True
    return doTradeoffs



def determineStatus(board,player):
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"

    ownNumPieces = numPiecesLeft(board,player)
    enemyNumPieces = numPiecesLeft(board,opponentPlayer)

    numOwnCheckers = 0
    numOwnKings = 0
    encroach = True
    for row in range(8):
        for col in range(8):
            if board[row][col].lower() == player:
                numOwnCheckers += 1
                if board[row][col] != player.upper():  #if not a king
                    encroach = False  #encroach only when kings left for player
                else:
                    numOwnKings += 1

    numEnemyCheckers = 0
    numEnemyKings = 0
    for row in range(8):
        for col in range(8):
            if board[row][col].lower() == opponentPlayer:
                numEnemyCheckers += 1
            if board[row][col] == opponentPlayer.upper():
                numEnemyKings += 1
    if numEnemyCheckers == 1:
        repetitionCornerSquares = ["G0","H1","A6","B7","F1","G2","B5","C6"]
        enemyMovesList=listValidMoves(board,opponentPlayer)
        if len(enemyMovesList) > 0:
            anEnemyMove = enemyMovesList[0]
            FROMLocation = anEnemyMove[:2]
            if FROMLocation in repetitionCornerSquares:
                encroach = False

    stopPreservingHomeRow = False
    if numOwnCheckers < 8:  #arbitrary number choice
        stopPreservingHomeRow = True

    downInMaterial = False
    if ownNumPieces < enemyNumPieces:
        downInMaterial = True

    oneKingLeft = False
    if numOwnKings == 1 and ownNumPieces == 2:
        oneKingLeft = True
    elif numOwnKings > 1 and numOwnKings <= 3:  #check for trapped kings
        movesList=listValidMoves(board,player)
        safeMoves = findSafeMoves(board,player,movesList.copy())
        uniqueStartingSquares = []
        for move in safeMoves:
            if move[:2] not in uniqueStartingSquares:
                uniqueStartingSquares.append(move[:2])
        if len(uniqueStartingSquares) == 1:  #if other king(s) can't move
            oneKingLeft = True
    #elif numEnemyKings == 1:
        #oneKingLeft = True
    
    return stopPreservingHomeRow, encroach, downInMaterial, oneKingLeft



#-----Heuristic 16: when no safe moves, make a move that limits the damage-----
def limitTheBleeding(board,player,movesList):
    infoDict = {}
    bestMoves = []
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"
    safeMoves = findSafeMoves(board,player,movesList.copy())
    startingOwnNumPieces = numPiecesLeft(board,player)
    endangeredSquares,immediatelyThreatenedCheckers = findEndangeredCheckers(board,player)
    #printBoard(board)

    for move in movesList.copy():
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        futureBoard = copy.deepcopy(board)
        playerToken = futureBoard[FROMRow][FROMCol]
        futureBoard[FROMRow][FROMCol] = "e"
        futureBoard[TORow][TOCol] = playerToken
        newEndangeredSquare,immediatelyThreatenedCheckers = findEndangeredCheckers(futureBoard,player)
        for square in endangeredSquares:
            if square in newEndangeredSquare or square == move[3:]:
                newEndangeredSquare.remove(square)
                
        if len(newEndangeredSquare) > 0:
            theSquareToBeJumped = newEndangeredSquare[0]
        else:
            theSquareToBeJumped = "blah"

        futureEnemyJumpsList=listSingleJumps(futureBoard,opponentPlayer)
        futureEnemyJumpsList=listMultipleJumps(futureBoard,opponentPlayer,futureEnemyJumpsList)

        jumpsInvolvingTheSquare = []
        for jump in futureEnemyJumpsList:
            reps = jump.count(":")
            Jump = jump
            for i in range(reps):
                FROMRow,FROMCol,TORow,TOCol=parseMove(Jump)
                jumpSquare = chr(((FROMRow+TORow)//2)+65) + str((FROMCol+TOCol)//2)
                if jumpSquare == theSquareToBeJumped and jump not in jumpsInvolvingTheSquare:
                    jumpsInvolvingTheSquare.append(jump)
                Jump=Jump[3:]
        #printDebugInfo("jumpsInvolvingTheSquare",jumpsInvolvingTheSquare,True)

        for jump in jumpsInvolvingTheSquare:
            futureBoard2 = copy.deepcopy(futureBoard)
            reps = jump.count(":")
            Jump = jump
            for i in range(reps):
                FROMRow2,FROMCol2,TORow2,TOCol2=parseMove(Jump)
                enemyToken = futureBoard2[FROMRow2][FROMCol2]
                futureBoard2[FROMRow2][FROMCol2] = "e"
                futureBoard2[(FROMRow2+TORow2)//2][(FROMCol2+TOCol2)//2] = "e"
                futureBoard2[TORow2][TOCol2] = enemyToken
                Jump=Jump[3:]
            newOwnNumPieces = numPiecesLeft(futureBoard2,player)
            numOwnPiecesLost = startingOwnNumPieces - newOwnNumPieces
            if move in infoDict:
                if infoDict[move] < numOwnPiecesLost:  #Take worst case
                    infoDict[move] = numOwnPiecesLost
            else:
                infoDict[move] = numOwnPiecesLost

    minimumLoss = 10
    for move in infoDict:
        if infoDict[move] < minimumLoss:
            minimumLoss = infoDict[move]
    for move in infoDict:
        if infoDict[move] == minimumLoss:
            bestMoves.append(move)
    #printDebugInfo("bestMoves",bestMoves,False)
    return bestMoves


#-----Heuristic 17: find and prefer regular jumps that land on a safe square-----
def findSafeJumps(board,player,jumpsList):
    safeJumps = []
    for jump in jumpsList.copy():
        futureBoard = copy.deepcopy(board)
        endingSquare = jump[-2:]
        reps = jump.count(":")
        Jump = jump
        for i in range(reps):
            FROMRow,FROMCol,TORow,TOCol=parseMove(Jump)
            ownToken = futureBoard[FROMRow][FROMCol]
            futureBoard[FROMRow][FROMCol] = "e"
            futureBoard[(FROMRow+TORow)//2][(FROMCol+TOCol)//2] = "e"
            futureBoard[TORow][TOCol] = ownToken
            Jump=Jump[3:]
        endangeredSquares,immediatelyThreatenedCheckers = findEndangeredCheckers(futureBoard,player)
        if not endingSquare in endangeredSquares:
            safeJumps.append(jump)
    return safeJumps


#-----Heuristic 18: find the jumps that win most material-----
def findBestJumps(board,player,jumpsList):
    infoDict = {}
    bestJumps = []
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"
    startingEnemyNumPieces = numPiecesLeft(board,opponentPlayer)
    for jump in jumpsList.copy():
        futureBoard = copy.deepcopy(board)
        endingSquare = jump[-2:]
        reps = jump.count(":")
        Jump = jump
        for i in range(reps):
            FROMRow,FROMCol,TORow,TOCol=parseMove(Jump)
            ownToken = futureBoard[FROMRow][FROMCol]
            futureBoard[FROMRow][FROMCol] = "e"
            futureBoard[(FROMRow+TORow)//2][(FROMCol+TOCol)//2] = "e"
            futureBoard[TORow][TOCol] = ownToken
            Jump=Jump[3:]
        newEnemyNumPieces = numPiecesLeft(futureBoard,opponentPlayer)
        enemyPiecesLost = startingEnemyNumPieces-newEnemyNumPieces
        infoDict[jump] = enemyPiecesLost
        
    highestEnemyLoss = 0
    for jump in infoDict:  #find max enemy loss
        if infoDict[jump] > highestEnemyLoss:
            highestEnemyLoss = infoDict[jump]
    for jump in infoDict:  #find the jumps that do it
        if infoDict[jump] == highestEnemyLoss:
            bestJumps.append(jump)
    if bestJumps != []:  #if there are best jumps
        return bestJumps,highestEnemyLoss
    else:  #if somehow not
        return jumpsList,highestEnemyLoss


#-----Heuristic 19: encroach on enemy pieces with kings-----
def encroachingMoves(board,player,movesList):
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"
    kingMoves = []
    encroachMoves = []
    for move in movesList:
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        if board[FROMRow][FROMCol] == player.upper():
            kingMoves.append(move)
    enemyCheckerLocationList = []
    for row in range(8):
        for col in range(8):
            if board[row][col].lower() == opponentPlayer:
                enemyCheckerLocationList.append([row,col])
                
    closestDistance = 10
    movesThatMoveClosest = []
    distanceDict = {}
    for move in kingMoves:
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        for enemyChecker in enemyCheckerLocationList:
            enemyRow = enemyChecker[0]
            enemyCol = enemyChecker[1]
            startingDistance = (((FROMRow-enemyRow)**2)+((FROMCol-enemyCol)**2))**0.5
            endingDistance = (((TORow-enemyRow)**2)+((TOCol-enemyCol)**2))**0.5
            if endingDistance < startingDistance and move not in encroachMoves:
                encroachMoves.append(move)
                distanceDict[move] = endingDistance
                if endingDistance < closestDistance:
                    closestDistance = endingDistance

    for move in distanceDict:
        if distanceDict[move] == closestDistance:
            movesThatMoveClosest.append(move)
    movesThatMoveClosest = findSafeMoves(board,player,movesThatMoveClosest.copy())
    #print(movesThatMoveClosest)
    
    safeEncroachMoves = findSafeMoves(board,player,encroachMoves.copy())
    return safeEncroachMoves, movesThatMoveClosest

def ANTIencroachingMoves(board,player,movesList):
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"
    kingMoves = []
    antiEncroachMoves = []
    for move in movesList:
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        if board[FROMRow][FROMCol] == player.upper():
            kingMoves.append(move)
    enemyCheckerLocationList = []
    for row in range(8):
        for col in range(8):
            if board[row][col].lower() == opponentPlayer:
                enemyCheckerLocationList.append([row,col])
                
    for move in kingMoves:
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        for enemyChecker in enemyCheckerLocationList:
            enemyRow = enemyChecker[0]
            enemyCol = enemyChecker[1]
            startingDistance = (((FROMRow-enemyRow)**2)+((FROMCol-enemyCol)**2))**0.5
            endingDistance = (((TORow-enemyRow)**2)+((TOCol-enemyCol)**2))**0.5
            if endingDistance > startingDistance and move not in antiEncroachMoves:
                antiEncroachMoves.append(move)
    
    safeAntiEncroachMoves = findSafeMoves(board,player,antiEncroachMoves.copy())
    return safeAntiEncroachMoves


#-----Heuristic 20: find and take "trapping" moves if one enemy checker left-----
def findLastTrap(board,player,movesList):
    trappingMoves = []
    bottomRightCornerLocation = [[7,7],[6,6],[5,5]]
    topLeftCornerLocation = [[0,0],[1,1],[2,2]]
    BOTTOMedgeLocationsROW = [[7,3],[7,5],[6,4]]
    TOPedgeLocationsROW = [[0,2],[0,4],[1,3]]
    RIGHTedgeLocationsCOL = [[3,7],[5,7],[4,6]]
    LEFTedgeLocationsCOL = [[2,0],[4,0],[3,1]]
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"
    #enemyNumPieces = numPiecesLeft(board,opponentPlayer)
    #if enemyNumPieces > 2:
        #return []
    enemyCheckerLocationList = []
    for row in range(8):
        for col in range(8):
            if board[row][col].lower() == opponentPlayer:
                enemyCheckerLocationList.append([row,col])
    for move in movesList:
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        for enemyChecker in enemyCheckerLocationList:
            enemyRow = enemyChecker[0]
            enemyCol = enemyChecker[1]
            bestSquaresToLandOn = []
            if enemyChecker in bottomRightCornerLocation:
                bestSquaresToLandOn = [str(chr(enemyRow-2+65)+str(enemyCol)),str(chr(enemyRow+65)+str(enemyCol-2)),str(chr(enemyRow-2+65)+str(enemyCol-2))]
            elif enemyChecker in topLeftCornerLocation:
                bestSquaresToLandOn = [str(chr(enemyRow+2+65)+str(enemyCol)),str(chr(enemyRow+65)+str(enemyCol+2)),str(chr(enemyRow+2+65)+str(enemyCol+2))]
            elif enemyChecker in BOTTOMedgeLocationsROW:
                bestSquaresToLandOn = [str(chr(enemyRow-2+65)+str(enemyCol))]
            elif enemyChecker in TOPedgeLocationsROW:
                bestSquaresToLandOn = [str(chr(enemyRow+2+65)+str(enemyCol))]
            elif enemyChecker in RIGHTedgeLocationsCOL:
                bestSquaresToLandOn = [str(chr(enemyRow+65)+str(enemyCol-2))]
            elif enemyChecker in LEFTedgeLocationsCOL:
                bestSquaresToLandOn = [str(chr(enemyRow+65)+str(enemyCol+2))]
            #else:
                #return []
            if move[-2:] in bestSquaresToLandOn and move not in trappingMoves:
                trappingMoves.append(move)
    return trappingMoves


#-----Heuristic 21: avoid moving into an enemy sacrifice-----
                #AND
#-----Heuristic 22: avoid moving into an enemy tradeoff if down in material-----
        #see the 'determineStatus' function as well

def avoidEnemySacsAndTradeoffs(board,player,movesList):
    movesThatDontMoveIntoAnEnemySac = []
    movesThatEliminateEnemySacs = []
    movesThatDontMoveIntoAnEnemyTradeoff = []
    movesThatEliminateEnemyTradeoffs = []
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"
    initialEnemyMovesList=listValidMoves(board,opponentPlayer)
    initialEnemySacrificeMoves,initialEnemyBestSacs,initialEnemyTradeoffMoves = findSacrificesAndTradeoffs(board,opponentPlayer,initialEnemyMovesList)
    safeMoves = findSafeMoves(board,player,movesList.copy())
    for move in safeMoves:
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        futureBoard = copy.deepcopy(board)
        playerToken = futureBoard[FROMRow][FROMCol]
        futureBoard[FROMRow][FROMCol] = "e"
        futureBoard[TORow][TOCol] = playerToken
        enemyMovesList=listValidMoves(futureBoard,opponentPlayer)
        enemySacrificeMoves,enemyBestSacs,enemyTradeoffMoves = findSacrificesAndTradeoffs(futureBoard,opponentPlayer,enemyMovesList)
        
        numSacrificesTHEN = len(initialEnemySacrificeMoves)
        numSacrificesNOW = len(enemySacrificeMoves)
        
        numTradeoffsTHEN = len(initialEnemyTradeoffMoves)
        numTradeoffsNOW = len(enemyTradeoffMoves)

        if numSacrificesNOW <= numSacrificesTHEN:
            movesThatDontMoveIntoAnEnemySac.append(move)
            if numSacrificesNOW < numSacrificesTHEN:
                movesThatEliminateEnemySacs.append(move)
                
        if numTradeoffsNOW <= numTradeoffsTHEN:
            movesThatDontMoveIntoAnEnemyTradeoff.append(move)
            if numTradeoffsNOW < numTradeoffsTHEN:
                movesThatEliminateEnemyTradeoffs.append(move)
    return movesThatDontMoveIntoAnEnemySac, movesThatDontMoveIntoAnEnemyTradeoff, movesThatEliminateEnemySacs, movesThatEliminateEnemyTradeoffs


def lookForEnemySacs(board,player,movesList):
    thereIsASacToAvoidNow = False
    thereIsASacToAvoid = False
    if player=="b":
        opponentPlayer = "r"
    else:
        opponentPlayer = "b"
    initialEnemyMovesList=listValidMoves(board,opponentPlayer)
    initialEnemySacrificeMoves,initialEnemyBestSacs,initialEnemyTradeoffMoves = findSacrificesAndTradeoffs(board,opponentPlayer,initialEnemyMovesList)
    if initialEnemySacrificeMoves != []:
        thereIsASacToAvoidNow = True
        
    safeMoves = findSafeMoves(board,player,movesList.copy())
    for move in safeMoves:
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        futureBoard = copy.deepcopy(board)
        playerToken = futureBoard[FROMRow][FROMCol]
        futureBoard[FROMRow][FROMCol] = "e"
        futureBoard[TORow][TOCol] = playerToken
        enemyMovesList=listValidMoves(futureBoard,opponentPlayer)
        enemySacrificeMoves,enemyBestSacs,enemyTradeoffMoves = findSacrificesAndTradeoffs(futureBoard,opponentPlayer,enemyMovesList)
        
        numSacrificesTHEN = len(initialEnemySacrificeMoves)
        numSacrificesNOW = len(enemySacrificeMoves)
        
        numTradeoffsTHEN = len(initialEnemyTradeoffMoves)
        numTradeoffsNOW = len(enemyTradeoffMoves)

        if numSacrificesNOW > numSacrificesTHEN:
            thereIsASacToAvoid = True
            
    return thereIsASacToAvoidNow, thereIsASacToAvoid


#-----Heuristic 23: Avoid moving into a square that then forces a bad jump next turn-----
#          AND
#-----Heuristic 24: Avoid moving into a square that then forces a tradeoff next turn if I'm down in material-----
def avoidMovesThatSetUpForBadJump(board,player,movesList):
    infoDict = {}
    movesThatAvoidBadForcedJump = movesList.copy()
    tradeoffMoves = []
    movesThatAvoidForcedTradeoffJumps = movesList.copy()
    negativeMoves = []
    if player=="r":
        kingRow=7
        opponentPlayer = "b"
    else:
        kingRow=0
        opponentPlayer = "r"
    kingTokens = ["R","B"]
    startingEnemyNumPieces = numPiecesLeft(board,opponentPlayer)
        
    for move in movesList:  #considering only safe moves
        #print(move)
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        futureBoard = copy.deepcopy(board)
        playerToken = futureBoard[FROMRow][FROMCol]
        futureBoard[FROMRow][FROMCol] = "e"
        if playerToken not in kingTokens and TORow == kingRow:
            futureBoard[TORow][TOCol] = playerToken.upper()  #make a king
        else:
            futureBoard[TORow][TOCol] = playerToken
        futureOwnJumpsList = listSingleJumps(futureBoard,player)
        futureOwnJumpsList = listMultipleJumps(futureBoard,player,futureOwnJumpsList)
        #printBoard(futureBoard)


        jumpsForThatMovedChecker = []
        for jump in futureOwnJumpsList:
            FROMRow2,FROMCol2,TORow2,TOCol2=parseMove(jump)
            if FROMRow2 == TORow and FROMCol2 == TOCol:  #if jump is with moved checker
                jumpsForThatMovedChecker.append(jump)
        #print(jumpsForThatMovedChecker)

        for jump in jumpsForThatMovedChecker:
            futureBoard2 = copy.deepcopy(futureBoard)
            reps = jump.count(":")
            Jump = jump
            for i in range(reps):
                FROMRow3,FROMCol3,TORow3,TOCol3=parseMove(Jump)
                playerToken = futureBoard2[FROMRow3][FROMCol3]
                futureBoard2[FROMRow3][FROMCol3] = "e"
                futureBoard2[(FROMRow3+TORow3)//2][(FROMCol3+TOCol3)//2] = "e"
                futureBoard2[TORow3][TOCol3] = playerToken
                Jump=Jump[3:]
            #printBoard(futureBoard2)
            checkerLocation = chr(TORow3+65) + str(TOCol3)

            futureEnemyJumpsList = listSingleJumps(futureBoard2,opponentPlayer)
            futureEnemyJumpsList = listMultipleJumps(futureBoard2,opponentPlayer,futureEnemyJumpsList)

            startingOwnNumPieces = numPiecesLeft(futureBoard2,player)


            jumpsInvolvingTheMovedCheckerThatJustMadeAJump = []
            for jump in futureEnemyJumpsList:
                reps = jump.count(":")
                Jump = jump
                for i in range(reps):
                    FROMRow4,FROMCol4,TORow4,TOCol4=parseMove(Jump)
                    jumpedChecker = chr(((FROMRow4+TORow4)//2)+65) + str((FROMCol4+TOCol4)//2)
                    if jumpedChecker == checkerLocation:  #if my piece can get jumped
                        jumpsInvolvingTheMovedCheckerThatJustMadeAJump.append(jump)
                    Jump=Jump[3:]

            for jump in jumpsInvolvingTheMovedCheckerThatJustMadeAJump:
                futureBoard3 = copy.deepcopy(futureBoard2)
                reps = jump.count(":")
                Jump = jump
                for i in range(reps):
                    FROMRow5,FROMCol5,TORow5,TOCol5=parseMove(Jump)
                    enemyToken = futureBoard3[FROMRow5][FROMCol5]
                    futureBoard3[FROMRow5][FROMCol5] = "e"
                    futureBoard3[(FROMRow5+TORow5)//2][(FROMCol5+TOCol5)//2] = "e"
                    futureBoard3[TORow5][TOCol5] = enemyToken
                    Jump=Jump[3:]

                enemyCheckerLocation = chr(TORow5+65) + str(TOCol5)
                futureOwnJumpsList = listSingleJumps(futureBoard3,player)
                futureOwnJumpsList = listMultipleJumps(futureBoard3,player,futureOwnJumpsList)

                newOwnNumPieces = numPiecesLeft(futureBoard3,player)
                newEnemyNumPieces = numPiecesLeft(futureBoard3,opponentPlayer)
                
                myReturningJumps = []
                for jump in futureOwnJumpsList:
                    reps = jump.count(":")
                    Jump = jump
                    for i in range(reps):
                        FROMRow6,FROMCol6,TORow6,TOCol6=parseMove(Jump)
                        jumpedChecker = chr(((FROMRow6+TORow6)//2)+65) + str((FROMCol6+TOCol6)//2)
                        if jumpedChecker == enemyCheckerLocation:  #if enemy piece can get jumped by me
                            myReturningJumps.append(jump)
                        Jump=Jump[3:]

                if myReturningJumps != []:
                    for jump in myReturningJumps:
                        futureBoard4 = copy.deepcopy(futureBoard3)
                        reps = jump.count(":")
                        Jump = jump
                        for i in range(reps):
                            FROMRow7,FROMCol7,TORow7,TOCol7=parseMove(Jump)
                            ownToken = futureBoard4[FROMRow7][FROMCol7]
                            futureBoard4[FROMRow7][FROMCol7] = "e"
                            futureBoard4[(FROMRow7+TORow7)//2][(FROMCol7+TOCol7)//2] = "e"
                            futureBoard4[TORow7][TOCol7] = ownToken
                            Jump=Jump[3:]
                        newEnemyNumPieces = numPiecesLeft(futureBoard4,opponentPlayer)


                numOwnPiecesLost = startingOwnNumPieces - newOwnNumPieces
                numEnemyPiecesLost = startingEnemyNumPieces - newEnemyNumPieces
                theDifference = numEnemyPiecesLost - numOwnPiecesLost

                if move in infoDict:
                    if theDifference < infoDict[move]:
                        infoDict[move] = theDifference
                else:
                    infoDict[move] = theDifference

    for move in infoDict:
        if infoDict[move] == 0:  #if tradeoff
            tradeoffMoves.append(move)
            movesThatAvoidForcedTradeoffJumps.remove(move)
        elif infoDict[move] < 0:  #if bad, forced jump
            negativeMoves.append(move)
            movesThatAvoidBadForcedJump.remove(move)
            movesThatAvoidForcedTradeoffJumps.remove(move)
    #print(negativeMoves, tradeoffMoves)
    return negativeMoves, tradeoffMoves


def removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesList,downInMaterial):
    negativeMoves,tradeoffMoves = avoidMovesThatSetUpForBadJump(board,player,movesList.copy())
    movesListCopy = movesList.copy()
    movesListToAlter = movesList.copy()
    if downInMaterial:
        for move in movesListCopy:
            if move in tradeoffMoves or move in negativeMoves:
                movesListToAlter.remove(move)
    else:
        for move in movesListCopy:
            if move in negativeMoves:
                movesListToAlter.remove(move)
    return movesListToAlter


#     REMOVED     #-----Heuristic 25: Don't block or avoid an enemy jump that would result in a gain of material for you, or a tradeoff when ahead-----
def considerAllowingEnemyJump(board,player,enemyJumps,downInMaterial):
    if enemyJumps == []:
        return False
        
    allowJumpage = True
    onlyPositiveGainToBeHad = True
    infoDict = {}
    tradeOffWhenJumpAllowed = []
    gainWhenJumpAllowed = []
    if player=="r":
        opponentPlayer = "b"
    else:
        opponentPlayer = "r"

    startingOwnNumPieces = numPiecesLeft(board,player)
    startingEnemyNumPieces = numPiecesLeft(board,opponentPlayer)
        
    for jump in enemyJumps:
        futureBoard = copy.deepcopy(board)
        reps = jump.count(":")
        Jump = jump
        for i in range(reps):
            FROMRow,FROMCol,TORow,TOCol=parseMove(Jump)
            enemyToken = futureBoard[FROMRow][FROMCol]
            futureBoard[FROMRow][FROMCol] = "e"
            futureBoard[(FROMRow+TORow)//2][(FROMCol+TOCol)//2] = "e"
            futureBoard[TORow][TOCol] = enemyToken
            Jump=Jump[3:]
        checkerToJump = chr(TORow+65) + str(TOCol)
        
        futureOwnJumpsList = listSingleJumps(futureBoard,player)
        futureOwnJumpsList = listMultipleJumps(futureBoard,player,futureOwnJumpsList)


        myReturningJumps = []
        for jump in futureOwnJumpsList:
            reps = jump.count(":")
            Jump = jump
            for i in range(reps):
                FROMRow2,FROMCol2,TORow2,TOCol2=parseMove(Jump)
                jumpedChecker = chr(((FROMRow2+TORow2)//2)+65) + str((FROMCol2+TOCol2)//2)
                if jumpedChecker == checkerToJump:  #if enemy piece can get jumped by me
                    myReturningJumps.append(jump)
                Jump=Jump[3:]
                
        if myReturningJumps != []:
            for jump in myReturningJumps:
                futureBoard2 = copy.deepcopy(futureBoard)
                reps = jump.count(":")
                Jump = jump
                for i in range(reps):
                    FROMRow3,FROMCol3,TORow3,TOCol3=parseMove(Jump)
                    ownToken = futureBoard2[FROMRow3][FROMCol3]
                    futureBoard2[FROMRow3][FROMCol3] = "e"
                    futureBoard2[(FROMRow3+TORow3)//2][(FROMCol3+TOCol3)//2] = "e"
                    futureBoard2[TORow3][TOCol3] = ownToken
                    Jump=Jump[3:]
                checkerToJump = chr(TORow3+65) + str(TOCol3)

                futureEnemyJumpsList = listSingleJumps(futureBoard2,opponentPlayer)
                futureEnemyJumpsList = listMultipleJumps(futureBoard2,opponentPlayer,futureEnemyJumpsList)

                newEnemyNumPieces = numPiecesLeft(futureBoard2,opponentPlayer)
                newOwnNumPieces = numPiecesLeft(futureBoard2,player)
                
                enemyReturningJumps = []
                for jump in futureEnemyJumpsList:
                    reps = jump.count(":")
                    Jump = jump
                    for i in range(reps):
                        FROMRow4,FROMCol4,TORow4,TOCol4=parseMove(Jump)
                        jumpedChecker = chr(((FROMRow4+TORow4)//2)+65) + str((FROMCol4+TOCol4)//2)
                        if jumpedChecker == checkerToJump:  #if enemy can jump that checker of mine
                            enemyReturningJumps.append(jump)
                        Jump=Jump[3:]

                if enemyReturningJumps != []:
                    for jump in enemyReturningJumps:
                        futureBoard3 = copy.deepcopy(futureBoard2)
                        reps = jump.count(":")
                        Jump = jump
                        for i in range(reps):
                            FROMRow5,FROMCol5,TORow5,TOCol5=parseMove(Jump)
                            ownToken = futureBoard3[FROMRow5][FROMCol5]
                            futureBoard3[FROMRow5][FROMCol5] = "e"
                            futureBoard3[(FROMRow5+TORow5)//2][(FROMCol5+TOCol5)//2] = "e"
                            futureBoard3[TORow5][TOCol5] = ownToken
                            Jump=Jump[3:]
                        newOwnNumPieces = numPiecesLeft(futureBoard3,player)

                        
                numOwnPiecesLost = startingOwnNumPieces - newOwnNumPieces
                numEnemyPiecesLost = startingEnemyNumPieces - newEnemyNumPieces
                theDifference = numEnemyPiecesLost - numOwnPiecesLost

                if theDifference < 0:
                    allowJumpage = False
                    return allowJumpage
                if theDifference <= 0:
                    onlyPositiveGainToBeHad = False
                    
        else:  #no return jump, bad
            allowJumpage = False
            return allowJumpage
        
    if downInMaterial:
        if not onlyPositiveGainToBeHad:
            allowJumpage = False
            return allowJumpage
    
    return allowJumpage  #If made it through, it must be true  :)



#-----Heuristic 26: Don't move home row checkers if enemy is right there, waiting to be kinged-----
def disallowEnemyKinging(board,player,movesList,stopPreservingHomeRow):
    if not stopPreservingHomeRow:  #if preserve home row anyway
        return False  #echo it back
    
    stopPreservingHomeRow = True
    if player=="b":
        opponentPlayer = "r"
        homeRow = 7
    else:
        opponentPlayer = "b"
        homeRow = 0

    enemyMovesList=listValidMoves(board,opponentPlayer)
    enemyCrowningMoves=findCrownRowMovesOrJumps(board,opponentPlayer,enemyMovesList.copy())
    if enemyCrowningMoves != []:  #don't even bother trying to stop it
        return True

    for move in movesList:
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        if FROMRow == homeRow and board[FROMRow][FROMCol] == player:  #so, not a king
            futureBoard = copy.deepcopy(board)
            playerToken = futureBoard[FROMRow][FROMCol]
            futureBoard[FROMRow][FROMCol] = "e"
            futureBoard[TORow][TOCol] = playerToken
            
            enemyFutureMovesList=listValidMoves(futureBoard,opponentPlayer)
            enemyFutureCrowningMoves=findCrownRowMovesOrJumps(futureBoard,opponentPlayer,enemyFutureMovesList)
            if enemyFutureCrowningMoves != []:  #if enemy could then crown
                stopPreservingHomeRow = False
                return stopPreservingHomeRow
        else:
            continue

    return stopPreservingHomeRow


#-----Heuristic 27: At endgame, avoid death squares-----
def avoidDeathSquares(board,player,movesList):
    deathSquares = [[7,7],[6,6],[0,0],[1,1],[7,3],[7,5],[6,4],[0,2],[0,4],[1,3],[3,7],[5,7],[4,6],[2,0],[4,0],[3,1],[2,2],[5,5]]
    for move in movesList.copy():
        FROMRow,FROMCol,TORow,TOCol=parseMove(move)
        endSquare = [int(TORow),int(TOCol)]
        if endSquare in deathSquares:
            movesList.remove(move)
    #print(movesList)
    return movesList


    

def getValidMove(board,player):
    if player=="b":
        playerName="black"
        opponentPlayer = "r"
    else:
        playerName="red"
        opponentPlayer = "b"
        
    movesList=listValidMoves(board,player)
    jumpsList=listSingleJumps(board,player)
    jumpsList=listMultipleJumps(board,player,jumpsList)
    crowningJumps=findCrownRowMovesOrJumps(board,player,jumpsList.copy())
    crowningMoves=findCrownRowMovesOrJumps(board,player,movesList.copy())

    encroachMoves, movesThatMoveClosest = encroachingMoves(board,player,movesList.copy())
    antiEncroachMoves = ANTIencroachingMoves(board,player,movesList.copy())
    lastTrapMoves = findLastTrap(board,player,encroachMoves.copy())
    
    bestJumps,highestEnemyLoss = findBestJumps(board,player,jumpsList.copy())
    safeJumps = findSafeJumps(board,player,jumpsList.copy())
    safeBestJumps = findSafeJumps(board,player,bestJumps.copy())

    sideColumnMoves = findSideColumnMoves(board,movesList.copy())
    movesThatDontMessWithHomeRow = movesNotInvolvingHomeRowCheckers(board,player,movesList.copy())
    safeMoves = findSafeMoves(board,player,movesList.copy())
    safeMovesToAvoidBeingJumped,prioritizedAvoidingMoves = findSafeMovesForEndangeredCheckers(board,player,movesList.copy())
    prioritizedAvoidingMoves = findSafeMoves(board,player,prioritizedAvoidingMoves.copy())

    sacrificeMoves,bestSacs,tradeoffMoves = findSacrificesAndTradeoffs(board,player,movesList)
    makeTradeoffs = doTradeoffs(board,player)
    stopPreservingHomeRow, encroach, downInMaterial, oneKingLeft = determineStatus(board,player)
    
    movesThatDontMoveIntoAnEnemySac, movesThatDontMoveIntoAnEnemyTradeoff, movesThatEliminateEnemySacs, movesThatEliminateEnemyTradeoffs = avoidEnemySacsAndTradeoffs(board,player,movesList.copy())
    thereIsASacToAvoidNow, thereIsASacToAvoid = lookForEnemySacs(board,player,movesList.copy())

    enemyMovesList=listValidMoves(board,opponentPlayer)
    enemyJumpsList=listSingleJumps(board,opponentPlayer)
    enemyJumpsList=listMultipleJumps(board,opponentPlayer,enemyJumpsList)
    enemyCrowningJumps=findCrownRowMovesOrJumps(board,opponentPlayer,enemyJumpsList.copy())
    enemyCrowningMoves=findCrownRowMovesOrJumps(board,opponentPlayer,enemyMovesList.copy())

    stopPreservingHomeRow = disallowEnemyKinging(board,player,safeMoves.copy(),stopPreservingHomeRow)
    #printDebugInfo("stopPreservingHomeRow",stopPreservingHomeRow,False)
    #allowJumpage = considerAllowingEnemyJump(board,player,enemyJumpsList.copy(),downInMaterial)

    movesThatBlockEnemyJumps,preferredMovesThatBlockEnemyJumps,jumpsThatBlockEnemyJumps,preferredJumpsThatBlockEnemyJumps,movesThatBlockEnemyCrowningJumps,jumpsThatBlockEnemyCrowningJumps,movesThatBlockEnemyCrowningMoves,jumpsThatBlockEnemyCrowningMoves = findBlockingMoves(board,player,enemyJumpsList.copy(),enemyCrowningJumps.copy(),enemyCrowningMoves.copy(),movesList.copy(),jumpsList.copy())
    preferredSafeBlockingMoves = findSafeMoves(board,player,preferredMovesThatBlockEnemyJumps.copy()) 
    safeBlockingMoves = findSafeMoves(board,player,movesThatBlockEnemyJumps.copy())    
    #print("ONE KING LEFT",oneKingLeft)
    #print("ENCROACH",encroach)
    #print()
        
    if DEBUG:
        print("----Status----")
        print("TRADEOFFS:",makeTradeoffs)
        print("DON'T PRESERVE HOME:",stopPreservingHomeRow)
        print("DOWN MATERIAL",downInMaterial)
        print("SAC TO AVOID",thereIsASacToAvoid)
        print("ONE KING LEFT",oneKingLeft)
        #print("ALLOW JUMPAGE",allowJumpage)
        print()
        print("----Own moves----")
        print("MOVES", movesList)
        print("JUMPS", jumpsList)
        print("CROWN MOVES", crowningMoves)
        print("CROWN JUMPS", crowningJumps)
        print("SAFE MOVES", safeMoves)
        print("SACRIFICE MOVES", sacrificeMoves)
        print("BEST SACRIFICE MOVES",bestSacs)
        print("TRADEOFF MOVES", tradeoffMoves)
        print("SAFE JUMPS",safeJumps)
        print("BEST JUMPS",bestJumps)
        print("AVOIDING MOVES",safeMovesToAvoidBeingJumped)
        print("BEST AVOIDING MOVES",prioritizedAvoidingMoves)
        print("ENCROACHING MOVES",encroachMoves)
        print("LAST TRAP MOVE",lastTrapMoves)
        print("AVOID SAC",movesThatDontMoveIntoAnEnemySac)
        print("ELIMINATE SAC",movesThatEliminateEnemySacs)
        print("AVOID TRADEOFF",movesThatDontMoveIntoAnEnemyTradeoff)
        print("ELIMINATE TRADEOFF",movesThatEliminateEnemyTradeoffs)
        print()
        print("----Opponent's moves----")
        print("ENEMY MOVES", enemyMovesList)
        print("ENEMY JUMPS", enemyJumpsList)
        print("ENEMY CROWN MOVES", enemyCrowningMoves)
        print("ENEMY CROWN JUMPS", enemyCrowningJumps)
        print()
        print("----Potential blocking moves----")
        print("MOVES TO BLOCK JUMPS", movesThatBlockEnemyJumps)
        print("JUMPS TO BLOCK JUMPS", jumpsThatBlockEnemyJumps)
        print("MOVES TO BLOCK CROWN JUMPS", movesThatBlockEnemyCrowningJumps)
        print("JUMPS TO BLOCK CROWN JUMPS", jumpsThatBlockEnemyCrowningJumps)
        print("MOVES TO BLOCK CROWN MOVES", movesThatBlockEnemyCrowningMoves)
        print("JUMPS TO BLOCK CROWN MOVES", jumpsThatBlockEnemyCrowningMoves)
        print("PREFERRED BLOCKS",preferredSafeBlockingMoves)
        print()
    
    while True:

#the heirarchy:

        
    #check jumps:

        #Take a crown jump...
        if crowningJumps != []:
            if findJumpsThatJumpEnemyKingsIn(board,crowningJumps) != []:
                jumps = findLongestJumpsOf(findJumpsThatJumpEnemyKingsIn(board,crowningJumps))
                return jumps[random.randrange(0,len(jumps))]
            return findLongestJumpsOf(crowningJumps)[random.randrange(0,len(findLongestJumpsOf(crowningJumps)))]
            
        #Jump to block an enemy crowning jump...
        elif jumpsThatBlockEnemyCrowningJumps != []:
            if findJumpsThatJumpEnemyKingsIn(board,jumpsThatBlockEnemyCrowningJumps) != []:
                jumps = findLongestJumpsOf(findJumpsThatJumpEnemyKingsIn(board,jumpsThatBlockEnemyCrowningJumps))
                return jumps[random.randrange(0,len(jumps))]
            return findLongestJumpsOf(jumpsThatBlockEnemyCrowningJumps)[random.randrange(0,len(findLongestJumpsOf(jumpsThatBlockEnemyCrowningJumps)))]
            
        #Jump to block an enemy crowning move...
        elif jumpsThatBlockEnemyCrowningMoves != []:
            if findJumpsThatJumpEnemyKingsIn(board,jumpsThatBlockEnemyCrowningMoves) != []:
                jumps = findLongestJumpsOf(findJumpsThatJumpEnemyKingsIn(board,jumpsThatBlockEnemyCrowningMoves))
                return jumps[random.randrange(0,len(jumps))]
            return findLongestJumpsOf(jumpsThatBlockEnemyCrowningMoves)[random.randrange(0,len(findLongestJumpsOf(jumpsThatBlockEnemyCrowningMoves)))]
            
        #Jump to block an enemy jump...
        elif preferredJumpsThatBlockEnemyJumps != []:
            return preferredJumpsThatBlockEnemyJumps[random.randrange(0,len(preferredJumpsThatBlockEnemyJumps))]
        
        elif jumpsThatBlockEnemyJumps != []:
            if findJumpsThatJumpEnemyKingsIn(board,jumpsThatBlockEnemyJumps) != []:
                jumps = findLongestJumpsOf(findJumpsThatJumpEnemyKingsIn(board,jumpsThatBlockEnemyJumps))
                return jumps[random.randrange(0,len(jumps))]
            return findLongestJumpsOf(jumpsThatBlockEnemyJumps)[random.randrange(0,len(findLongestJumpsOf(jumpsThatBlockEnemyJumps)))]
            
        #Take a standard jump...
        elif jumpsList != []:
            if highestEnemyLoss > 2:
                return bestJumps[random.randrange(0,len(bestJumps))]
            if safeBestJumps != []:
                return safeBestJumps[random.randrange(0,len(safeBestJumps))]
            if bestJumps != []:
                return bestJumps[random.randrange(0,len(bestJumps))]
            
            return jumpsList[random.randrange(0,len(jumpsList))]
        

    #check moves, no jumps available:
        
        #Take a sacrificing move...
        elif bestSacs != []:
            return bestSacs[random.randrange(0,len(bestSacs))]
        elif sacrificeMoves != []:
            return sacrificeMoves[random.randrange(0,len(sacrificeMoves))]

        #Take a crowning move...
        elif crowningMoves != []:
            preferredCrowningMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,crowningMoves.copy(),downInMaterial)
            if preferredCrowningMoves != []:
                return preferredCrowningMoves[random.randrange(0,len(preferredCrowningMoves))]
            
            return crowningMoves[random.randrange(0,len(crowningMoves))]
        
        #Move to block an enemy crowning jump...
        elif movesThatBlockEnemyCrowningJumps != []:
            return movesThatBlockEnemyCrowningJumps[random.randrange(0,len(movesThatBlockEnemyCrowningJumps))]
        
        #Move to block an enemy crowning move...
        elif movesThatBlockEnemyCrowningMoves != []:
            return movesThatBlockEnemyCrowningMoves[random.randrange(0,len(movesThatBlockEnemyCrowningMoves))]

        #Take a safe avoiding move...
        if safeMovesToAvoidBeingJumped != []:
            if prioritizedAvoidingMoves != []:
                return prioritizedAvoidingMoves[random.randrange(0,len(prioritizedAvoidingMoves))]
            return safeMovesToAvoidBeingJumped[random.randrange(0,len(safeMovesToAvoidBeingJumped))]
        
        #Move to block an enemy jump, but do it safely...
        elif preferredSafeBlockingMoves != []:
            block_AND_avoidSacs,block_AND_avoidTradeoff,cTemp,dTemp = avoidEnemySacsAndTradeoffs(board,player,preferredSafeBlockingMoves.copy())
            if thereIsASacToAvoid and block_AND_avoidSacs != []:
                return block_AND_avoidSacs[random.randrange(0,len(block_AND_avoidSacs))]
            if downInMaterial and block_AND_avoidTradeoff != []:
                return block_AND_avoidTradeoff[random.randrange(0,len(block_AND_avoidTradeoff))]
            return preferredSafeBlockingMoves[random.randrange(0,len(preferredSafeBlockingMoves))]

        elif safeBlockingMoves != []:
            safe_AND_avoidSacs,safe_AND_avoidTradeoff,cTemp,dTemp = avoidEnemySacsAndTradeoffs(board,player,safeBlockingMoves.copy())
            if thereIsASacToAvoid and safe_AND_avoidSacs != []:
                return safe_AND_avoidSacs[random.randrange(0,len(safe_AND_avoidSacs))]
            if downInMaterial and safe_AND_avoidTradeoff != []:
                return safe_AND_avoidTradeoff[random.randrange(0,len(safe_AND_avoidTradeoff))]
            return safeBlockingMoves[random.randrange(0,len(safeBlockingMoves))]



        #Avoiding sacs and tradeoffs:
        
        #Take tradeoffs when ahead...
        elif makeTradeoffs and tradeoffMoves != []:
            return tradeoffMoves[random.randrange(0,len(tradeoffMoves))]

        #Move to get rid of an enemy sac move that is on their next turn...
        elif thereIsASacToAvoidNow and movesThatEliminateEnemySacs != []:
            aTemp,bTemp,movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves,dTemp = avoidEnemySacsAndTradeoffs(board,player,findSideColumnMoves(board,movesThatDontMessWithHomeRow.copy()))
            aTemp,bTemp,movesThatEliminateEnemySacs_AND_sideColumnMoves,dTemp = avoidEnemySacsAndTradeoffs(board,player,sideColumnMoves.copy())
            aTemp,bTemp,movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow,dTemp = avoidEnemySacsAndTradeoffs(board,player,movesThatDontMessWithHomeRow.copy())

            preferred_movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves.copy(),downInMaterial)
            preferred_movesThatEliminateEnemySacs_AND_sideColumnMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatEliminateEnemySacs_AND_sideColumnMoves.copy(),downInMaterial)
            preferred_movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow.copy(),downInMaterial)
            preferred_movesThatEliminateEnemySacs = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatEliminateEnemySacs.copy(),downInMaterial)

            if preferred_movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves != [] and not stopPreservingHomeRow:
                return preferred_movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves[random.randrange(0,len(preferred_movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves))]
            if movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves != [] and not stopPreservingHomeRow:
                return movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves[random.randrange(0,len(movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves))]

            if preferred_movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow != [] and not stopPreservingHomeRow:
                return preferred_movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow[random.randrange(0,len(preferred_movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow))]
            if movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow != [] and not stopPreservingHomeRow:
                return movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow[random.randrange(0,len(movesThatEliminateEnemySacs_AND_movesThatDontMessWithHomeRow))]

            if preferred_movesThatEliminateEnemySacs_AND_sideColumnMoves != []:
                return preferred_movesThatEliminateEnemySacs_AND_sideColumnMoves[random.randrange(0,len(preferred_movesThatEliminateEnemySacs_AND_sideColumnMoves))]
            #if movesThatEliminateEnemySacs_AND_sideColumnMoves != []:
                #return movesThatEliminateEnemySacs_AND_sideColumnMoves[random.randrange(0,len(movesThatEliminateEnemySacs_AND_sideColumnMoves))]
            
            if preferred_movesThatEliminateEnemySacs != []:
                return preferred_movesThatEliminateEnemySacs[random.randrange(0,len(preferred_movesThatEliminateEnemySacs))]
            
            return movesThatEliminateEnemySacs[random.randrange(0,len(movesThatEliminateEnemySacs))]


        #Avoid moving into an enemy sac...
        elif thereIsASacToAvoid and movesThatDontMoveIntoAnEnemySac != []:
            movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves,bTemp,cTemp,dTemp = avoidEnemySacsAndTradeoffs(board,player,findSideColumnMoves(board,movesThatDontMessWithHomeRow.copy()))
            movesThatDontMoveIntoAnEnemySac_AND_sideColumnMoves,bTemp,cTemp,dTemp = avoidEnemySacsAndTradeoffs(board,player,sideColumnMoves.copy())
            movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow,bTemp,cTemp,dTemp = avoidEnemySacsAndTradeoffs(board,player,movesThatDontMessWithHomeRow.copy())

            preferred_movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves.copy(),downInMaterial)
            preferred_movesThatDontMoveIntoAnEnemySac_AND_sideColumnMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatDontMoveIntoAnEnemySac_AND_sideColumnMoves.copy(),downInMaterial)
            preferred_movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow.copy(),downInMaterial)
            preferred_movesThatDontMoveIntoAnEnemySac = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatDontMoveIntoAnEnemySac.copy(),downInMaterial)

            if preferred_movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves != [] and not stopPreservingHomeRow:
                return preferred_movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves[random.randrange(0,len(preferred_movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves))]
            if movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves != [] and not stopPreservingHomeRow:
                return movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves[random.randrange(0,len(movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves))]

            if preferred_movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow != [] and not stopPreservingHomeRow:
                return preferred_movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow[random.randrange(0,len(preferred_movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow))]
            if movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow != [] and not stopPreservingHomeRow:
                return movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow[random.randrange(0,len(movesThatDontMoveIntoAnEnemySac_AND_movesThatDontMessWithHomeRow))]

            if preferred_movesThatDontMoveIntoAnEnemySac_AND_sideColumnMoves != []:
                return preferred_movesThatDontMoveIntoAnEnemySac_AND_sideColumnMoves[random.randrange(0,len(preferred_movesThatDontMoveIntoAnEnemySac_AND_sideColumnMoves))]
            #if movesThatDontMoveIntoAnEnemySac_AND_sideColumnMoves != []:
                #return movesThatDontMoveIntoAnEnemySac_AND_sideColumnMoves[random.randrange(0,len(movesThatDontMoveIntoAnEnemySac_AND_sideColumnMoves))]

            if preferred_movesThatDontMoveIntoAnEnemySac != []:
                return preferred_movesThatDontMoveIntoAnEnemySac[random.randrange(0,len(preferred_movesThatDontMoveIntoAnEnemySac))]

            return movesThatDontMoveIntoAnEnemySac[random.randrange(0,len(movesThatDontMoveIntoAnEnemySac))]


        #Move to get rid of an enemy tradeoff move that is on their next turn if down in material...
        elif downInMaterial and movesThatEliminateEnemyTradeoffs != []:
            aTemp,bTemp,cTemp,movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves = avoidEnemySacsAndTradeoffs(board,player,findSideColumnMoves(board,movesThatDontMessWithHomeRow.copy()))
            aTemp,bTemp,cTemp,movesThatEliminateEnemyTradeoffs_AND_sideColumnMoves = avoidEnemySacsAndTradeoffs(board,player,sideColumnMoves.copy())
            aTemp,bTemp,cTemp,movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow = avoidEnemySacsAndTradeoffs(board,player,movesThatDontMessWithHomeRow.copy())

            preferred_movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves.copy(),downInMaterial)
            preferred_movesThatEliminateEnemyTradeoffs_AND_sideColumnMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatEliminateEnemyTradeoffs_AND_sideColumnMoves.copy(),downInMaterial)
            preferred_movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow.copy(),downInMaterial)
            preferred_movesThatEliminateEnemyTradeoffs = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatEliminateEnemyTradeoffs.copy(),downInMaterial)

            if preferred_movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves != [] and not stopPreservingHomeRow:
                return preferred_movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves[random.randrange(0,len(preferred_movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves))]
            if movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves != [] and not stopPreservingHomeRow:
                return movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves[random.randrange(0,len(movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves))]

            if preferred_movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow != [] and not stopPreservingHomeRow:
                return preferred_movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow[random.randrange(0,len(preferred_movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow))]
            if movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow != [] and not stopPreservingHomeRow:
                return movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow[random.randrange(0,len(movesThatEliminateEnemyTradeoffs_AND_movesThatDontMessWithHomeRow))]

            if preferred_movesThatEliminateEnemyTradeoffs_AND_sideColumnMoves != []:
                return preferred_movesThatEliminateEnemyTradeoffs_AND_sideColumnMoves[random.randrange(0,len(preferred_movesThatEliminateEnemyTradeoffs_AND_sideColumnMoves))]
            #if movesThatEliminateEnemyTradeoffs_AND_sideColumnMoves != []:
                #return movesThatEliminateEnemyTradeoffs_AND_sideColumnMoves[random.randrange(0,len(movesThatEliminateEnemyTradeoffs_AND_sideColumnMoves))]

            if preferred_movesThatEliminateEnemyTradeoffs != []:
                return preferred_movesThatEliminateEnemyTradeoffs[random.randrange(0,len(preferred_movesThatEliminateEnemyTradeoffs))]
            
            return movesThatEliminateEnemyTradeoffs[random.randrange(0,len(movesThatEliminateEnemyTradeoffs))]
        

        #If down in material, move to avoid an enemy tradeoff that is on their next turn...
        elif downInMaterial and movesThatDontMoveIntoAnEnemyTradeoff != []:
            aTemp,movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves,cTemp,dTemp = avoidEnemySacsAndTradeoffs(board,player,findSideColumnMoves(board,movesThatDontMessWithHomeRow.copy()))
            aTemp,movesThatDontMoveIntoAnEnemyTradeoff_AND_sideColumnMoves,cTemp,dTemp = avoidEnemySacsAndTradeoffs(board,player,sideColumnMoves.copy())
            aTemp,movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow,cTemp,dTemp = avoidEnemySacsAndTradeoffs(board,player,movesThatDontMessWithHomeRow.copy())

            preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves.copy(),downInMaterial)
            preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_sideColumnMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatDontMoveIntoAnEnemyTradeoff_AND_sideColumnMoves.copy(),downInMaterial)
            preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow.copy(),downInMaterial)
            preferred_movesThatDontMoveIntoAnEnemyTradeoff = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,movesThatDontMoveIntoAnEnemyTradeoff.copy(),downInMaterial)

            if preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves != [] and not stopPreservingHomeRow:
                return preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves[random.randrange(0,len(preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves))]
            if movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves != [] and not stopPreservingHomeRow:
                return movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves[random.randrange(0,len(movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves))]

            if preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow != [] and not stopPreservingHomeRow:
                return preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow[random.randrange(0,len(preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow))]
            if movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow != [] and not stopPreservingHomeRow:
                return movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow[random.randrange(0,len(movesThatDontMoveIntoAnEnemyTradeoff_AND_movesThatDontMessWithHomeRow))]

            if preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_sideColumnMoves != []:
                return preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_sideColumnMoves[random.randrange(0,len(preferred_movesThatDontMoveIntoAnEnemyTradeoff_AND_sideColumnMoves))]
            #if movesThatDontMoveIntoAnEnemyTradeoff_AND_sideColumnMoves != []:
                #return movesThatDontMoveIntoAnEnemyTradeoff_AND_sideColumnMoves[random.randrange(0,len(movesThatDontMoveIntoAnEnemyTradeoff_AND_sideColumnMoves))]

            if preferred_movesThatDontMoveIntoAnEnemyTradeoff != []:
                return preferred_movesThatDontMoveIntoAnEnemyTradeoff[random.randrange(0,len(preferred_movesThatDontMoveIntoAnEnemyTradeoff))]
            
            return movesThatDontMoveIntoAnEnemyTradeoff[random.randrange(0,len(movesThatDontMoveIntoAnEnemyTradeoff))]


        
        #Take a standard move...
        elif movesList != []:
            if safeMoves != []:
                safeMoves_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves = findSafeMoves(board,player,findSideColumnMoves(board,movesThatDontMessWithHomeRow.copy()))
                safeMoves_AND_movesThatDontMessWithHomeRow = findSafeMoves(board,player,movesThatDontMessWithHomeRow.copy())

                preferred_safeMoves_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,safeMoves_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves.copy(),downInMaterial)
                preferred_safeMoves_AND_movesThatDontMessWithHomeRow = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,safeMoves_AND_movesThatDontMessWithHomeRow.copy(),downInMaterial)
                preferred_sideColumnMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,sideColumnMoves.copy(),downInMaterial)
                preferred_safeMoves = removeMovesThatMakePlayerBeForcedIntoUnwantedJump(board,player,safeMoves.copy(),downInMaterial)
                
                if preferred_safeMoves_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves != [] and not stopPreservingHomeRow:
                    return preferred_safeMoves_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves[random.randrange(0,len(preferred_safeMoves_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves))]
                if safeMoves_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves != [] and not stopPreservingHomeRow:
                    return safeMoves_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves[random.randrange(0,len(safeMoves_AND_movesThatDontMessWithHomeRow_AND_sideColumnMoves))]

                if preferred_safeMoves_AND_movesThatDontMessWithHomeRow != [] and not stopPreservingHomeRow:
                    return preferred_safeMoves_AND_movesThatDontMessWithHomeRow[random.randrange(0,len(preferred_safeMoves_AND_movesThatDontMessWithHomeRow))]
                if safeMoves_AND_movesThatDontMessWithHomeRow != [] and not stopPreservingHomeRow:
                    return safeMoves_AND_movesThatDontMessWithHomeRow[random.randrange(0,len(safeMoves_AND_movesThatDontMessWithHomeRow))]

                if preferred_sideColumnMoves != []:
                    return preferred_sideColumnMoves[random.randrange(0,len(preferred_sideColumnMoves))]
                #if sideColumnMoves != []:
                    #return sideColumnMoves[random.randrange(0,len(sideColumnMoves))]
                
                #Take a trapping move to win
                #print(lastTrapMoves)
                if oneKingLeft and lastTrapMoves != []:
                    return lastTrapMoves[random.randrange(0,len(lastTrapMoves))]
                
                #Encroach with king
                safeEncroachMoves = avoidDeathSquares(board,player,encroachMoves.copy())
                safeClosestMoves = avoidDeathSquares(board,player,movesThatMoveClosest.copy())
                if oneKingLeft and encroach and safeClosestMoves != []:
                    return safeClosestMoves[random.randrange(0,len(safeClosestMoves))]
                
                if oneKingLeft and encroach and safeEncroachMoves != []:
                    return safeEncroachMoves[random.randrange(0,len(safeEncroachMoves))]

                if oneKingLeft and not encroach and antiEncroachMoves != []:
                    return antiEncroachMoves[random.randrange(0,len(antiEncroachMoves))]
                
                
                if not oneKingLeft and encroach and encroachMoves != []:
                    return encroachMoves[random.randrange(0,len(encroachMoves))]


                if preferred_safeMoves != []:
                    safeEndgameMoves = avoidDeathSquares(board,player,preferred_safeMoves.copy())
                    if oneKingLeft and safeEndgameMoves != []:
                        return safeEndgameMoves[random.randrange(0,len(safeEndgameMoves))]
                    
                    return preferred_safeMoves[random.randrange(0,len(preferred_safeMoves))]

                safeEndgameMoves = avoidDeathSquares(board,player,safeMoves.copy())
                if oneKingLeft and safeEndgameMoves != []:
                    return safeEndgameMoves[random.randrange(0,len(safeEndgameMoves))]
                
                return safeMoves[random.randrange(0,len(safeMoves))]
                
            if tradeoffMoves != []:
                return tradeoffMoves[random.randrange(0,len(tradeoffMoves))]

            prioritizedMoves = limitTheBleeding(board,player,movesList.copy())
            prioritized_AND_dontMessWithHomeRow = limitTheBleeding(board,player,movesThatDontMessWithHomeRow.copy())
            if prioritized_AND_dontMessWithHomeRow != [] and not stopPreservingHomeRow:
                return prioritized_AND_dontMessWithHomeRow[random.randrange(0,len(prioritized_AND_dontMessWithHomeRow))]
            if prioritizedMoves != []:
                return prioritizedMoves[random.randrange(0,len(prioritizedMoves))]
                
            return movesList[random.randrange(0,len(movesList))]




#NOTE: You should really look at my checkersMain. It's the same as Dr.White's
# but lays out my heuristics very nicely. And my test cases rely on manual input.

#But regardless, here are my instructions:




#---Heuristic #8: Take biggest jump ---   
#checkersMain("HeuristicsTest - TakeBiggestJump.txt",redWinCount,blackWinCount)
    #move H1:G2 to see it always choose the jump of length 3
    # OR move B7:A6 to see that it randomly chooses between the two longest jumps (of length 2)
    #notice that red won't do the single jump in the top right before the other, longer jumps




#---Heuristic #9: Jump an enemy king whenever possible ---      
#checkersMain("HeuristicsTest - JumpKingsIfPossible.txt",redWinCount,blackWinCount)
    #move H1:G2 to see that it will still prefer the single king jump in the top right
    #move F7:E6 to see that it will choose the longest of the jumps that jump enemy kings
    #in short, it will always (at this point) prefer jumping enemy kings, and it will take the longest of those jumps




#---Heuristic #10: Move to side columns if no better move available ---
#checkersMain("HeuristicsTest - MoveToSidesOfBoard.txt",redWinCount,blackWinCount)
    #move the black King around (back and forth) 3 times to see the preference to the board's sides
    #I only have this heuristic for regular, non-king pieces.
    #This is to avoid a king always moving back to where it was before (a side column), getting stuck in a loop.




#---Heuristic #11: Keep home row "guarded" as long as possible ---
#checkersMain("HeuristicsTest - KeepHomeRowIntact.txt",redWinCount,blackWinCount)
    #move G6:H7
    #then do what you can to jump red's two checkers there (should be fairly obvious)
    #watch how red only moves those pieces that are not in the home row.
    #when it has to, it'll break one red checker away from the home row.
    #the side column logic still applies, so red will prefer the side column move




#---Heuristic #12: Don't take a move that sets up for an enemy jump ---
#checkersMain("HeuristicsTest - DontMoveToJumpableSquare.txt",redWinCount,blackWinCount)
    #move the black king in the bottom left around (like 4-5 times).
    #notice how red will only move its king.
    #The other checkers, if they moved, would be endangered, so they do not move.
    
#checkersMain("HeuristicsTest - DontUnBlock.txt",redWinCount,blackWinCount)
    #with the way I coded heuristic 12, the automated player will not "unblock" its own peices
    #In other words, it will not create a jump for the other player
    #move the black king around, notice how red will only move its "free" checker
    #it refuses to move the checker that is blocking black's jump



#---Heuristic #13: Take a move that frees a checker from danger ---
#checkersMain("HeuristicsTest - EndangeredCheckers.txt",redWinCount,blackWinCount)
    #move B3:A2, notice red doing an "avoiding" move
    #move B5:C4, notice this again. It chooses between its "safe" options.
    #move H5:G6 to set up another jump (if red randomly moved and "blocked" this next jump, do C4:D5 to kick that checker away), notice it again.
    #basically, it will prioritize not getting jumped. NOTE: it will still, however, choose kinging moves over avoiding moves (and also blocking moves over avoiding moves)




#MP13

#---Heuristic #14: Take a sacrificing move ---
#checkersMain("HeuristicsTest - Sacrifices.txt",redWinCount,blackWinCount)
    #Move either H3:G4 or H3:G2 to see that it will always choose the sacrifice.
    #It sees that it will gain material and it makes the move.
    
#checkersMain("HeuristicsTest - Sacrifices2.txt",redWinCount,blackWinCount)
    #The sacrifice functionality also works for "unblocking" a checker.
    #Move H7:G6 to see red deviously unblock its own piece as a sacrificing move.

#checkersMain("HeuristicsTest - Sacrifices3.txt",redWinCount,blackWinCount)
    #Move either H3:G2 or H3:G4. Notice how red chooses not just any sacrifice, but the best one (C6:D5).
    #Move the black king again to see another sacrifice.



#---Heuristic #15: Find and take tradeoff moves when ahead or when no safe moves ---
#checkersMain("HeuristicsTest - Tradeoffs.txt",redWinCount,blackWinCount)
    #As you can see, red is up in material.
    #Move B7:C6 to see red force a crazy tradeoff.
    #It'll set up a double jump tradeoff (because I have kings as being worth 2 checkers)
    #Then move E0:D1 (only move) to see red force another tradeoff to win.

#checkersMain("HeuristicsTest - Tradeoffs2.txt",redWinCount,blackWinCount)
    #This example shows how the automatic player "looks ahead" 4 moves to see
    #if it's a sac move (meaning it gains material), or if it will be jumped back at the end.
    #Move H1:G0 to see it happen. It recognizes it as a tradeoff.



#---Heuristic #16: take best option when no safe moves (instead of random choice) ---
#checkersMain("HeuristicsTest - BestRemainingMoves.txt",redWinCount,blackWinCount)
    #Move C6:D7 to fully block in the red king.
    #Notice how red, when presented with no safe moves, will not give up its king.

#checkersMain("HeuristicsTest - BestRemainingMoves2.txt",redWinCount,blackWinCount)
    #Move H5:G4. Once again, red has no safe option.
    #In response, red refuses to allow a double jump with either E2:F1 or E2:F3.
    #It chooses D7:E6, which gives up only one piece, and hopefully frees up some future moves.



#---Heuristic #17: take safe jumps over "unsafe" ones ---
#checkersMain("HeuristicsTest - SafeJumps.txt",redWinCount,blackWinCount)
    #Move the black king in the bottom-left corner
    #Notice how red chooses the "safe" jump (C0:E2) over the jump that results in being jumped back.




#End MP13, extra stuff below


#---Heuristic #18: take best jumps (kind of a rewrite of former heuristics, so I'd call it a bonus) ---
#checkersMain("HeuristicsTest - TakeBestJump.txt",redWinCount,blackWinCount)
    #Move F7:E6, notice how red always chooses H7:F5:D7 since it gains most material (again, kings being worth 2).
    #Then move H1:G2, notice the jump (instead of jumping the black king).
    #Then B5:C6



#---Heuristic #19: Have kings do "encroaching" moves ---
#checkersMain("HeuristicsTest - Encroach.txt",redWinCount,blackWinCount)
    #Move the black checkers around. Watch how the red king intentionally moves toward them.
    #But it still keeps enough distance to always be safe.
    #I imagine this to be more of an endgame thing.



#---Heuristic #20: When 1 or 2 enemy checkers left, find and take trapping moves ---
#checkersMain("HeuristicsTest - LastTrap.txt",redWinCount,blackWinCount)
    #Move black king into the top left corner or into a board edge.
    #Red king follows closely and tries to find a trapping move.
    #For example, move black king into A0. Red should follow and move into C0, C2, or A2.



#---Heuristic #21: Avoid enemy sacs ---
#checkersMain("HeuristicsTest - AvoidEnemySacs.txt",redWinCount,blackWinCount)
    #Okay, so move H5:G4. Red now evaluates every safe move it has and sees if it will result in an enemy sac.
    #B3:C4 would be bad for red, so it avoids that move, taking any other moves available.
    #In this case, red always goes for C6:D7, because it moves into a side column.



#---Heuristic #22: Avoid enemy tradeoffs if down in material ---   
#checkersMain("HeuristicsTest - AvoidEnemyTradeoffs.txt",redWinCount,blackWinCount)
    #Notice how red is down in material; it does not desire to trade off its pieces.
    #Move A0:B1. Notice how red will never let black's G6 checker force a tradeoff.
    #Red always chooses E4:F3 or D5:E6.



#---Heuristic #23: Avoid moving into a square that then forces a bad jump next turn ---   
#checkersMain("HeuristicsTest - AvoidForcedBadJump.txt",redWinCount,blackWinCount)
    #Move black king.
    #Red has the ability to become a king, but should it go to either H3 or H5?
    #As black, move H1:G0. Notice that if red were to go to H3, the game would be lost for red.
    #Black would just allow H3:F1, then it would jump G0:E2 to win.
    #This heuristic makes sure red avoids this.
    #Notice that red always goes to H5.

#checkersMain("HeuristicsTest - AvoidForcedBadJump2.txt",redWinCount,blackWinCount)
    #Move black king.
    #Notice how red never goes C6:D7, because that would allow black to capitalize with a double jump.
    #(G0:H1, red goes D7:F5, then black with G6:E4:C2).



#---Heuristic #24: Avoid moving into a square that then forces a tradeoff next turn when down in material ---
#checkersMain("HeuristicsTest - AvoidForcedTradeoff.txt",redWinCount,blackWinCount)
    #Move black king.
    #Similarly, red denies C6:D7 because red is down in material, and C6:D7 would force a tradeoff.



#     REMOVED    #---Heuristic #25: Don't block or avoid an enemy jump that would result in a gain of material for you ---
           #checkersMain("HeuristicsTest - AllowEnemyJumps.txt",redWinCount,blackWinCount)



#---Heuristic #26: Keep home row intact if enemy trying to king ---
#checkersMain("HeuristicsTest - DisallowKinging.txt",redWinCount,blackWinCount)
    #Move the black king around. Notice how red refuses to move its home row piece.
    #It is preoccupied blocking the black checker from kinging.



#---Heuristic #27: At endgame, avoid death squares ---
#checkersMain("HeuristicsTest - Endgame.txt",redWinCount,blackWinCount)
#checkersMain("HeuristicsTest - Endgame2.txt",redWinCount,blackWinCount)
#checkersMain("HeuristicsTest - Endgame3.txt",redWinCount,blackWinCount)

        
