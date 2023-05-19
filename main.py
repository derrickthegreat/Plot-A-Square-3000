import os
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
        # Uncomment to only process the first ten records.
        #if index > 50:
        #    break
    return df

def init():
    csv_path = ''
    while csv_path == '':
        csv_path = input('Enter the path of the input CSV file: ')

    output_path = input('Enter the output path for the modified CSV file (default: root of input CSV): ')
    if output_path == "":
        output_path = os.path.join(os.path.dirname(csv_path), "output.csv")

    miles = float(input('Enter the number of miles for the square: '))

    print('Plotting the squares.....')
    
    output = plot_squares(csv_path,miles)
    output.to_csv(output_path, index=False)

if __name__ == '__main__':
    print('Welcome to the Plot-A-Square 3000')
    print()
    init()
