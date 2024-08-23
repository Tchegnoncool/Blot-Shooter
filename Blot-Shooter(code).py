from cmu_graphics import *
import random

"""
THis is a fight between Kaido and Luffy. In the begining, these is a sceen showing kaido and luffy.
The user is asked to press space, and if they do, the press space label dissapears before the characters
start moving towards each other, and uppon contact, the screen changes, and we go to a transition screen
baiting the two parties to fight. Instead of circles to represent the players, there are two characters
but you can only win the game by shooting your blot where the original circle would have been. The names of
each attack is displayed as soon as the user lunches the blot. Upon firing an attack, the character laughes.
It they win, the continue laughing until the game is reset.
"""

def onAppStart(app):
    app.kaido = 'cmu://785904/29316394/download__3_-removebg-preview.png'
    app.luffy = 'cmu://785904/29316403/download__4_-removebg-preview.png'
    luffyLaughURL = 'cmu://785904/29317037/luffy_laugh.mp3'
    app.luffyLaugh = Sound(luffyLaughURL)
    kaidoLaughURL = 'cmu://785904/29317053/kaido_laugh.mp3'
    app.kaidoLaugh = Sound(kaidoLaughURL)
    app.luffyVKaido = 'cmu://785904/29316337/images+(4).jpg'
    app.throne = 'cmu://785904/29316541/download+(8).jpg'
    app.width = 600
    app.height = 600
    app.buildingCount = 10
    app.buildingWidth = app.width / app.buildingCount
    app.playerRadius = 15
    app.holeRadius = 35
    startNewGame(app)

def startNewGame(app):
    app.buildingHeights = [random.randrange(50, 250) for _ in range(app.buildingCount)]
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    app.buildingColors = [random.choice(colors) for _ in range(app.buildingCount)]
    # place new player
    cx0 = app.buildingWidth / 2
    cy0 = app.height - app.buildingHeights[0] - app.playerRadius
    cx1 = app.width - cx0
    cy1 = app.height - app.buildingHeights[-1] - app.playerRadius
    app.players = [(cx0, cy0, 'lightblue'), (cx1, cy1, 'pink')]
    app.showBlot = False
    app.currentPlayer = 0
    app.holeRadius = 30
    app.holes = []
    app.moveCharacters = False
    app.transition = False
    app.gameOver = False
    app.moveImages = True
    app.startGame = False
    app.count = 0
    app.moveCharBy = 0
    app.blotCX = 10
    app.blotCY = 10
    app.blotColor = None
    app.blotDX = 5
    app.blotDY = 5
    app.luffyhand = []
    app.showAttack = False
    app.showPressSpace = True
    app.luffyLaugh.pause()
    app.kaidoLaugh.pause()
    
def onKeyPress(app, key):
    if key == 'n':
        startNewGame(app)
    if not app.startGame and key == 'space':
        app.moveCharacters = True
        app.showPressSpace = False

def getBuildingBounds(app, i):
    width = app.width/ app.buildingCount
    height = app.buildingHeights[i]
    left = i * width
    top = app.height - height
    return left, top, width, height

def redrawAll(app):
    if app.startGame:
        drawRect(0, 0, app.width, app.height, fill = 'red')
        if not app.gameOver:
            #draw buildings
            for i in range (app.buildingCount):
                height = app.buildingHeights[i]
                color = app.buildingColors[i]
                left, top, width, height = getBuildingBounds(app, i)
                drawRect(left, top, width, height, fill = color, border = 'black', borderWidth = 5)
            # draw title
            drawLabel('Blot Shooter', 100, 15, size = 20)
            # draw player's turn
            currentPlayer = 'Luffy'
            if app.currentPlayer == 1:
                currentPlayer = 'Kaido'
            drawLabel(f'Current Player: {currentPlayer}', 250, 15, size =20)
            # draw holes
            for cx, cy in app.holes:
                drawCircle(cx, cy, app.holeRadius, fill = 'red')
            # drawBlot
            if app.showBlot:
                if app.currentPlayer == 0:
                    for x, y in app.luffyhand:
                        drawCircle(x, y, app.playerRadius - 5, fill = app.blotColor)
                else:
                    drawCircle(app.blotCX, app.blotCY, app.playerRadius, fill = app.blotColor)
            # draw players
            for player in range (len(app.players)):
                cx, cy, color = app.players[player]
                individual = app.luffy
                if player == 1:
                    individual = app.kaido
                drawImage(individual, cx - 50, cy - 75, width=100, height=100)
            if app.showAttack:
                if app.currentPlayer == 0:
                    drawLabel('GUMMO-GUMMO-NO ELEPHANT GUN', app.width/2, app.height/2, size = 30)
                else:
                    drawLabel('RAIMEI HAKKE', app.width/2, app.height/2, size = 30)
        else:
            drawImage(app.throne, app.width/2, app.height/2, width=600, height=600, align = 'center')
            drawLabel('Game Over!!!!', app.width/2, app.height/2, size = 50, bold = True)
            currentPlayer = 'Luffy'
            if app.currentPlayer == 0:
                currentPlayer = 'Kaido'
            drawLabel(f'Player {currentPlayer} wins!', app.width/2,
                            app.height/2 + 50, size = 50, bold = True)
    elif app.transition:
        drawRect(app.width/2, app.height/2, app.width, app.height,
                    fill = gradient('white', 'red'), align = 'center')
        drawLabel('FIGHT!!!!!!', app.width/2, app.height/2, size = 75)
    else: # Intro Screen
        drawImage(app.luffyVKaido, app.width/2, app.height/2,
                    width=app.width, height =app.height, align = 'center')
        drawLabel('Luffy V Kaido', app. width/2, app.height/2 + 200, size = 70, fill = 'gold')
        if app.showPressSpace:
            drawLabel('Press space to begin', app.width/2, app.height/2, size = 20, fill = 'gold')
        if app.moveCharacters == True:
            drawImage(app.luffy, 50 + app.moveCharBy, app.height/2)
            drawImage(app.kaido, app.width - 300 - app.moveCharBy, app.height/2)

def onMousePress(app, mouseX, mouseY):
    if app.gameOver or app.showBlot:
        if app.player == 0:
            app.luffyLaugh.play(loop=True)
        else:
            app.kaidoLaugh.play(loop=True)
        return
    app.showAttack = True
    app.blotCX, app.blotCY, app.blotColor = app.players[app.currentPlayer]
    app.blotDX = (mouseX - app.blotCX) / 20
    app.blotDY = (mouseY - app.blotCY) / 20
    app.showBlot = True
    if app.currentPlayer == 0:
        app.luffyLaugh.play(loop=False)
    else:
        app.kaidoLaugh.play(loop=False)

def otherPlayerLocation(app):
    player2X, player2Y, player2Color = app.players[1 - app.currentPlayer]
    return player2X, player2Y

def distance(x1, x2, y1, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def onStep(app):
    if app.moveCharacters == True:
        app.count += 1
        if app.count % 10:
            app.moveCharBy += 1
        if app.moveCharBy == 120:
            app.count = 0
            app.moveCharacters = False
            app.transition = True
    if app.transition:
        app.count += 1
        if app.count == 120:
            app.transition = False
            app.startGame = True
    if app.showBlot:
        app.blotCX += app.blotDX
        app.blotCY += app.blotDY
        app.blotDY += 0.8
        app.luffyhand.append([app.blotCX,app.blotCY])
        if (app.blotCX < (0 - app.playerRadius) or app.blotCX > (app.width + app.playerRadius)):
            app.showBlot = False
            app.luffyhand = []
            app.showAttack = False
            app.currentPlayer = 1 - app.currentPlayer
        else:
            p2x, p2y = otherPlayerLocation(app)
            dist = distance(p2x, app.blotCX, p2y, app.blotCY)
            if dist <= 2 * app.playerRadius:
                app.showAttack = False
                app.gameOver = True
                return
            for cx, cy in app.holes: # Draw holes
                dist = distance(app.blotCX, cx, app.blotCY, cy)
                if dist <= app.holeRadius - app.playerRadius:
                    app.showAttack = False
                    return
            for i in range(app.buildingCount): # Building blot intersection
                left, top, width, height = getBuildingBounds(app, i)
                if ((left <= app.blotCX <= (left + width)) and
                        (top <= app.blotCY <= top + height)):
                        app.currentPlayer = 1 - app.currentPlayer
                        app.showBlot = False
                        app.holes.append((app.blotCX, app.blotCY))
                        app.luffyhand = []
                        app.showAttack = False
    
def main():
    runApp()
    
main()