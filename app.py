from flask import Flask, render_template, request
import pandas as pd
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', static_folder='static')

# _________________________________________________________________________________________________________________________
# Specify the path to your Excel file
excel_file_path = '/Users/abbywoolf/Desktop/Data_Projects/Costing_App/Cleaned_Cost_Data.xlsx'
# Specify the sheet name you want to import
sheet_name = 'Frames'  # Replace 'Sheet1' with the actual sheet name
# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
# __________________________________________________________________________________________________________________________-
# MAKE THE DFS
# Drop all Nan Values
frames_df = df.dropna()
# frame_ids = frames_df['Inventory ID'].unique()
# Data for the printers DataFrame
data = {
    'PrinterName': ['inca', 'epson', 'swiss', 'canon', 'swissq-reductive', 'swissq-synograph'],
    'Price': [8.0, 5.0, 20.0, 7.0, 8.0, 20.0]
}
# Create the printers DataFrame
printers_df = pd.DataFrame(data)

# Make substrate df
# Data for the printers DataFrame
substrate_data = {
    'Substrate': ['canvas', 'paper', 'mdf'],
    'Price/sf': [.66, 1.35, 0.99]
}
# Create the printers DataFrame
substrate_df = pd.DataFrame(substrate_data)

# Make substrate df
# Data for the printers DataFrame
hardware_data = {
    'hardware': ['cleat', 'wire', 'd-rings'],
    'Price': [5.00, 2.00, 0]
}
# Create the printers DataFrame
hardware_df = pd.DataFrame(hardware_data)
# __________________________________________________________________________________________
# Your function goes here
def total_cost(length, width, frame_type, substrate, printer):
    # Calc Substrate Costs
    if substrate == 'canvas':
        if length > 58 and width > 58:
            square_feet = ((length + 11) * (width + 11)) / 144
        else:
            square_feet = ((length + 8) * (width + 8)) / 144
    elif substrate == 'paper':
        square_feet = ((length + 2) * (width + 2)) / 144
    elif substrate == 'mdf':
        square_feet = (length * width) / 144
    else:
        raise ValueError("Invalid substrate")

    price_per_sf = substrate_df.loc[substrate_df['Substrate'] == substrate, 'Price/sf'].values[0]
    cost_of_substrate = square_feet * price_per_sf
    
    
    # Calc Frame costs
    # Check if a matching row exists in the DataFrame
    matching_rows = frames_df[
        (frames_df['Length'] == length) &
        (frames_df['Width'] == width) &
        (frames_df['Frame'].str.contains(frame_type))
    ]

    if not matching_rows.empty:
        # Retrieve the price for the given frame type, length, and width
        cost_of_frame = matching_rows['GP Price'].values[0]
        # return price
    else:
        print(f"Frame with Length {length}, Width {width}, and Type {frame_type} not found.")
        return None

    # Printing Cost
    if printer in printers_df['PrinterName'].values:
        cost_of_printer = printers_df.loc[printers_df['PrinterName'] == printer, 'Price'].values[0]

    
    return cost_of_substrate + cost_of_frame + cost_of_printer
    

@app.route('/')
def index():
    return render_template('index.html')

# Create list to hold the results
results_list = []  # This list will store the results for each entry

@app.route('/calculate', methods=['POST'])
def calculate():
    # Retrieve the form data
    data = request.get_json()

    # Check if all required fields are present in the JSON data
    required_fields = ['title', 'length', 'width', 'frame_type', 'substrate', 'printer']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All required fields must be provided.'}), 400

    title = data['title']
    length = float(data['length'])
    width = float(data['width'])
    frame_type = data['frame_type'].upper()
    substrate = data['substrate'].lower()
    printer = data['printer'].lower()

    price = f"${round(total_cost(length, width, frame_type, substrate, printer),2)}"

    # Append the results to the list
    results_list.append({
        'title': title,
        'length': length,
        'width': width,
        'frame_type': frame_type,
        'substrate': substrate,
        'printer': printer,
        'price': price
    })

    # Return the results as JSON
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)
