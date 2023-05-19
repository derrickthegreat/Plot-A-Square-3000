from geopy.distance import geodesic, great_circle

def calculate_square_coordinates(coordinates,miles):
    half_length = miles / 2
    
    top_left = geodesic(miles=half_length).destination(coordinates, 45)
    top_right = geodesic(miles=half_length).destination(coordinates, 135)
    bottom_left = geodesic(miles=half_length).destination(coordinates, 315)
    bottom_right = geodesic(miles=half_length).destination(coordinates, 225)

    return top_left.format_decimal(), top_right.format_decimal(), bottom_left.format_decimal(), bottom_right.format_decimal()
