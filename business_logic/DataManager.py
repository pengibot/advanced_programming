import json

import pandas as pd

from utils import LoggerFactory
from utils.NaNConverter import NaNConverter


class DataManager:


    data_frame = None

    def get_data_frame(self):
        return self.data_frame

    def remove_unwanted_NGRs(self, unwanted_NGRs, jsonFile):
        # Load the data from the JSON file
        with open(jsonFile, 'r') as file:
            data = json.load(file)

        # Use list comprehension to keep only the entries with an NGR not in the unwanted set
        data = [entry for entry in data if entry['transmitter_info']['NGR'] not in unwanted_NGRs]

        # Write the data back to the JSON file
        with open(jsonFile, 'w') as file:
            json.dump(data, file, indent=4)


    def extract_EID_data(self, multiplexes, jsonFile):
        # Load the data from the JSON file
        with open(jsonFile, 'r') as file:
            data = json.load(file)

            for entry in data:
                if entry['broadcast_info']['EID'] in multiplexes:
                    entry['broadcast_info']['EID'] = {entry['broadcast_info']['EID']: {
                        "Site": entry['broadcast_info']['Site'],
                        "Site Height": entry['transmitter_info']['Site Height'],
                        "Aerial height (m)": entry['transmitter_info']['In-Use Ae Ht'],
                        "Power (kW)": entry['transmitter_info']['In-Use ERP Total']
                    }
                    }

        # Write the data back to the JSON file
        with open(jsonFile, 'w') as file:
            json.dump(data, file, indent=4)


    def read_in_csv_data(self, transmitterInfoFilename, broadcastInfoFilename):
        try:
            # Read the data from the CSV files
            transmitter_info = pd.read_csv(transmitterInfoFilename, encoding='iso-8859-1')
            LoggerFactory.get_logger().info(f"Successfully read {transmitterInfoFilename} file into a DataFrame")
            broadcast_info = pd.read_csv(broadcastInfoFilename, encoding='iso-8859-1')
            LoggerFactory.get_logger().info(f"Successfully read {broadcastInfoFilename} file into a DataFrame")

            # Merge the datasets on 'id'
            LoggerFactory.get_logger().info(f"Starting merge of DataFrames into one, based on the 'id' field")
            self.data_frame = pd.merge(transmitter_info, broadcast_info, on='id')
            LoggerFactory.get_logger().info(f"Successfully merged DataFrames into one")
            return True
        except Exception as error:
            LoggerFactory.get_logger().error(f"An error occurred whilst merging DataFrames: {error}")
            return False



    def convert_data_frame_to_json(self, data_frame, json_file_name):

        # Convert the DataFrame into a nested dictionary
        nested_dict = []
        for index, row in data_frame.iterrows():
            temp = {
                "id": row['id'],
                "transmitter_info": {
                    "NGR": row['NGR'],
                    "Longitude/Latitude": row['Longitude/Latitude'],
                    "Site Height": row['Site Height'],
                    "In-Use Ae Ht": row['In-Use Ae Ht'],
                    "In-Use ERP Total": row['In-Use ERP Total'],
                    "Dir Max ERP": row['Dir Max ERP'],
                    "Radiation Pattern":
                        {str(i * 10): row[str(i * 10)] for i in range(36)},
                    "Lat": row['Lat'],
                    "Long": row['Long']
                },
                "broadcast_info": {
                    "Date": row['Date'],
                    "Ensemble": row['Ensemble'],
                    "Licence": row['Licence'],
                    "Ensemble Area": row['Ensemble Area'],
                    "EID": row['EID'],
                    "Transmitter Area": row['Transmitter Area'],
                    "Site": row['Site'],
                    "Freq.": row['Freq.'],
                    "Block": row['Block'],
                    "TII Main Id (Hex)": row['TII Main Id (Hex)'],
                    "TII Sub Id (Hex)": row['TII Sub Id (Hex)'],
                    "Services": [
                        {f'Serv Label{i} ': row[f'Serv Label{i} '],
                         f'SId {i} (Hex)': row[f'SId {i} (Hex)'],
                         f'LSN {i} (Hex)': row[f'LSN {i} (Hex)']}
                        for i in range(1, 33) if pd.notna(row[f'Serv Label{i} '])],
                    "Lat": row['Lat'],
                    "Long": row['Long']
                }
            }
            nested_dict.append(temp)

        # Convert the nested dictionary into a JSON string
        nested_json = json.dumps(nested_dict, indent=4, cls=NaNConverter)

        # Write the JSON string to a file
        with open(json_file_name, 'w') as file:
            file.write(nested_json)


# transmitterInfoFile = input("Enter Transmitter Info File> ")
# broadcastInfoFile = input("Enter Broadcast Info File> ")
# print("Converting .csv files into a single .json file")
# convert_csv_to_json('TxAntennaDAB.csv', 'TxParamsDAB.csv', 'nested_data.json')
# print("Removing unwanted NGR\'s")
# remove_unwanted_NGRs({"NZ02553847", "SE213515", "NT05399374", "NT25265908"}, 'nested_data.json')
# print("Extracting EID data and Renaming Headers")
# extract_EID_data(["C18A", "C18F", "C188"], 'nested_data.json')
# print("All processes completed successfully")
