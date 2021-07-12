#never ending game.py
import pygame, sys, random, math,time,os
pygame.init()

w=800
h=600
name="Winning is for losers"
screen=pygame.display.set_mode((w,h))
pygame.display.set_caption(name)
font=pygame.font.SysFont("comicsansms",32)
text=font.render("0",True,(255,255,255))
text_rect=text.get_rect(center=(w-50,50))


hacksMode=False #Super duper secret

class Platform():
    def __init__(self,x,y,width,height,color,_type="normal"):
        """Create a Platform"""
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.type=_type
        if self.type=='moving':
            self.direction=1
            self.color=(255,0,0)

    def runTimePrecedures(self):
        if self.type=="moving":
            if self.direction==1:
                self.y+=random.randint(0,2)
                if self.y>=h-100:
                    self.direction=-1
            else:
                self.y-=random.randint(0,2)
                if self.y<=100:
                    self.direction=1             

playerX=w//2
playerY=h//2
playerRad=25
playerCol=(78,121,234)

moveAmount=1
moveFaster=False
fall=False
movingLeft=False
deletePlatforms=[]
startFalling=False
upMotion=False
defUpCountDown=30
upCountdown=defUpCountDown
defJumpsLeft=2
jumpsLeft=defJumpsLeft
score=0
paused=False

platforms=[Platform(w//2,playerY+int(playerRad*1.5),200,50,(255,0,204)),
           Platform(w//2+400,playerY+int(playerRad*1.5),200,50,(255,0,204)),
           Platform(w//2+800,playerY+int(playerRad*1.5),200,50,(255,0,204))
           ]

input("""
You are the circle. Jump from platform to platform and stay alive as long as possible.
Press spacebar to jump
Press l to make you move faster horizontally
Press p to pause

(Press enter to continue)
""")
screen=pygame.display.set_mode((w,h))


#main loop
while True:
    if startFalling:
        fall=True
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
            quit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and not paused:
                jumpsLeft-=1
                if jumpsLeft>0:
                    upMotion=True
                    fall=False
                    startFalling=True
                    movingLeft=True
                
            elif event.key==pygame.K_l and not paused:
                moveFaster=True

            elif event.key==pygame.K_p:
                paused=not paused
                
            if hacksMode and not paused:
                if event.key==pygame.K_a: playerY+=60; fall=True
                elif event.key==pygame.K_d: playerY-=60
                elif event.key==pygame.K_q: playerY=1234
                
        elif event.type == pygame.KEYUP and not paused:
            if event.key == pygame.K_l:
                moveFaster=False
                
    screen.fill((0,0,0))

    time.sleep(0.03)
    if not paused:
        if upCountdown>0 and upMotion:
            upCountdown-=1
            playerY-=15
        else:
            upCountdown=defUpCountDown
            upMotion=False
    
    for i in range(0,len(platforms)):
        platform=platforms[i]

        if not paused: platform.runTimePrecedures()
        
        if movingLeft and not paused:
            platform.x-=(abs(moveAmount)+abs(int(moveFaster))*2)
            
        if (platform.x+platform.width<=platform.width or platform.width+platform.x<playerX) and not paused:
            deletePlatforms.append(i)

        rect=pygame.draw.rect(screen,platform.color,(platform.x-50,platform.y,platform.width,platform.height))
        player=pygame.draw.circle(screen,playerCol,(playerX,playerY),playerRad)

        #print(abs(player.bottom - rect.top),player.x//2 > rect.left,player.x//2 < rect.right)

        if (not rect.colliderect(player)) and fall and i==0 and not paused:
            playerY+=5
        if rect.colliderect(player) and not paused:
            jumpsLeft=defJumpsLeft
            playerY=rect.top-playerRad
            if upMotion:
                playerY=rect.top-playerRad
            """if platform.type=="hole": and 
                platform.timeleft-=1
                if platform.timeleft==0:
                    deletePlatforms.append(i)"""


    for i in range(len(deletePlatforms)):
        del platforms[i]
        score+=1
        text=font.render(str(score),True,(255,255,255))
        text_rect=text.get_rect(center=(w-50,50))
        platforms.append(Platform(platforms[-1].x+platforms[-1].width+random.randint(30,150),random.randint(50,h-70),random.randint(50,250),random.randint(30,55),(255,0,204),random.choice(["normal","moving"])))    

    deletePlatforms=[]

    screen.blit(text,text_rect)
    if paused:
        pauseText=font.render("Paused",True,(255,255,255))
        pauseText_rect=pauseText.get_rect(center=(w//2,h//2))
        screen.blit(pauseText,pauseText_rect)

    pygame.display.update()

    if playerY>=w+50:
        print("\n"*10)
        print("you lost, try to win next time!\n By the way, you got a score of ",end="")
        print(score)
        pygame.quit()
        sys.exit()
