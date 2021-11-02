from PIL import Image

class ObjectSelection: 
    def __init__(self):
        self.imageHeight = 0
        self.imageWidth = 0
        self.flagL = False

    def labeling(self, path, img):
        image = Image.open(path)

        self.imageHeight = image.size[0]
        self.imageWidth = image.size[1]

        L = 0
        areas = []
        self.flagL = True

        labels = [[int(0)] * self.imageWidth for i in range(self.imageHeight)]

        for i in range(0, self.imageHeight, 1):
            for j in range(0, self.imageWidth, 1):
                if self.flagL == True:
                    L += 1
                    areas.append([int(i), int(j), int(i), int(j)])
                    self.flagL = False
                else:
                    areas[L - 1][0] = areas[L - 1][2] = i
                    areas[L - 1][1] = areas[L - 1][3] = j

                self.fill(img, labels, L, i, j, areas)

        if self.flagL == False:
            areas.pop(L - 1)

        return labels, areas

    def fill(self, img, labels, L, i, j, areas):
        if labels[i][j] == 0 and img[i][j] == 1:
            labels[i][j] = L
            self.flagL = True

            if i < areas[L - 1][0]:
                areas[L - 1][0] = i
            elif i > areas[L - 1][2]:
                areas[L - 1][2] = i

            if j < areas[L - 1][1]:
                areas[L - 1][1] = j
            elif j > areas[L - 1][3]:
                areas[L - 1][3] = j

            if j > 0:
                self.fill(img, labels, L, i, j - 1, areas)

            if j < self.imageWidth - 1:
                self.fill(img, labels, L, i, j + 1, areas)

            if i > 0:
                self.fill(img, labels, L, i - 1, j, areas)

            if i < self.imageHeight - 1:
                self.fill(img, labels, L, i + 1, j, areas)