import math
import cv2
import random
import cvzone
import numpy as np

class SnakeGame:
    def __init__(self, pathFood):
        self.points = [] 
        self.lengths = []
        self.currentLength = 0
        self.maxLength = 150
        self.prevHead = 0,0
        self.score = 0
        self.gameOver = False

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood,_ = self.imgFood.shape

        self.foodPoint = 0, 0
        self.randomFoodLocations()

    def randomFoodLocations(self):
        self.foodPoint = random.randint(100,1000), random.randint(100, 600)


    def update(self, imgMain, currentHead):

        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over press 'r' to restart", [300,550],
                               scale=3,thickness=4, colorB=(0,225,0), offset=10)
            
            cvzone.putTextRect(imgMain, f'Your Score:{self.score}', [400,600],
                               scale=3,thickness=4, colorB=(0,225,0),offset=10)
            
        else:
            px,py = self.prevHead
            cx,cy = currentHead

            self.points.append([cx,cy])
            distance = math.hypot(cx-px, cy-py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.prevHead = cx, cy

            # Reduction of length

            if self.currentLength > self.maxLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length

                    self.lengths.pop(i)
                    self.points.pop(i)

                    if self.currentLength < self.maxLength:
                        break

            # Check if snake eats the food
            rx,ry = self.foodPoint
            if rx - self.wFood // 2 <cx<rx + self.wFood // 2 and ry - self.hFood // 2<cy<ry + self.hFood:
                self.randomFoodLocations()
                self.maxLength += 50
                self.score += 1
                print(self.score)



            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i-1],self.points[i],(0,0,225),20)
                cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)    
            
            # Draw Food
            rx, ry = self.foodPoint
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))


            cvzone.putTextRect(imgMain, f"Score: {self.score}", [50,60],
                                scale = 3,thickness=3, offset=10)
            

            # Check if snake collides
            # Use OpenCv function 

            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(imgMain, [pts],False,(0,200,0),3)# Check if snake collides
            # Use OpenCv function 

            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(imgMain, [pts],False,(0,200,0),3)

            minDistance = cv2.pointPolygonTest(pts,(cx,cy),True)

            if -1 <= minDistance <= 1:
                # print("Hit")
                self.gameOver = True
                self.points = [] 
                self.lengths = []
                self.currentLength = 0
                self.maxLength = 150
                self.prevHead = 0,0
                self.score = 0
                self.randomFoodLocations()




        return imgMain


# game = SnakeGame("donut.png")