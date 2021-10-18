import matplotlib.pyplot as plot

class HistogramTools:
    def getHistogramFromImage(self, image):
        brightnesses = []

        for row in image:
            for line in row:
                brightnesses.append(round(0.299 * line[0] + 0.587 * line[1] + 0.114 * line[2]))

        histogram = [0] * 256

        for brightness in brightnesses:
            histogram[brightness] += 1
            
        return histogram


    def display(self, histogram):
        plot.bar(range(len(histogram)), histogram, width=1)
        plot.show()