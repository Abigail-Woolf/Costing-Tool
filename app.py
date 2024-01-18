from flask import Flask, render_template, request
import pandas as pd
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', static_folder='static')

# _________________________________________________________________________________________________________________________
# Specify the path to your Excel file
excel_file_path = '/Users/abbywoolf/Desktop/Costing-Tool/Cleaned_Cost_Data.xlsx'
# /Users/abbywoolf/Desktop/Costing-Tool
# Specify the sheet name you want to import
sheet_name = 'Frames'  # Replace 'Sheet1' with the actual sheet name
# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
# __________________________________________________________________________________________________________________________-
# MAKE Frames_df
frames_df = df.dropna()
frames_df['Frame'] = frames_df['Frame'].str.lower()


printer_data = {
    'PrinterName': ['inca-reductive', 'inca-synograph', 'epson', 'swissQ-synograph', ' SwissQ-Reductive', 'canon'],
    'labor': [8.0, 8.0, 5.0, 20.0, 20.00, 7.0],
    'ink': [.08, 1.68, 0.22, 2.80, .22, .27]
}
printer_costs_df = pd.DataFrame(printer_data)
# Make substrate df
substrate_data = {
    'SubstrateType': ['canvas', 'Epson-paper', 'Canon-paper', 'mdf'],
    'Price/sf': [.66, 1.35, 1.35, 0.99]
}
substrate_df = pd.DataFrame(substrate_data)

# Make hardware df
hardware_data = {
    'hardwareType': ['cleat', 'wire', 'd-rings'],
    'price': [5.00, 2.00, 0]
}
hardware_df = pd.DataFrame(hardware_data)
# ___________________________FUNCTION______________________________________________
# def total_cost(length, width, frame_type, substrate, printer, hardware, margin_percent, royality_percent):
    # valid_options_arg1 = ['fps','gwt','bfl','cfl','gfl','bgf','nfl','wfl','bcap','ncap','gcap','walcap']
    # valid_options_arg2 = ['canvas', 'Epson-paper', 'Canon-paper', 'mdf']
    # valid_options_arg3 = ['inca-reductive', 'inca-synograph', 'epson', 'swissQ-synograph', ' SwissQ-Reductive', 'canon']
    # valid_options_arg4 = ['cleat', 'wire', 'd-rings']

    # # Check if the arguments are in the valid options
    # if frame_type not in valid_options_arg1:
    #     raise ValueError(f"Invalid value for arg1. Allowed options are: {valid_options_arg1}")
    # if substrate not in valid_options_arg2:
    #     raise ValueError(f"Invalid value for arg2. Allowed options are: {valid_options_arg2}")
    # if printer not in valid_options_arg3:
    #     raise ValueError(f"Invalid value for arg3. Allowed options are: {valid_options_arg3}")
    # if hardware not in valid_options_arg4:
    #     raise ValueError(f"Invalid value for arg4. Allowed options are: {valid_options_arg4}")
    
  #_______________________________________________________________________________ 
    # Calc Substrate Costs
    # price_per_sf = substrate_df.loc[substrate_df['SubstrateType'] == substrate, 'Price/sf'].values[0]
    # if substrate == 'canvas':
    #     if length > 58 and width > 58:
    #         cost_of_substrate = (((length + 11) * (width + 11)) / 144) * price_per_sf
    #     else:
    #         cost_of_substrate = (((length + 8) * (width + 8)) / 144) * price_per_sf

    # elif substrate == 'Epson-paper' or 'Canon-paper':
    #     cost_of_substrate = (((length + 1.5) * (width +1.5)) / 144) * price_per_sf

    # elif substrate == 'mdf':
    #     #Check if dimensions match 49x60
    #     if (length == 60 and width == 48) or (length == 48 and width == 60):
    #         cost_of_substrate= 15.32
    #     else:
    #         cost_of_substrate = ((length * width) / 144) * 1.2
    # else:
    #     raise ValueError("Invalid substrate")
    #return cost_of_substrate

    # price_per_sf = substrate_df.loc[substrate_df['Substrate'] == substrate, 'Price/sf'].values[0]
    #cost_of_substrate = square_feet * price_per_sf
    
  #_______________________________________________________________________________  
    # Calc Frame costs
    # Check if a matching row exists in the DataFrame
#     length= float(length)
#     width= float(width)
#     matching_rows = frames_df[
#         (frames_df['Length'] == length) &
#         (frames_df['Width'] == width) &
#         (frames_df['Frame'].str.contains(frame_type))
#     ]

#     if not matching_rows.empty:
#         cost_of_frame = matching_rows['GP Price'].values[0]
#         return cost_of_frame
#     else:
#         print(f"Frame with Length {length}, Width {width}, and Type {frame_type} not found.")
#         return None  # Or any other appropriate value or indication

# #__________________________________________________________________________________
#     # Implement the calculation for printer costs

#     ink_per_sf = printer_costs_df.loc[printer_costs_df['PrinterName'] == printer, 'ink'].values[0]
#     labor_cost = printer_costs_df.loc[printer_costs_df['PrinterName'] == printer, 'labor'].values[0]

#     total_printer_cost = ink_per_sf + labor_cost
#     #return total_printer_cost
    
# #_______________________________________________________________________________ 
#     #implement hardware costs
#     hardware_cost = hardware_df.loc[hardware_df['hardwareType'] == hardware, 'price'].values[0]
# #___________________________________________________________________________________
#     # Create the desired margin calculator
#     final_cost_no_roy = cost_of_substrate + cost_of_frame + total_printer_cost + hardware_cost
#     # return final_cost

#  #___________________________________________________________________________________   
#     margin_dec = margin_percent * .01
#     royality_dec = royality_percent * .01
    
#     wsp = final_cost_no_roy/(1-royality_dec - margin_dec)
#     royalty_value = wsp * royality_dec
#     final_cost_with_roy = final_cost_no_roy + royalty_value
#     return final_cost_with_roy, wsp
 #________________________END FUNCTION______________________________________________    
def test_substrate_cost(length, width, substrate):
    price_per_sf = substrate_df.loc[substrate_df['SubstrateType'] == substrate, 'Price/sf'].values[0]
    if substrate == 'canvas':
        if length > 58 and width > 58:
            cost_of_substrate = (((length + 11) * (width + 11)) / 144) * price_per_sf
        else:
            cost_of_substrate = (((length + 8) * (width + 8)) / 144) * price_per_sf

    elif substrate == 'Epson-paper' or substrate == 'Canon-paper':
        cost_of_substrate = (((length + 1.5) * (width +1.5)) / 144) * price_per_sf


    elif substrate == 'tar-board':
        cost_of_substrate = (((length + .125) * (width + .125)) / 144) * price_per_sf
    
    elif substrate == 'mdf':
        #Check if dimensions match 49x60
        if (length == 60 and width == 48) or (length == 48 and width == 60):
            cost_of_substrate= 15.32
        else:
            cost_of_substrate = (((length * width) / 144) * 1.2) * price_per_sf
    else:
        raise ValueError("Invalid substrate")


    return cost_of_substrate

def test_frame_cost(length, width, frame_type):
    # Calc Frame costs
    # Check if a matching row exists in the DataFrame
    length= float(length)
    width= float(width)
    matching_rows = frames_df[
        (frames_df['Length'] == length) &
        (frames_df['Width'] == width) &
        (frames_df['Frame'].str.contains(frame_type))
    ]

    if not matching_rows.empty:
        cost_of_frame = matching_rows['GP Price'].values[0]
        return cost_of_frame
    else:
        print(f"Frame with Length {length}, Width {width}, and Type {frame_type} not found.")
        return None  # Or any other appropriate value or indication

    # Implement the calculation for printer costs
def test_printer_cost(length, width, printer):
    
        ink_per_sf = printer_costs_df.loc[printer_costs_df['PrinterName'] == printer, 'ink'].values[0]
        labor_cost = printer_costs_df.loc[printer_costs_df['PrinterName'] == printer, 'labor'].values[0]

        total_printer_cost = ((ink_per_sf) * (length * width) / 144) + labor_cost
        return total_printer_cost

def test_hardware_cost(hardware):
#implement hardware costs
    hardware_cost = hardware_df.loc[hardware_df['hardwareType'] == hardware, 'price'].values[0]
    return hardware_cost

    # Create the desired margin calculator
def royalty_calculator(final_cost, margin_percent, royalty_percent):


 #___________________________________________________________________________________   
        margin_dec = margin_percent * .01
        royalty_dec = royalty_percent * .01
    
        wsp = final_cost/(1-royalty_dec - margin_dec)
        royalty_value = wsp * royalty_dec
        final_cost_with_roy = final_cost + royalty_value
        return final_cost_with_roy

        # Create the desired margin calculator
def wsp_calculator(final_cost, margin_percent, royalty_percent):
 #___________________________________________________________________________________   
        margin_dec = margin_percent * .01
        royalty_dec = royalty_percent * .01
    
        wsp = final_cost/(1-royalty_dec - margin_dec)
        royalty_value = wsp * royalty_dec
        final_cost_with_roy = final_cost + royalty_value
        return wsp


def final_cost(length, width, frame_type, printer, substrate, hardware, margin_percent, royalty_percent):
    test_substrate = test_substrate_cost(length, width, substrate)
    test_frames = test_frame_cost(length, width,frame_type)
    test_printer = test_printer_cost(length, width,printer)
    test_hardware = test_hardware_cost(hardware)
    final_cost = test_substrate + test_frames + test_printer + test_hardware
    def wsp_calculator(final_cost, margin_percent, royalty_percent):
 #___________________________________________________________________________________   
        margin_dec = margin_percent * .01
        royalty_dec = royalty_percent * .01
    
        wsp = final_cost/(1-royalty_dec - margin_dec)
        royalty_value = wsp * royalty_dec
        final_cost_with_roy = final_cost + royalty_value
    
    test_wsp = wsp_calculator(final_cost, margin_percent, royalty_percent)
    cost_with_roy = margin_calculator(final_cost, margin_percent, royalty_percent)

    data = {'Substrate Cost': [test_substrate],
            'Frame Cost': [test_frames],
            'Printer Costs': [test_printer],
            'Harware Costs': [test_hardware],
            'Final GP Cost': [final_cost],
            'Cost w/ Royalty': [cost_with_roy],
            'WSP @ % Margin': [test_wsp]}
    results_df = pd.DataFrame(data)
    return results_df
    
 #________________________END FUNCTION______________________________________________ 



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
    required_fields = ['title', 'length', 'width', 'frame_type', 'substrate', 'printer', 'hardware', 'margin_percent','royality_percent']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All required fields must be provided.'}), 400

    title = data['title']
    length = float(data['length'])
    width = float(data['width'])
    frame_type = data['frame_type'].lower()
    substrate = data['substrate'].lower()
    printer = data['printer'].lower()
    hardware = data['hardware'].lower()
    margin_percent = data['margin_percent']
    royality_percent = data['royality_percent']


    price = f"${round(final_cost(length, width, frame_type, substrate, printer, hardware, margin_percent, royality_percent),2)}"

    # Append the results to the list
    results_list.append({
        'title': title,
        'length': length,
        'width': width,
        'printer': printer,
        'substrate': substrate,
        'frame_type': frame_type,
        'hardware': hardware,
        'margin_percent': margin_percent,
        'Royality_percent': royality_percent,
        'price': price,
        'wsp': test_wsp
    })


    # Return the results as JSON
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)
