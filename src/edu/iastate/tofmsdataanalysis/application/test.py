from src.edu.iastate.tofmsdataanalysis.analysis.utility import utility

data = [3, 5, 6, 7, 8, 9, 11, 13, 15]

points = utility.find_closest(0, data)
print(str(points[0]) + " " + str(points[1]))

points = utility.find_closest(10, data)
print(str(points[0]) + " " + str(points[1]))

points = utility.find_closest(16, data)
print(str(points[0]) + " " + str(points[1]))
