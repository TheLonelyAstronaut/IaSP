import matplotlib.image as mpimg
import matplotlib.pyplot as plot

class ImageTools: 
    def __init__(self):
        plot.gray()
        self.inputPath = 'data/input/image_processing/'
        self.outputPath = 'data/output/image_processing/'


    def load(self, name):
        return mpimg.imread(self.inputPath + name)


    def save(self, name):
        plot.savefig(self.outputPath + name, bbox_inches='tight')


    def display(self, image, interpolation = 'none'):
        plot.imshow(image, interpolation = interpolation)
        plot.axis('off')

    
    def waitForClose(self):
        plot.show()