import numpy
import matplotlib.pyplot

backLegSensorValues = numpy.load("data//BackLegSensorValues.npy")
frontLegSensorValues = numpy.load("data//FrontLegSensorValues.npy")


matplotlib.pyplot.plot(backLegSensorValues, linewidth=5, label="Back Leg")
matplotlib.pyplot.plot(frontLegSensorValues, label="Front Leg")

matplotlib.pyplot.legend()
matplotlib.pyplot.show()
