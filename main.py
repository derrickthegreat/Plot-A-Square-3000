import os
import math
import pandas as pd
from geopy.distance import geodesic

def calculate_diagonal(length_of_side):
    return math.sqrt(length_of_side ** 2 + length_of_side ** 2)

def calculate_square(coordinates,miles):
    
    top_right = geodesic(miles=miles).destination(coordinates, 45)
    bottom_right = geodesic(miles=miles).destination(coordinates, 135)
    top_left = geodesic(miles=miles).destination(coordinates, 315)
    bottom_left = geodesic(miles=miles).destination(coordinates, 225)

    return top_left.format_decimal(), top_right.format_decimal(), bottom_left.format_decimal(), bottom_right.format_decimal()

def plot_squares(csv_path, miles):
    # Load csv
    df = pd.read_csv(csv_path)

    # Create new columns for df
    corner_columns = ['Top Left X', 'Top Left Y', 'Top Right X', 'Top Right Y', 
                      'Bottom Left X', 'Bottom Left Y', 'Bottom Right X',
                      'Bottom Right Y']
    df[corner_columns] = pd.DataFrame([[0] * len(corner_columns)], index=df.index)

    df_length = len(df)
    # iter through rows
    for index, row in df.iterrows():
        coords = (row['LAT'], row['LONG'])
        square = calculate_square(coords, miles)
        top_left, top_right, bottom_left, bottom_right = square

        # Add to separate column on df:
        df.at[index, 'Top Left X'] = top_left.split(", ")[0]
        df.at[index, 'Top Left Y'] = top_left.split(", ")[1]
        df.at[index, 'Top Right X'] = top_right.split(", ")[0]
        df.at[index, 'Top Right Y'] = top_right.split(", ")[1]
        df.at[index, 'Bottom Left X'] = bottom_left.split(", ")[0]
        df.at[index, 'Bottom Left Y'] = bottom_left.split(", ")[1]
        df.at[index, 'Bottom Right X'] = bottom_right.split(", ")[0]
        df.at[index, 'Bottom Right Y'] = bottom_right.split(", ")[1]

        # Progress Update
        progress = (index + 1) / df_length * 100
        print(f"Processing: {progress:.2f}% complete", end="\r")
        # Uncomment to only process the first X records.
        #if index > 1:
        #    break
    return df

def init():
    print('Welcome to the Plot-A-Square 3000')
    print()
    valid_csv = False
    while not valid_csv:
        csv_path = input('Please enter the path of the input CSV file: ')
        if os.path.isfile(csv_path):
            valid_csv = True
        print('This file does not exist...')

    output_path = os.path.join(os.path.dirname(csv_path), "output.csv")

    miles = float(input('Please enter the number of miles for each side of the square: '))
    
    miles = calculate_diagonal(miles)

    print('Plotting the squares.....')
    
    output = plot_squares(csv_path,miles)
    output.to_csv(output_path, index=False)

if __name__ == '__main__':
    init()
