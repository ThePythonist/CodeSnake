import random
snakeLength = 0
lastmove = 0
name = "RNG Snake v2.1"

def reset():
    pass



def move( myPos, enermyPos, pelletPos ):
    global lastMove, snakeLength

    my_x , my_y = myPos
    en_x , en_y = enermyPos
    pe_x , pe_y = pelletPos

    rightMove = pe_x - my_x
    upMove = pe_y - my_y

    if rightMove > 0:
        if upMove > 0:
            direction = random.choice( ["right" , "up"] )
            lastMove = direction
            return direction
        if upMove < 0:
            direction = random.choice( ["right" , "left"] )
            lastMove = direction
            return direction
        if upMove == 0:
            return "right"
    if rightMove < 0:
        if upMove > 0:
            direction = random.choice( ["left" , "up"] )
            lastMove = direction
            return direction
        if upMove < 0:
            direction = random.choice( ["left" , "down"] )
            lastMove = direction
            return direction
        if upMove == 0:
            direction = "left"
            lastMove = direction
            return direction
    if rightMove == 0:
        if upMove > 0:
            direction = "up"
            lastMove = direction
            return direction
        if upMove < 0:
            direction = "down"
            lastMove = direction
            return direction
        if upMove == 0:
            snakeLength += 1
