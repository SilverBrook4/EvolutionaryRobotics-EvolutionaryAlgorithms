import numpy
import matplotlib.pyplot

backLegSensorValues = numpy.load("data//BackLegSensorValues.npy")
frontLegSensorValues = numpy.load("data//FrontLegSensorValues.npy")

matplotlib.pyplot.plot(backLegSensorValues)
matplotlib.pyplot.plot(frontLegSensorValues)
matplotlib.pyplot.show()
