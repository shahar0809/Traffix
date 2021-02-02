def to_string(crosswalk_points):
    str = ''.join(crosswalk_points)
    x = to_string(crosswalk_points[0])
    y = to_string(crosswalk_points[1])
    (x, y) = (x, y)
    print(str)

to_string((5, 6))