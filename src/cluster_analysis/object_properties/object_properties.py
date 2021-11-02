import math
from PIL import Image, ImageDraw

class ObjectProperties:
    def __init__(self):
        self.number = 50
        self.maxImageHeight = 300
        self.rotateFactor = 30

    def getObjectProperties(self, labels, areas):
        orientation = 0

        elements = []

        size = len(areas)

        for indexAreas in range(0, size, 1):
            area = self.getObjectArea(labels, areas, indexAreas)

            if area < self.number:
                continue

            perimeter = self.getObjectPerimeter(labels, areas, indexAreas)
            compactness = self.getObjectCompactness(perimeter, area)
            xCenter, yCenter = self.getObjectCenterOfMass(labels, areas[indexAreas], indexAreas)

            self.createImage(labels, areas[indexAreas], indexAreas, "source/")

            heightCur = areas[indexAreas][2] - areas[indexAreas][0]

            widthCur = areas[indexAreas][3] - areas[indexAreas][1]

            if (widthCur <= heightCur):
                newLabels, newAreas = self.rotateImage(labels, areas[indexAreas], indexAreas, -1 * self.rotateFactor, xCenter, yCenter)
                widthPred = newAreas[3] - newAreas[1]

                newLabels, newAreas = self.rotateImage(newLabels, newAreas, indexAreas, 2 * self.rotateFactor, xCenter, yCenter)
                widthNext = newAreas[3] - newAreas[1]

                while not (widthPred >= widthCur and widthNext >= widthCur):
                    widthPred = widthCur
                    widthCur = widthNext
                    newLabels, newAreas = self.rotateImage(newLabels, newAreas, indexAreas, self.rotateFactor, xCenter, yCenter)
                    widthNext = newAreas[3] - newAreas[1]
            else:
                newLabels, newAreas = self.rotateImage(labels, areas[indexAreas], indexAreas, -1 * self.rotateFactor, xCenter,
                                              yCenter)
                heightPred = newAreas[2] - newAreas[0]

                newLabels, newAreas = self.rotateImage(newLabels, newAreas, indexAreas, 2 * self.rotateFactor, xCenter, yCenter)
                heightNext = newAreas[2] - newAreas[0]

                while not (heightPred >= heightCur and heightNext >= heightCur):
                    heightPred = heightCur
                    heightCur = heightNext
                    newLabels, newAreas = self.rotateImage(newLabels, newAreas, indexAreas, self.rotateFactor, xCenter, yCenter)
                    heightNext = newAreas[2] - newAreas[0]

            newLabels, newAreas = self.rotateImage(newLabels, newAreas, indexAreas, -1 * self.rotateFactor, xCenter, yCenter)

            self.createImage(newLabels, newAreas, indexAreas, "rotated/")

            xCenter, yCenter = self.getObjectCenterOfMass(newLabels, newAreas, indexAreas)
            xCenter, yCenter, orientation = self.getCenterOfMass(xCenter, yCenter, newAreas)
            staticMoment11 = self.getObjectStaticMoment(newLabels, newAreas, indexAreas, xCenter, yCenter, 1, 1, orientation)
            staticMoment20 = self.getObjectStaticMoment(newLabels, newAreas, indexAreas, xCenter, yCenter, 2, 0, orientation)
            staticMoment02 = self.getObjectStaticMoment(newLabels, newAreas, indexAreas, xCenter, yCenter, 0, 2, orientation)
            elongation = self.getObjectElongation(staticMoment02, staticMoment20, staticMoment11)

            scalingFactor = self.getScalingFactor(newAreas)

            scalingXCenter = scalingFactor * xCenter
            scalingYCenter = scalingFactor * yCenter

            self.writeData(str(indexAreas) + ".txt", newAreas, area, perimeter, compactness, xCenter, yCenter,
                    staticMoment02, staticMoment11, staticMoment20, elongation)

            elements.append([indexAreas, scalingXCenter, scalingYCenter, compactness * 2, elongation])

        return elements


    def getObjectArea(self, labels, areas, indexAreas):
        area = 0

        for i in range(areas[indexAreas][0], areas[indexAreas][2] + 1, 1):
            for j in range(areas[indexAreas][1], areas[indexAreas][3] + 1, 1):
                if (labels[i][j] == indexAreas + 1):
                    area += 1

        return area


    def getLabel(self, labels, i, j):
        try:
            return labels[i][j]
        except Exception as exc:
            return 0


    def getObjectPerimeter(self, labels, areas, indexAreas):
        perimeter = 0

        for i in range(areas[indexAreas][0], areas[indexAreas][2] + 1, 1):
            for j in range(areas[indexAreas][1], areas[indexAreas][3] + 1, 1):
                if labels[i][j] == indexAreas + 1:
                    counter = self.getLabel(labels, i - 1, j) + \
                        self.getLabel(labels, i + 1, j) + \
                        self.getLabel(labels, i, j - 1) + \
                        self.getLabel(labels, i, j + 1)

                    if counter != (indexAreas + 1) * 4:
                        perimeter += 1

        return perimeter


    def getObjectCompactness(self, perimeter, area):
        return perimeter ** 2 / area


    def getObjectCenterOfMass(self, labels, areas, indexAreas):
        xCounter = 0
        yCounter = 0
        counter = 0

        for i in range(areas[0], areas[2] + 1, 1):
            for j in range(areas[1], areas[3] + 1, 1):
                if labels[i][j] == indexAreas + 1:
                    xCounter += i
                    yCounter += j
                    counter += 1

        return (xCounter / counter) - areas[0], (yCounter / counter) - areas[1]


    def getObjectStaticMoment(self, labels, areas, indexAreas, xCenter, yCenter, i, j, orientation):
        staticMoment = 0
        height = areas[2] - areas[0] + 1
        width = areas[3] - areas[1] + 1
        for x in range(areas[0], areas[2] + 1, 1):
            for y in range(areas[1], areas[3] + 1, 1):
                if labels[x][y] == indexAreas + 1:
                    valueX = x - areas[0]
                    valueY = y - areas[1]
                    if orientation == 0:
                        staticMoment += ((valueX - xCenter) ** i) * ((valueY - yCenter) ** j)
                    elif orientation == 1:
                        staticMoment += (((height - valueX) - xCenter) ** i) * (((width - valueY) - yCenter) ** j)
                    elif orientation == 2:
                        staticMoment += (((width - valueY) - xCenter) ** i) * ((valueX - yCenter) ** j)
                    elif orientation == 3:
                        staticMoment += ((valueY - xCenter) ** i) * (((height - valueX) - yCenter) ** j)

        return staticMoment


    def getObjectElongation(self, staticMoment02, staticMoment20, staticMoment11):
        try:
            part1 = staticMoment20 + staticMoment02
            part2 = math.sqrt((staticMoment20 - staticMoment02) ** 2 + 4 * staticMoment11)

            return (part1 + part2) / (part1 - part2)

        except Exception as exp:
            return math.inf


    def getObjectOrientation(self, staticMoment02, staticMoment20, staticMoment11):
        try:
            value = 2 * staticMoment11 / (staticMoment20 - staticMoment02)
            return 0.5 * math.atan(value) * 180 / math.pi
        except Exception as exp:
            return 45


    def writeData(self, fileName, diap, area, perimeter, comp, x, y, stM02, stM20, stM11, el):
        try:
            file = open("data/output/cluster_analysis/" + fileName, 'w')
            try:
            
                file.write("Square: " + str(area) + "\n")
                file.write("Pereimeter: " + str(perimeter) + "\n")
                file.write("Density: " + str(comp) + "\n")
                file.write("Elongation : " + str(el) + "\n")
                file.write("Center of mass x=" + str(x) + " y=" + str(y) + "\n")
                file.write("Static moments:\n")
                file.write("stM02=" + str(stM02) + "\n")
                file.write("stM11=" + str(stM11) + "\n")
                file.write("stM20=" + str(stM20) + "\n")
                file.write("Height: " + str(diap[2] - diap[0] + 1) + "\n")
                file.write("Width: " + str(diap[3] - diap[1] + 1) + "\n")
            
            except Exception as ex:
                print(ex)
            finally:
                file.close()
        except Exception as ex:
            print(ex)


    def rotateImage(self, labels, areas, indexAreas, orientation, xCenterOfMass, yCenterOfMass):
        flag = False
        diap = []

        diap.append(int(math.sqrt(xCenterOfMass ** 2 + yCenterOfMass ** 2) + 1))
        diap.append(int(math.sqrt(((areas[2] - areas[0]) - xCenterOfMass) ** 2 + yCenterOfMass ** 2) + 1))
        diap.append(int(math.sqrt(xCenterOfMass ** 2 + ((areas[3] - areas[1]) - yCenterOfMass) ** 2) + 1))
        diap.append(
            int(math.sqrt(((areas[2] - areas[0]) - xCenterOfMass) ** 2 + ((areas[3] - areas[1]) - yCenterOfMass) ** 2) + 1))

        xCenterNew = max(diap)
        yCenterNew = max(diap)

        imageHeight = imageWidth = max(diap) * 2

        newLabels = [[int(0)] * imageWidth for i in range(imageHeight)]
        newAreas = 0

        k = math.pi / 180

        for i in range(areas[0], areas[2] + 1, 1):
            for j in range(areas[1], areas[3] + 1, 1):
                if labels[i][j] == indexAreas + 1:
                    valueI = int(i - areas[0] - xCenterOfMass)
                    valueJ = int(j - areas[1] - yCenterOfMass)

                    newI = int(valueI * math.cos(orientation * k) - valueJ * math.sin(orientation * k) + 0.5)
                    newJ = int(valueI * math.sin(orientation * k) + valueJ * math.cos(orientation * k) + 0.5)

                    newI += xCenterNew
                    newJ += yCenterNew

                    newLabels[newI][newJ] = indexAreas + 1

                    if flag == False:
                        newAreas = [int(newI), int(newJ), int(newI), int(newJ)]
                        flag = True

                    if newAreas[0] > newI:
                        newAreas[0] = newI
                    elif newAreas[1] > newJ:
                        newAreas[1] = newJ

                    if newAreas[2] < newI:
                        newAreas[2] = newI
                    elif newAreas[3] < newJ:
                        newAreas[3] = newJ

        for i in range(newAreas[0], newAreas[2] + 1, 1):
            for j in range(newAreas[1], newAreas[3] + 1, 1):
                if newLabels[i][j] == 0:
                    counter = self.getLabel(newLabels, i - 1, j) + \
                        self.getLabel(newLabels, i + 1, j) + \
                        self.getLabel(newLabels, i, j - 1) + \
                        self.getLabel(newLabels, i, j + 1) + \
                        self.getLabel(newLabels, i - 1, j - 1) + \
                        self.getLabel(newLabels, i + 1, j - 1) + \
                        self.getLabel(newLabels, i + 1, j - 1) + \
                        self.getLabel(newLabels, i + 1, j + 1)

                    if counter >= 6 * (indexAreas + 1):
                        newLabels[i][j] = indexAreas + 1

        return newLabels, newAreas


    def createImage(self, labels, areas, indexAreas, repository):
        height = areas[2] - areas[0] + 1
        width = areas[3] - areas[1] + 1

        image = Image.new("RGB", (height, width))
        draw = ImageDraw.Draw(image)

        pix = image.load()

        for i in range(0, height, 1):
            for j in range(0, width, 1):
                draw.point((i, j), (0, 0, 0))

        for i in range(0, height, 1):
            for j in range(0, width, 1):
                if labels[i + areas[0]][j + areas[1]] == indexAreas + 1:
                    draw.point((i, j), (255, 255, 255))

        for i in range(0, height, 1):
            for j in range(0, width, 1):
                if labels[i + areas[0]][j + areas[1]] == 0:
                    counter = self.getLabel(labels, i - 1 + areas[0], j + areas[1]) + \
                        self.getLabel(labels, i + 1 + areas[0], j + areas[1]) + \
                        self.getLabel(labels, i + areas[0], j - 1 + areas[1]) + \
                        self.getLabel(labels, i + areas[0], j + 1 + areas[1])

                    if counter >= 4 * (indexAreas + 1):
                        draw.point((i, j), (255, 255, 255))

        image.save("data/output/cluster_analysis/" + repository + str(indexAreas) + ".png")


    def getCenterOfMass(self, xCenter, yCenter, newAreas):
        height = newAreas[2] - newAreas[0] + 1
        width = newAreas[3] - newAreas[1] + 1

        diapX = []
        diapY = []

        diapX.append(xCenter)
        diapX.append(height - xCenter)
        diapX.append(width - yCenter)
        diapX.append(yCenter)

        diapY.append(yCenter)
        diapY.append(width - yCenter)
        diapY.append(xCenter)
        diapY.append(height - xCenter)

        maxValue = max(diapX)
        orientation = diapX.index(maxValue)

        return diapX[orientation], diapY[orientation], orientation


    def getScalingFactor(self, areas):
        height = areas[2] - areas[0] + 1
        width = areas[3] - areas[1] + 1

        value = max(height, width)

        return self.maxImageHeight / value    