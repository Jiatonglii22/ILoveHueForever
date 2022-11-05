#Jiatong Li TP Project 
#Andrew ID: jiatong4 
#Project Title: I LOVE HUE Forever 

from cmu_112_graphics import *
import random
import math 

#############################################
# HELPERS  
#############################################

################# GENERAL HELPERS ########################

def rgbColor(rgb): 
    #translates rgb to something tkinter friendly
    r, g, b = rgb 
    return f'#{r:02x}{g:02x}{b:02x}'

def drawGameIntro(app, canvas): #draws intro screen 
    canvas.create_rectangle(app.width // 8, app.height // 8, 
                            app.width - app.width // 8, app.height - app.height // 8, fill = "#6a6699")
    canvas.create_text(app.width //2, app.height // 3, text = "I LOVE HUE Forever", fill = "white",
                        font = 'times 48 italic')
    canvas.create_text(app.width // 2, app.height // 3 + app.height // 10, text = "Press ' i ' for instructions", 
                        fill = "white", font = 'times 20 underline')
    canvas.create_text(app.width //2, app.height // 2, text = "Press ' e ' for Easy level",
                        fill = "white", font = 'times 30')
    canvas.create_text(app.width //2, app.height // 2 + app.height//8, text = "Press ' m ' for Medium level",
                        fill = "white", font = 'times 30')
    canvas.create_text(app.width //2, app.height // 2 + app.height//4, text = "Press ' h ' for Hard level",
                        fill = "white", font = 'times 30')

def drawInstructions(app, canvas): #draws instructions 
    canvas.create_rectangle(app.width // 8, app.height // 8, 
                            app.width - app.width // 8, app.height - app.height // 8, fill = "#6a6699")
    canvas.create_text(app.width // 2, app.height //3 , text = "How to Play:", fill = "white",
                            font = 'times 48 italic')
    canvas.create_text(app.width // 2, app.height // 3 + app.height // 10, text = "Press ' i ' again to go back", 
                        fill = "white", font = 'times 20 underline')
    canvas.create_text(app.width // 2, app.height // 2, text = "Goal: rearrange the colors to match the hue", 
                            fill = "white", font = 'times 24')
    canvas.create_text(app.width // 2, app.height // 2 + app.height // 8, text = "Click the shapes to switch their colors", 
                            fill = "white", font = 'times 24') 
    canvas.create_text(app.width //2, app.height // 2 + app.height // 8 + app.height // 16, text = "Shapes with dots cannot be moved", 
                            fill = "white", font = 'times 24')
    canvas.create_text(app.width // 2, app.height // 2 + app.height // 8 + app.height // 10, text = "and are already at the right place", 
                            fill = "white", font = 'times 24')
    canvas.create_text(app.width // 2, app.height // 2 + app.height // 3, text = "Press 'spacebar' for a hint if you're stuck!", 
                            fill = "white", font = 'times 24')

def drawWinningState(app, canvas): #draws winning screen 
    canvas.create_rectangle(app.width // 8, app.height // 8, 
                                    app.width - app.width // 8, app.height - app.height // 8, 
                                    fill = "#6a6699")
    canvas.create_text(app.width // 2, app.height // 3, text = "You Win!", fill = "white",
                                font = 'times 48 italic') 
    canvas.create_text(app.width // 2, app.height // 2, text = "Press ' r ' to restart!", 
                                    fill = "white", font = "times 30 italic")
    canvas.create_text(app.width // 2, (app.height // 3) * 2, text = "Number of switches: " + str(app.counter), 
                                fill = "white", font = 'times 30')

def drawBoarder(app, canvas): #draws a boarder 
    x0 = app.margin 
    y0 = app.margin 
    x1 = app.width - app.margin 
    y1 = app.height - app.margin
    canvas.create_rectangle(x0, y0, x1, y1, fill = None, outline = "white")

#below are other functions that draws text to help the player understand how the game works
def getHint(app, canvas): 
    canvas.create_text(app.width // 2, app.height // 15, text = "Press ' spacebar ' for a hint!", 
                        fill = "gray", font = 'times 24')

def drawGoal(app, canvas): 
    canvas.create_text(app.width // 2, app.height // 15, text = "This should be the final result!", 
                        fill = "gray", font = 'times 24')

def getRules(app, canvas): 
    canvas.create_text (app.width // 2, app.height - app.height // 15, text = "Shapes with a dot are at the right place and cannot be moved", 
                        fill = "gray", font = 'times 20')

def drawGameStart(app, canvas): 
    canvas.create_text (app.width // 2, app.height - app.height // 15, text = "Press ' s ' to start the game!", 
                        fill = "gray", font = 'times 24')

def drawScore(app, canvas): 
    canvas.create_text(app.width // 8, app.margin // 2, text = "Score: " + str(app.counter), fill = "gray", font = 'times 20')

def checkGame(app): #checks if game is completed 
    if app.grid == app.solution: 
        app.isGameOver = True 
        app.solutionTimer = 0 

################# ANIMATION ##############################

def drawSolutionAnimation(app, canvas): 
    #draws the completed version to show players what end result should look like + inlcudes animation 
    for row in range(app.rows): 
        for col in range(app.cols):
            color = app.solution[row][col][0]
            drawSolutionCell(app, canvas, row, col, color)

def drawSolutionCell(app, canvas, row, col, color):
    #makes the squares grow smaller and then bigger again as animation 
    decr = app.solutionTimer * 2 
    if app.level == 1: 
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        if app.solutionTimer > 22: 
            canvas.create_rectangle(x0 + decr, y0 + decr, x1 - decr, y1 - decr, fill = app.grid[row][col][0])
        else: 
            canvas.create_rectangle(x0 + decr, y0 + decr, x1 - decr, y1 - decr, fill = color)
            
def drawSelectionAnimation(app, canvas): 
    #draws a bigger version of the selected shape 
    row = app.newSelection[0] 
    col = app.newSelection[1] 
    if app.level == 1: 
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        factor = app.selectionTimer * 10   
        canvas.create_rectangle(x0 - factor, y0 - factor, x1 + factor, y1 + factor, fill = app.grid[row][col][0])
        
################# HINT FUNCTIONS #########################

def getSecondCell(app, startRow, startCol): #gets the other cell in the hint given one of them 
    for row in range(app.rows): 
        for col in range(app.cols): 
            if app.solution[row][col] == app.grid[startRow][startCol]: 
                return (row, col) 

def generateHint(app): #function that generates 2 (row, col) cells as a hint 
    leastMoves = app.rows * app.cols 
    bestCell = (-1, -1) 
    switchToCell = (-1, -1)

    fixedGrid = [[0] * app.cols for i in range(app.rows)]
    for row in range(app.rows): 
        for col in range(app.rows):
            fixedGrid[row][col] = app.grid[row][col] 
            #creates a nondestructive copy of the current grid

    for startRow in range(app.rows): 
        for startCol in range(app.cols): 
            if fixedGrid[startRow][startCol] != app.solution[startRow][startCol]: 
                #if a cell is not at the correct location
                moves = generateHintHelper(app, startRow, startCol, fixedGrid) 
                #get number of moves until optimal state
                if moves < leastMoves: #if least number of moves, update best hint cells
                    leastMoves = moves 
                    bestCell = (startRow, startCol)
                    switchToCell = getSecondCell(app, startRow, startCol)
    return (bestCell, switchToCell)

def generateHintHelper(app, startRow, startCol, grid): #recursive function to generate best hint to reach optimal state
    # FYI: optimal state describes the condition where if player switches two colors, both end up at the correct location 
    # it does not necessarily mean the whole game is solved (can but doesn't have to)
    if grid[startRow][startCol] == app.solution[startRow][startCol]: #color already at the place it should be 
        return 0
    else: #find where the color should go 
        for endRow in range(app.rows): 
            for endCol in range(app.cols):  
                if app.solution[endRow][endCol] == grid[startRow][startCol]: #want to put color at end row and col 
                    #code below changes the colors  
                    temp = grid[endRow][endCol] 
                    grid[endRow][endCol] = grid[startRow][startCol] 
                    grid[startRow][startCol] = temp 
                    #recursively call helper again on the new state (same row and col with different color now) 
                    result = generateHintHelper(app, startRow, startCol, grid)
                    return 1 + result #return number of moves 

def drawHint(app, canvas): #visually indicate what the two hint cells are 
    row = app.hintCell[0] 
    col = app.hintCell[1]
    row2 = app.hintCell2[0] 
    col2 = app.hintCell2[1] 
    if app.level == 1: 
        (x0, y0, x1, y1) = getCellBounds(app, row, col) 
        canvas.create_rectangle(x0, y0, x1, y1, fill = '', outline = "red", width = 5)
        (x0, y0, x1, y1) = getCellBounds(app, row2, col2)
        canvas.create_rectangle(x0, y0, x1, y1, fill = '', outline = "red", width = 5)
    elif app.level == 2: 
        coordinates = app.centerVertices[(row, col)]
        canvas.create_polygon(coordinates, fill = '', outline = "red", width = 5)
        coordinates2 = app.centerVertices[(row2, col2)] 
        canvas.create_polygon(coordinates2, fill = '', outline = "red", width = 5)
    elif app.level == 3:
        coordinates = app.orderedVertices[(row, col)] 
        canvas.create_polygon(coordinates, fill = '', outline = "red", width = 5)
        coordinates2 = app.orderedVertices[(row2, col2)] 
        canvas.create_polygon(coordinates2, fill = '', outline = "red", width = 5)

def checkHint(app): #checks if the player actually followed through with the hint or not 
    checkRow, checkCol = app.hintCell 
    checkRow2, checkCol2 = app.hintCell2
    if (app.grid[checkRow][checkCol][0] == app.solution[checkRow][checkCol][0] or
             app.grid[checkRow2][checkCol2][0] == app.solution[checkRow2][checkCol2][0]): 
        #resets if the player made the change the hint suggested 
        app.hintCell = (-1, -1) 
        app.hintCell2 = (-1, -1) 

################# SQUARES (easy level (to code)) ###################

def drawGrid(app, canvas): #draws grid of squares 
    for row in range(app.rows): 
        for col in range(app.cols):
            color = app.grid[row][col][0]
            drawCell(app, canvas, row, col, color) 

def drawCell(app, canvas, row, col, color): #draws each individual cell 
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = color) 

def drawDot(app, canvas): # draws black dot indicating cells are fixed 
    for row in range(app.rows): 
        for col in range(app.cols): 
            fixedValue = app.grid[row][col][1]
            if fixedValue == True:
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                mid = app.cellSize // 2 
                cx = x0 + mid 
                cy = y0 + mid 
                r = app.cellSize // 25
                canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = "black") 

# Taken from cmu 112 website (https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html)
def getCellBounds(app, row, col): 
    gridWidth = app.width - 2 * app.margin 
    gridHeight = app.height - 2 * app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1) 

#taken from cmu 112 website (https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html)
def getCell(app, x, y): 
    if (not pointInGrid(app, x, y)): 
        return (-1, -1) 
    gridWidth = app.width - 2 * app.margin 
    gridHeight = app.height - 2 * app.margin 
    cellWidth = gridWidth / app.cols 
    cellHeight = gridHeight / app.rows 

    row = int((y - app.margin) / cellHeight) 
    col = int((x - app.margin) / cellWidth) 
    return (row, col) 

# taken from cmu 112 website (https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html)
def pointInGrid(app, x, y): 
    return ((app.margin <= x <= app.width - app.margin) and 
            (app.margin <= y <= app.height - app.margin))

############################# ISOMETRIC (medium level (to code)) ##############################

def getCenters(app): #generate centers that would be the centers of each cell 
    result = []
    for row in range(app.rows): 
        rowCenters = []
        for col in range(app.cols):
            cx = app.margin + app.shapeSize * (col + 1) - app.sizeIncrement 
            cy = app.margin + app.shapeSize * (row + 1) - app.sizeIncrement  
            rowCenters.append((cx, cy))
        result.append(rowCenters)
    return result

def drawCenters(app, canvas): #draw the center if the cell is supposed to be fixed
    for row in range(app.rows): 
        for col in range(app.cols): 
            fixedValue = app.grid[row][col][1] 
            if fixedValue == True: 
                cx = app.centers[row][col][0] 
                cy = app.centers[row][col][1] 
                r = 2
                canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = "black")

def drawSquare1(app, row, col): #draws first type of square
    cx = app.centers[row][col][0] 
    cy = app.centers[row][col][1] 
    x0 = cx - app.sizeIncrement * 3
    y0 = cy - app.sizeIncrement 
    x1 = cx - app.sizeIncrement
    y1 = cy + app.sizeIncrement * 3 
    x2 = cx + app.sizeIncrement * 3 
    y2 = cy + app.sizeIncrement 
    x3 = cx + app.sizeIncrement 
    y3 = cy - app.sizeIncrement * 3
    return [(x0, y0), (x1, y1), (x2, y2), (x3, y3)] 
    
def drawDiamond1(app, row, col): #draws first type of diamond
    cx = app.centers[row][col][0] 
    cy = app.centers[row][col][1] 
    x0 = cx - app.sizeIncrement * 3
    y0 = cy - app.sizeIncrement * 3
    x1 = cx - app.sizeIncrement  
    y1 = cy + app.sizeIncrement 
    x2 = cx + app.sizeIncrement * 3
    y2 = cy + app.sizeIncrement * 3
    x3 = cx + app.sizeIncrement 
    y3 = cy - app.sizeIncrement
    return [(x0, y0), (x1, y1), (x2, y2), (x3, y3)] 
    
def drawSquare2(app, row, col): #draws second type of square
    cx = app.centers[row][col][0] 
    cy = app.centers[row][col][1]
    x0 = cx - app.sizeIncrement
    y0 = cy - app.sizeIncrement * 3 
    x1 = cx - app.sizeIncrement * 3
    y1 = cy + app.sizeIncrement 
    x2 = cx + app.sizeIncrement 
    y2 = cy + app.sizeIncrement * 3 
    x3 = cx + app.sizeIncrement * 3 
    y3 = cy - app.sizeIncrement
    return [(x0, y0), (x1, y1), (x2, y2), (x3, y3)] 

def drawDiamond2(app, row, col): #draws second type of diamond
    cx = app.centers[row][col][0] 
    cy = app.centers[row][col][1]
    x0 = cx - app.sizeIncrement 
    y0 = cy - app.sizeIncrement
    x1 = cx - app.sizeIncrement * 3 
    y1 = cy + app.sizeIncrement * 3
    x2 = cx + app.sizeIncrement 
    y2 = cy + app.sizeIncrement 
    x3 = cx + app.sizeIncrement * 3 
    y3 = cy - app.sizeIncrement * 3
    return [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]  
    
def getCenterVertices(app): #get the vertices of each shape given the center
    #returns a dict mapping centers to their vertices 
    result = {} 
    for row in range(app.rows): 
        for col in range(app.cols): 
            if row % 2 == 0: #even rows
                if col % 2 == 0: #even rows and even col 
                    result[(row, col)] = drawSquare1(app, row, col)
                elif col % 2 == 1: #even rows and odd col 
                    result[(row, col)] = drawDiamond1(app, row, col)
            elif row % 2 == 1: #odd rows
                if col % 2 == 0: #odd rows and even col 
                    result[(row, col)] = drawDiamond2(app, row, col)
                elif col % 2 == 1: #odd row and odd col 
                    result[(row, col)] = drawSquare2(app, row, col)
    return result 

def drawIsometric(app, canvas): #draws the shapes out  
    for row in range(app.rows): 
        for col in range(app.cols): 
            coordinates = app.centerVertices[(row, col)] 
            color = app.grid[row][col][0] 
            canvas.create_polygon(coordinates, fill = color, outline = "black")

def getCenter(app, x, y): #get row and col given x and y coordinate
    #uses minimum distance to the center 
    minDis = app.width // 4
    bestCenter = (-1, -1) 
    for row in range(app.rows): 
        for col in range(app.cols): 
            currCenter = app.centers[row][col]
            currCenterx = currCenter[0] 
            currCentery = currCenter[1] 
            dis = getDistance(x, y, currCenterx, currCentery)
            if dis < minDis: 
                minDis = dis 
                bestCenter = (row, col)
    return bestCenter

def drawSolutionIsometric(app, canvas): #draws what the result should look like 
    for row in range(app.rows): 
        for col in range(app.cols): 
            coordinates = app.centerVertices[(row, col)] 
            canvas.create_polygon(coordinates, fill = app.solution[row][col][0], outline = "black")

#################### VORONOI (hard level (to code)) ###########################

def generateSeeds(app): #generate a 2D list of random seeds: (x, y) coordinates
    result = []
    for row in range(app.rows): 
        rowSeeds = []
        for col in range(app.cols): 
            #sets x and y bounds to randomly pick the cell (so that cells look somewhat like a shape)
            xlower = app.margin + ((app.width - app.margin)//app.cols) * col 
            xhigher = 0 + ((app.width - app.margin)//app.cols) * (col + 1)
            ylower = app.margin + ((app.height - app.margin)//app.rows) * row
            yhigher = 0 + ((app.height - app.margin)//app.rows) * (row + 1)
            #randomly select (x, y) to be the seed 
            seedx = random.randint(xlower, xhigher)
            seedy = random.randint(ylower, yhigher)
            rowSeeds.append((seedx, seedy))
        result.append(rowSeeds)
    return result 

def generateSeedMap(app): #maps coordinates to its closest seed 
    result = {}
    for x in range(0, app.width, app.step): 
        for y in range(0, app.height, app.step): # loop through all x and y by the step 
            min = app.width // 2
            closestSeedRow = 0 
            closestSeedCol = 0  
            for row in range(app.rows): 
                for col in range(app.cols): 
                    currSeed = app.seeds[row][col] # a tuple
                    currSeedx = currSeed[0] 
                    currSeedy = currSeed[1] 
                    dis = getDistance(x, y, currSeedx, currSeedy) 
                    if dis < min:
                        min = dis 
                        closestSeedRow = row 
                        closestSeedCol = col  
            result[(closestSeedRow, closestSeedCol)] = result.get((closestSeedRow, closestSeedCol),[]) + [(x, y)]
    return result 

def drawSeeds(app, canvas): #draws the seeds as dots if the cell is fixed
    for row in range(app.rows): 
        for col in range(app.cols): 
            fixedValue = app.grid[row][col][1]
            if fixedValue == True: 
                cx = app.seeds[row][col][0] 
                cy = app.seeds[row][col][1] 
                r = 2
                canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = "black")

def getSeed(app, x, y): #gets closest seed row and col given x and y value 
    minDis = app.width // 4
    bestSeed = (-1, -1) 
    for row in range(app.rows): 
        for col in range(app.cols): 
            currSeed = app.seeds[row][col] 
            currSeedx = currSeed[0] 
            currSeedy = currSeed[1] 
            dis = getDistance(x, y, currSeedx, currSeedy) 
            if dis < minDis: 
                minDis = dis 
                bestSeed = (row, col)
    return bestSeed

def getDistance(x0, y0, x1, y1): #gets the distance between two points 
    return math.sqrt((x1 - x0)**2 + (y1 - y0)**2)

def getVertices(app): #returns dict with seeds mapping to the vertices of the polygon it makes 
    result = {} 
    for seed in app.seedMap: 
        possibleVertices = app.seedMap[seed]
        seedVertices = getSeedVertices(app, possibleVertices) #list of vertices  
        result[seed] = seedVertices 
    return result 

def getSeedVertices(app, possibleVertices): #takes in list of tuples 
    return getVerticesHelper(app, possibleVertices, [])

def getVerticesHelper(app, possibleVertices, vertices): #returns actual vertices that would draw the polygon
    if possibleVertices == []: 
        return cleanUpVertices(vertices) #remove duplicates and those that are on the inside of the polygon 
    else: #loop through possible vertices (look at first one in index)
        currVertex = possibleVertices[0] 
        currX = possibleVertices[0][0] 
        currY = possibleVertices[0][1] 
        if vertices.count(currVertex) < 4: 
            vertices.append(currVertex)
            topRight = (currX + app.step, currY)
            vertices.append(topRight)
            botLeft = (currX, currY + app.step) 
            vertices.append(botLeft)
            botRight = (currX + app.step, currY + app.step)
            vertices.append(botRight)
            return getVerticesHelper(app, possibleVertices[1:], vertices)
    
def cleanUpVertices(vertices): 
    for vertex in vertices: 
        if vertices.count(vertex) >= 4: #remove it completely 
            vertexToRemove = vertex 
            vertices = [value for value in vertices if value != vertexToRemove]
        elif vertices.count(vertex) > 1: 
            while vertices.count(vertex) > 1: #remove until only 1 left
                vertices.remove(vertex)
    return sorted(vertices)

def orderVertices(app): #put vertices in correct drawing order 
    result = {}
    for seed in app.vertices:  
        unordered = app.vertices[seed] #list of tuples 
        startingPoint = unordered[0]
        res = [startingPoint] 
        result[seed] = intoOrder(app, unordered, startingPoint, res) #takes in unordered list, returns ordered list 
    return result 

#returns the ordered list of vertices so that the polygon can be drawn in tkinter
def intoOrder(app, unordered, startingPoint, result): 
    if len(unordered) == 0:
        return result 
    else: 
        startX = startingPoint[0] 
        startY = startingPoint[1]
        if (startX, startY + app.step) in unordered: 
            result.append((startX, startY + app.step))
            unordered.remove((startX, startY + app.step))
            startingPoint = (startX, startY + app.step) 
            return intoOrder(app, unordered, startingPoint, result)
        elif (startX + app.step, startY) in unordered: 
            result.append((startX + app.step, startY))
            unordered.remove((startX + app.step, startY))
            startingPoint = (startX + app.step, startY)
            return intoOrder(app, unordered, startingPoint, result) 
        elif (startX, startY - app.step) in unordered: 
            result.append((startX, startY - app.step))
            unordered.remove((startX, startY - app.step))
            startingPoint = (startX, startY - app.step) 
            return intoOrder(app, unordered, startingPoint, result)
        elif (startX - app.step, startY) in unordered: 
            result.append((startX - app.step, startY))
            unordered.remove((startX - app.step, startY))
            startingPoint = (startX - app.step, startY)
            return intoOrder(app, unordered, startingPoint, result) 

def drawPolygons(app, canvas): #draws the polygons
    for seed in app.orderedVertices: 
        seedRow = seed[0] 
        seedCol = seed[1]
        vertices = app.orderedVertices[seed] 
        color = app.grid[seedRow][seedCol][0]
        canvas.create_polygon(vertices, fill = color, outline = "black", width = 1) 

def drawSolutionVoronoi(app, canvas): #draws what the result should look like
    for row in range(app.rows): 
        for col in range(app.cols): 
            coordinates = app.orderedVertices[(row, col)] 
            canvas.create_polygon(coordinates, fill = app.solution[row][col][0], outline = "black")

##################################################
# MAIN 
#################################################

def appStarted(app):

    # GENERAL 
    app.isGameOver = False #game over 
    app.drawInstructions = 1 #shows instructions
    app.start = False #shows solution before starting game if False
    app.counter = 0 #counts number of color switches, used as score keeper 
    
    # ANIMATION 
    app.solutionTimer = 0 #animation timer used in switch from showing solution to showing the puzzle 
    app.selectionTimer = 1 #timer used in showing which cell is selected 
    
    # BOARD VARIABLES
    app.margin = app.width // 10 
    app.rows = 7 
    app.cols = 7
    app.numFixed = [False, False, True] #ratio of fixed to unfixed cells (fixed means they cannot be moved in the actual game) 
    app.cellSize = (app.width - (2 * app.margin)) // app.cols #size of cell 
    app.grid = [[0] * app.cols for i in range(app.rows)] #initializes grid 
    app.solution = [[0] * app.cols for i in range(app.rows)] #initializes solution 
    app.hintCell = (-1, -1) #row and col 
    app.hintCell2 = (-1, -1) #row and col 

    # COLOR VARIABLES
    app.rvalue = random.randint(0, 255) #starts with a random r value in rgb
    app.increment = 255 // app.cols # the increment to create hues 
    app.colorsToChange = [] #will put colors to change in this list (i.e. so that cells that are not fixed will have a random color) 

    #creates the solution: 
    for row in range(app.rows): 
        for col in range(app.cols):
            color = rgbColor((app.rvalue, 255 - row * app.increment, 255 - col * app.increment))
            fixedValue = random.choice(app.numFixed)
            app.grid[row][col] = (color, fixedValue) #creates two 2D list of what will be drawn and the solution 
            app.solution[row][col] = (color, fixedValue) 
    
    #scramble the colors in app.grid: 
    for row in range(app.rows): 
        for col in range(app.cols): 
            color = app.grid[row][col][0] 
            fixedValue = app.grid[row][col][1] 
            if fixedValue == False: 
                app.colorsToChange.append(color) #appends colors of cells that are not fixed 

    for row in range(app.rows): 
        for col in range(app.cols): 
            fixedValue = app.grid[row][col][1]
            if fixedValue == False:  
                newColor = random.choice(app.colorsToChange) #get a random color from the list of possible colors available for change 
                app.colorsToChange.remove(newColor) #removes the color from list of possible colors 
                app.grid[row][col] = (newColor, False) #change the corresponding color in app.grid 
    
    # GAME VARIABLES 
    app.prevSelection = (-1, -1) #for selection of cells 
    app.newSelection = (-1, -1) #(row, col) 
    app.level = 0 #indicate the level of the game 
    app.pressedLevel = 0 # each level key should only be able to be pressed once 

    # ISOMETRIC GRID VARIABLES
    app.sizeIncrement = ((app.width - (2 * app.margin)) // 30) #used to calculate centers and find vertices 
    app.shapeSize = app.sizeIncrement * 4 #about 2/3 of actual cell size, used to calculate centers and find vertices 
    app.centers = getCenters(app)
    app.centerVertices = getCenterVertices(app) #maps centers to their vertices 

    # VORONOI GRID VARIABLES
    app.step = 5 #increment of checking coordinates (i.e, instead of checking every x, check x, then x + app.step, etc.)
    app.seeds = generateSeeds(app) #initializes seed list  
    app.seedMap = generateSeedMap(app) #dict that maps seeds to its closest points 
    app.vertices = getVertices(app) # maps each seed to it's polygon vertices (different from closest points) 
    app.orderedVertices = orderVertices(app) #puts vertices in correct drawing order (so that it is drawn properly)
    #app.orderedVertices should be used to draw 

def keyPressed(app, event): 
    #shortcuts:
    if event.key == 'Up': 
        app.level += 1 
    if event.key == "Down": 
        app.level -= 1

    #game: 
    if event.key == 'i': 
        app.drawInstructions += 1 

    if event.key == 'e': 
        app.pressedLevel += 1 
        if app.pressedLevel == 1: 
            app.level = 1
            app.solutionTimer = 0 
        
    if event.key == 'm': 
        app.pressedLevel += 1 
        if app.pressedLevel == 1:
            app.level = 2 

    if event.key == 'h': 
        app.pressedLevel += 1 
        if app.pressedLevel == 1:
            app.level = 3
    
    if event.key == 'Space': #generates hint 
        app.hintCell = generateHint(app)[0] 
        app.hintCell2 = generateHint(app)[1]

    if event.key == 's': #starts game 
        app.start = True 
        
    if event.key == 'r': #restarts game
        appStarted(app)
    
def mousePressed(app, event):
    if app.isGameOver == False: 
        if app.level != 0: #avoids getting error if clicking before game starts 
            #gets row and col of the cell clicked based on level: 
            if app.level == 1: 
                (row, col) = getCell(app, event.x, event.y)
            if app.level == 2: 
                (row, col) = getCenter(app, event.x, event.y)
            if app.level == 3: 
                (row, col) = getSeed(app, event.x, event.y)
            if app.grid[row][col][1] == False: #if the cell selected is not fixed 
                #updates selection cells 
                temp = app.newSelection 
                app.newSelection = (row, col)
                app.prevSelection = temp
                if app.prevSelection != (-1, -1): #if two cells are selected 
                    #switch their colors 
                    oldRow, oldCol = app.prevSelection 
                    newRow, newCol = app.newSelection 
                    oldColor = app.grid[oldRow][oldCol] 
                    newColor = app.grid[newRow][newCol] 
                    app.grid[oldRow][oldCol] = newColor 
                    app.grid[newRow][newCol] = oldColor 
                    #resets the selection cells:
                    app.prevSelection = (-1, -1) 
                    app.newSelection = (-1, -1)
                    #adds to number of switches:
                    app.counter += 1
                    checkHint(app) #checks if player did the hint (doesn't really apply if no hint was generated)
                    
    checkGame(app) #checks if game is solved  

def timerFired(app):
    if app.start == True:
        app.solutionTimer += 1 
    if app.isGameOver == True: 
        app.solutionTimer += 1 

def redrawAll(app, canvas): 
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    if app.level == 0: 
        drawGameIntro(app, canvas)
        drawBoarder(app, canvas)
    else: 
        if app.level == 1:  
            if app.start == False:
                drawGoal(app, canvas) # 'This should be the final result' 
                drawGameStart(app, canvas) # 'Press 's' to start the game'
            if app.solutionTimer < 40:
                drawSolutionAnimation(app, canvas)
            else: 
                drawGrid(app, canvas)
                drawDot(app, canvas)
                getHint(app, canvas)
                getRules(app, canvas)
                if app.hintCell != (-1, -1): 
                    drawHint(app, canvas)  
    
        if app.level == 2:
            if app.start == False:
                drawSolutionIsometric(app, canvas) 
                drawGoal(app, canvas) # 'This should be the final result' 
                drawGameStart(app, canvas) # 'Press 's' to start the game'
            else: 
                drawIsometric(app, canvas) 
                drawCenters(app, canvas)
                getHint(app, canvas)
                getRules(app, canvas) 
            if app.hintCell != (-1, -1): 
                drawHint(app, canvas)  
        
        if app.level == 3: 
            if app.start == False: 
                drawSolutionVoronoi(app, canvas)
                drawGoal(app, canvas) # 'This should be the final result' 
                drawGameStart(app, canvas) # 'Press 's' to start the game'
            else: 
                drawPolygons(app, canvas) 
                drawSeeds(app, canvas)
            if app.hintCell != (-1, -1): 
                drawHint(app, canvas)

    drawScore(app, canvas)

    if app.drawInstructions % 2 == 0: 
            drawInstructions(app, canvas) 
        
    if app.newSelection != (-1, -1): 
        drawSelectionAnimation(app, canvas)
    
    if app.isGameOver == True: 
        if app.level == 1: 
            if app.solutionTimer < 40:  
                drawSolutionAnimation(app, canvas)
            if app.solutionTimer > 60: 
                drawWinningState(app, canvas) 
        else: 
            if app.solutionTimer > 25: 
                drawWinningState(app, canvas)
        
def playHueGame(): 
    runApp(width = 700, height = 700)

playHueGame()

###################### END OF TP PROJECT ######################