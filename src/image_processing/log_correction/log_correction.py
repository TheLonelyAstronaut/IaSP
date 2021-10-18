import math

class LogCorrection:
    def setCConstant(self, constant):
        self.brightness = []
        self.constant = constant

        for i in range(256):
            value = round(constant * math.log(1 + i))
            if value > 255:
                value = 255
            self.brightness.append(value)


    def correction(self, image):
        processedImagePixels = []

        for row in image:
            partial = []

            for pixel in row:
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]

                r = self.brightness[r]
                g = self.brightness[g]
                b = self.brightness[b]

                partial.append([r, g, b])

            processedImagePixels.append(partial)

        return processedImagePixels