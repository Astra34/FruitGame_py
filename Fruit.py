from turtle import *
from random import randint
from math import *
import time

class CreateEnv:
    def __init__(self):
        self.window = Screen()  
        self.turtle = Turtle()
        self.turtle_Score = Turtle()
        self.score = 0
        self.turtle.hideturtle()
        self.turtle.speed("fastest")
        self.turtle_Score.hideturtle()
        self.turtle_Score.speed("fastest")
        self.set_Bin()
        self.set_Score()

    def set_Bin(self):
        self.turtle.width(5)
        self.turtle.up()
        self.turtle.goto(150,100)
        self.turtle.down()
        for _ in range(3):
            self.turtle.right(90)
            self.turtle.fd(300)
    
    def set_Score(self):
        self.turtle_Score.up()
        self.turtle_Score.goto(-30,150)
        self.turtle_Score.write(f"Score: {self.score}", align="left", font=("Arial", 12, "normal"))

    def set_Increase_Score(self, increment):
        self.score += increment
        self.turtle_Score.clear()
        self.set_Score()

class Fruit:
    def __init__(self):
        self.lstFruits = {1: ['#FF0000', 1],2: ['#FF007F', 3],3: ['#832600', 6],4: ['#FFC300', 10],5: ['#A56100', 15],6: ['#FF0000', 21],7: ['#66BB44', 28],8: ['#FFB5B4', 36],9: ['#FFFF00', 45],10: ['#BCED91', 55],11: ['#228B22', 66]}
        self.turtle = Turtle()
        self.turtle.start_time = None
        self.turtle.lvl = randint(1, 4)
        self.turtle.speed('fastest')
        self.turtle.shape("circle")
        self.turtle.shapesize(self.turtle.lvl/1.5)
        self.turtle.fillcolor(self.lstFruits[self.turtle.lvl][0])
        self.turtle.up()
        self.turtle.goto(0,120)
        self.turtle.rayon = self.turtle.shapesize()[0]*20/2
        self.turtle.score = self.lstFruits[self.turtle.lvl][1]
        self.turtle.velocity_y = 10
        self.turtle.velocity_x = 10

    def set_upgrade(self, F1):
        if F1.turtle.lvl < 11 :
            self.turtle.lvl += 1
            self.turtle.score = self.lstFruits[self.turtle.lvl][1]
            self.turtle.shapesize(self.turtle.lvl/1.5)
            self.turtle.fillcolor(self.lstFruits[self.turtle.lvl][0])
            self.turtle.rayon = self.turtle.shapesize()[0]*20/2
            F1.turtle.hideturtle() 
            F1.turtle.goto(0,120)
    
    def set_recycle(self, turtle):
        turtle.lvl = randint(1,4)
        turtle.shapesize(turtle.lvl/1.5)
        turtle.fillcolor(self.lstFruits[turtle.lvl][0])
        turtle.rayon = turtle.shapesize()[0]*20/2
        turtle.score = self.lstFruits[turtle.lvl][1]
        turtle.velocity = 10
        turtle.showturtle()

class Game:
    def __init__(self):
        self.nextFruit = [Fruit()]  
        self.dropFruit = []
        self.Window = CreateEnv()
        self.MainLoop()
        self.Window.window.mainloop()

        
    def get_Fruit_Collision(self, F1, F2):
        return F1.turtle.distance(F2.turtle) - F2.turtle.rayon <= F1.turtle.rayon
    
    def set_Move_Fruit(self, event):
        x = event.x - self.Window.window.window_width() / 2
        if self.nextFruit:
            raduis = self.nextFruit[0].turtle.rayon
            if x + raduis < 150 and x - raduis > -150 and self.nextFruit:
                self.nextFruit[0].turtle.goto(x, 120 + raduis)

    def set_Next_Fruit(self, x, y):
        if len(self.nextFruit) > 1:
            self.nextFruit[1].set_recycle((self.nextFruit[1].turtle))
        if self.nextFruit:
            self.dropFruit.append(self.nextFruit.pop(0))
        if not self.nextFruit:
            self.nextFruit.append(Fruit())
    
    def set_Limite_Bin(self):
        for fruit1 in self.dropFruit:
            if fruit1.turtle: 
                if fruit1.turtle.ycor() - fruit1.turtle.rayon > -200:
                    fruit1.turtle.goto(fruit1.turtle.xcor(), fruit1.turtle.ycor() - fruit1.turtle.velocity_y)

                elif fruit1.turtle.ycor() - fruit1.turtle.rayon < -200:
                    fruit1.turtle.goto(fruit1.turtle.xcor(), -200 + fruit1.turtle.rayon)
                
                elif fruit1.turtle.xcor() - fruit1.turtle.rayon < -150:
                    fruit1.turtle.goto(-150 + fruit1.turtle.rayon, fruit1.turtle.ycor())

                elif fruit1.turtle.xcor() + fruit1.turtle.rayon > 150:
                    fruit1.turtle.goto(150 - fruit1.turtle.rayon, fruit1.turtle.ycor())
                

    def set_Merger_Fruit(self):
        for fruit1 in self.dropFruit:
            for fruit2 in self.dropFruit:  
                if fruit1 != fruit2 and self.get_Fruit_Collision(fruit1, fruit2):                    
                    if fruit1.turtle.lvl == fruit2.turtle.lvl:
                        fruit1.set_upgrade(fruit2)
                        self.Window.set_Increase_Score(fruit2.turtle.score)
                        if fruit1.turtle.lvl < 11:
                            obj = self.dropFruit.pop(self.dropFruit.index(fruit2))
                            self.nextFruit.append(obj)
                        else:
                            objs = [self.dropFruit.pop(self.dropFruit.index(fruit2)), self.dropFruit.pop(self.dropFruit.index(fruit1))]
                            self.nextFruit.extend(objs)


    def set_Travel_Fruit(self):
        for fruit1 in self.dropFruit:
            for fruit2 in self.dropFruit:
                if fruit1 != fruit2 and self.get_Fruit_Collision(fruit1, fruit2) and fruit1.turtle.lvl != fruit2.turtle.lvl:

                    # activer 1 system a la fois

                    # system de collision 1( pas fini ou mauvais )
                    # if fruit1.turtle.xcor() >= fruit2.turtle.xcor():
                    #     if -150< fruit1.turtle.xcor()+fruit1.turtle.velocity_x < 150:
                    #         fruit1.turtle.goto(fruit1.turtle.xcor() + fruit1.turtle.velocity_x , fruit1.turtle.ycor())
                    # else:
                    #     if -150< fruit1.turtle.xcor() + fruit1.turtle.velocity_x < 150:
                    #         fruit1.turtle.goto(fruit1.turtle.xcor() - fruit1.turtle.velocity_x, fruit1.turtle.ycor())


                    # system de collision 2 (pas trés avancé)
                    dist = fruit1.turtle.distance(fruit2.turtle) - (fruit1.turtle.rayon + fruit2.turtle.rayon)

                    if fruit1.turtle.ycor() > fruit2.turtle.ycor():
                        fruit1.turtle.goto(fruit1.turtle.xcor(), fruit1.turtle.ycor() - dist + 1)
                        fruit1.turtle.velocity_y = 0

                    else:
                        fruit2.turtle.goto(fruit2.turtle.xcor(), fruit2.turtle.ycor() - dist + 1)
                        fruit2.turtle.velocity_y = 0


    def set_Game_Over(self):
        for fruit in self.dropFruit:
            if fruit.turtle.ycor() + fruit.turtle.rayon > 100 and fruit.turtle.start_time == None:  
                fruit.turtle.start_time = time.time()

            elif fruit.turtle.ycor() + fruit.turtle.rayon < 100:
                fruit.turtle.start_time = None
            
            if fruit.turtle.start_time and time.time() - fruit.turtle.start_time > 3:
                self.Window.window.clear()
                self.Window.turtle_Score.write(f" Game Over ", align="left", font=("Arial", 12, "normal"))
                time.sleep(2)
                self.Window.window.bye()
                
    
    def MainLoop(self):
        self.set_Limite_Bin()
        self.set_Travel_Fruit()
        self.set_Merger_Fruit()
        self.Window.window.getcanvas().bind("<Motion>", self.set_Move_Fruit)
        self.Window.window.onclick(self.set_Next_Fruit)
        self.set_Game_Over()
        self.Window.window.ontimer(self.MainLoop, 1)

Jeu = Game()
