from src.image_processing.core import ImageProcessingCore

class AppCore:
    def __init__(self):
        self.imageProcessing = ImageProcessingCore()


    def start(self):
        self.imageProcessing.start()