from src.cluster_analysis.core import ClusterAnalysisCore
from src.image_processing.core import ImageProcessingCore

class AppCore:
    def __init__(self):
        self.imageProcessing = ImageProcessingCore()
        self.clusterAnalysis = ClusterAnalysisCore()


    def start(self):
        #self.imageProcessing.start()
        self.clusterAnalysis.start()