import math

class RobertsFiltration:
    def __init__(self):
        self.h1 = [0] * 4 #   0  1
        self.h1[1] = 1    #  -1  0
        self.h1[2] = -1   #

        self.h2 = [0] * 4   #  1  0
        self.h2[0] = 1      #  0 -1
        self.h2[3] = -1 

    
    def filter(self, image):
        imageWidth = len(image[0])
        imageHeight = len(image)

        processedImage = []

        for i in range(0, imageHeight - 1):
            processedImagePixel = []

            for j in range(0, imageWidth - 1):
                r = self.h1[0] * image[i, j, 0] + self.h1[1] * image[i, j + 1, 0] + \
                    self.h1[2] * image[i + 1, j, 0] + self.h1[3] * image[i + 1, j + 1, 0]
                g = self.h1[0] * image[i, j, 1] + self.h1[1] * image[i, j + 1, 1] + \
                    self.h1[2] * image[i + 1, j, 1] + self.h1[3] * image[i + 1, j + 1, 1]
                b = self.h1[0] * image[i, j, 2] + self.h1[1] * image[i, j + 1, 2] + \
                    self.h1[2] * image[i + 1, j, 2] + self.h1[3] * image[i + 1, j + 1, 2]

                r = pow(r, 2)
                g = pow(g, 2)
                b = pow(b, 2)

                r2 = self.h2[0] * image[i, j, 0] + self.h2[1] * image[i, j + 1, 0] + \
                    self.h2[2] * image[i + 1, j, 0] + self.h2[3] * image[i + 1, j + 1, 0]
                g2 = self.h2[0] * image[i, j, 1] + self.h2[1] * image[i, j + 1, 1] + \
                    self.h2[2] * image[i + 1, j, 1] + self.h2[3] * image[i + 1, j + 1, 1]
                b2 = self.h2[0] * image[i, j, 2] + self.h2[1] * image[i, j + 1, 2] + \
                    self.h2[2] * image[i + 1, j, 2] + self.h2[3] * image[i + 1, j + 1, 2]

                r2 = pow(r2, 2)
                g2 = pow(g2, 2)
                b2 = pow(b2, 2)

                r = round(math.sqrt(r + r2))
                g = round(math.sqrt(g + g2))
                b = round(math.sqrt(b + b2))

                if r < 0:
                    r = 0
                if g < 0:
                    g = 0
                if b < 0:
                    b = 0

                if r > 255:
                    r = 255
                if g > 255:
                    g = 255
                if b > 255:
                    b = 255
                
                processedImagePixel.append([r, g, b])
            
            processedImage.append(processedImagePixel)

        return processedImage