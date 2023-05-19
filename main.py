import pandas as pd
from geopy.distance import geodesic, great_circle

def calculate_square(coordinates,miles):
    half_length = miles / 2
    
    top_left = geodesic(miles=half_length).destination(coordinates, 45)
    top_right = geodesic(miles=half_length).destination(coordinates, 135)
    bottom_left = geodesic(miles=half_length).destination(coordinates, 315)
    bottom_right = geodesic(miles=half_length).destination(coordinates, 225)

    return top_left.format_decimal(), top_right.format_decimal(), bottom_left.format_decimal(), bottom_right.format_decimal()

def plot_squares(csv_path, miles):
    # Load csv
    df = pd.read_csv(csv_path)

    # iter through rows
    for index, row in df.iterrows():
        coords = (row['LAT'], row['LONG'])
        square = calculate_square(coords, miles)
        top_left, top_right, bottom_left, bottom_right = square

        # Add to separate column on df:
        df.at[index, 'Top Left'] = top_left
        df.at[index, 'Top Right'] = top_right
        df.at[index, 'Bottom Left'] = bottom_left
        df.at[index, 'Bottom Right'] = bottom_right
        if index > 10:
            break
    return df


csv_path = '~/Templates/__Misc__/Florida_pt01_gridpoints.csv'
miles = 10

output = plot_squares(csv_path, miles)

output.to_csv('~/Templates/__Misc__/output.csv', index=False)
print(output.head())
