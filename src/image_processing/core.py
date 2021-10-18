from src.image_processing.image_tools.image_tools import ImageTools
from src.image_processing.histogram_tools.histogram_tools import HistogramTools
from src.image_processing.log_correction.log_correction import LogCorrection
from src.image_processing.roberts_filtration.roberts_filtration import RobertsFiltration

class ImageProcessingCore: 
    def __init__(self):
        self.imageTools = ImageTools()
        self.histogramTools = HistogramTools()
        self.logCorrection = LogCorrection()
        self.robertsFiltration = RobertsFiltration()


    def start(self):
        c = int(input('Enter C constant: '))

        self.logCorrection.setCConstant(c)

        image = self.imageTools.load('meme.jpg')
        self.imageTools.display(image)
        self.imageTools.waitForClose()

        histogram = self.histogramTools.getHistogramFromImage(image)
        self.histogramTools.display(histogram)

        logCorrected = self.logCorrection.correction(image)
        self.imageTools.display(logCorrected, 'nearest')
        self.imageTools.save('meme_corrected.jpg')
        self.imageTools.waitForClose()

        histogram = self.histogramTools.getHistogramFromImage(logCorrected)
        self.histogramTools.display(histogram)

        filtered = self.robertsFiltration.filter(image)
        self.imageTools.display(filtered, 'nearest')
        self.imageTools.save('meme_filtered.jpg')
        self.imageTools.waitForClose()

        histogram = self.histogramTools.getHistogramFromImage(filtered)
        self.histogramTools.display(histogram)
        