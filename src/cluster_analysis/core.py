from src.cluster_analysis.image_dissection.image_dissection import ImageDissection
from src.cluster_analysis.object_selection.object_selection import ObjectSelection
from src.cluster_analysis.object_properties.object_properties import ObjectProperties
from src.cluster_analysis.analytics.analytics import Analytics
import sys
import threading

class ClusterAnalysisCore:
    def __init__(self):
        self.imageDissection = ImageDissection()
        self.objectSelection = ObjectSelection()
        self.objectProperties = ObjectProperties()
        self.analytics = Analytics()

    def _start(self):
        min = int(input("Enter the min value for dissection: "))

        if 0 > min or min > 255:
            print("Min value cannot be less than zero or greater than 255")
            return
        
        max = int(input("Enter the max value for dissection: "))

        if min > max or max > 255:
            print("Max value cannot be less than min value or greater than 255")
            return

        image, img = self.imageDissection.dissection(min, max, "data/input/cluster_analysis/test.jpg")

        image.save("data/output/cluster_analysis/dissected_image.png")

        labels, areas = self.objectSelection.labeling("data/input/cluster_analysis/test.jpg", img)

        elements = self.objectProperties.getObjectProperties(labels, areas)

        clusters_num = int(input("Clusters num (between 2 and " + str(len(elements)) + "): "))

        clusters = self.analytics.getClusters(elements, clusters_num)

        print(clusters)

    def start(self):
        sys.setrecursionlimit(50000)
        #threading.stack_size(2000000000)
        #thread = threading.Thread(target=self._start)
        #thread.start()
        self._start()