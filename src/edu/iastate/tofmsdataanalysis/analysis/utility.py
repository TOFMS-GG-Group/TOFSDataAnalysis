class utility:
    # TODO: Use a better method to find pairs like divide and conquer method.
    @staticmethod
    def find_closest(point, data):
        list_has_point = False

        data.sort()

        for i in range(len(data)):
            if point == data[i]:
                return [point, float('inf')]

        if list_has_point == False:
            data.append(point)
            data.sort()

            location = data.index(point)

            if location == 0:
                return [data[location + 1], data[location + 2]]
            if location == len(data) - 1:
                return [data[location - 1], data[location - 2]]

            return [data[location - 1], data[location + 1]]
