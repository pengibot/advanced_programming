import json
import statistics

import pandas as pd

from utils import LoggerFactory
from utils.NaNConverter import NaNConverter


class DataManager:
    """
        Class responsible for interacting with the data. Decoupled from the front end
    """

    # A reference to the Panda DataFrame in order to save and load a Data Set
    data_frame = None

    # A reference to the location a user decides to save the Data Set to.
    json_file_name = "temp.json"

    def get_data_frame(self):
        """
            A getter that can be used to get Panda Data Frame
        """
        return self.data_frame

    def remove_unwanted_NGRs(self, unwanted_NGRs, jsonFile):
        """
            Removes NGR data from the json file passed in
        """

        LoggerFactory.get_logger().info(f"Started removing the following NGR's from the data set, {unwanted_NGRs}")
        # Load the data from the JSON file
        with open(jsonFile, 'r') as file:
            LoggerFactory.get_logger().info(f"Opened {jsonFile} in order to remove NGR's")
            data = json.load(file)

        # Use list comprehension to keep only the entries with an NGR not in the unwanted set
        data = [entry for entry in data if entry['transmitter_info']['NGR'] not in unwanted_NGRs]
        LoggerFactory.get_logger().info(f"Successfully removed NGR's")

        # Write the data back to the JSON file
        with open(jsonFile, 'w') as file:
            LoggerFactory.get_logger().info(f"Updating {jsonFile} with changes")
            json.dump(data, file, indent=4)  # Use indent to make it human-readable

    def extract_EID_data(self, multiplexes, jsonFile):
        """
            Extracts EID data into a new entry.
            Renames 'In-Use Ae Ht' to 'Aerial height (m)'
            Renames 'In-Use ERP Total' to 'Power (kW)'
        """

        LoggerFactory.get_logger().info(f"Started extracting EID data {multiplexes} to a new entry")
        # Load the data from the JSON file
        with open(jsonFile, 'r') as file:
            LoggerFactory.get_logger().info(f"Opened {jsonFile} in order to extract data")
            data = json.load(file)

            for entry in data:
                if entry['broadcast_info']['EID'] in multiplexes:
                    LoggerFactory.get_logger().info(
                        f"Found EID data mathing a multiplex for {entry['broadcast_info']['EID']}")
                    LoggerFactory.get_logger().info(f"Extracting data to create a new entry")
                    entry['broadcast_info']['EID'] = {entry['broadcast_info']['EID']: {
                        "Site": entry['broadcast_info']['Site'],
                        "Site Height": entry['transmitter_info']['Site Height'],
                        "Aerial height (m)": entry['transmitter_info']['In-Use Ae Ht'],
                        "Power (kW)": entry['transmitter_info']['In-Use ERP Total']
                    }
                    }

        # Write the data back to the JSON file
        with open(jsonFile, 'w') as file:
            LoggerFactory.get_logger().info(f"Saving extracted data back to Data Source")
            json.dump(data, file, indent=4)  # Creating indent to be human-readable

    def read_in_csv_data(self, transmitter_info_filename, broadcast_info_filename):
        """
            Responsible for reading in 2 csv files and cleaning the data.
        """

        try:
            # Read the data from the CSV files
            transmitter_info = pd.read_csv(transmitter_info_filename, encoding='iso-8859-1')
            LoggerFactory.get_logger().info(f"Successfully read {transmitter_info_filename} file into a DataFrame")
            broadcast_info = pd.read_csv(broadcast_info_filename, encoding='iso-8859-1')
            LoggerFactory.get_logger().info(f"Successfully read {broadcast_info_filename} file into a DataFrame")

            # Merge the datasets on 'id'
            LoggerFactory.get_logger().info(f"Starting merge of DataFrames into one, based on the 'id' field")
            self.data_frame = pd.merge(transmitter_info, broadcast_info, on='id')
            LoggerFactory.get_logger().info(f"Successfully merged DataFrames into one")
            self.clean_csv_json_data()
            return True  # return result to GUI to inform of outcome
        except Exception as error:  # Catch errors from reading in the csv files and attempting to merge
            LoggerFactory.get_logger().error(f"An error occurred whilst merging DataFrames: {error}")
            return False  # return result to GUI to inform of outcome

    def read_in_json_data(self, json_file):
        """
            Reads in json file to a Data Frame using Pandas
        """
        try:
            LoggerFactory.get_logger().info(f"Starting to read in .json file {json_file}")
            self.data_frame = pd.read_json(json_file)  # Use Pandas library to read in .json file
            LoggerFactory.get_logger().info(f"Finished reading in .json file to Data Frame")
            return True  # return result to GUI to inform of outcome
        except Exception as error:
            # Catch errors that may occur due to the json file being invalid
            LoggerFactory.get_logger().error(f"An error occurred whilst reading .json file to Data Frame: {error}")
            return False  # return result to GUI to inform of outcome

    def save_json_file(self, json_file_name):
        """
            Responsible for saving the Data Frame to .json
        """
        try:
            LoggerFactory.get_logger().info(f"Writing Data Frame to {json_file_name} file ")
            with open(json_file_name, 'w') as file:
                # Takes a Pandas DataFrame and converts it to JSON before writing it to a file
                json.dump(json.loads(self.data_frame.to_json(orient='records')), file, indent=4)
            LoggerFactory.get_logger().info(f"File written Successfully")
            return True
        except Exception as error:
            # Catch errors that may occur due to the json file being invalid
            LoggerFactory.get_logger().error(f"An error occurred whilst saving Data Frame to .json file: {error}")
            return False

    def save_data_frame_to_json(self, json_file_name):
        """
            Responsible for initially setting up how the JSON is structured
            Writes the JSON to a file.
        """
        try:
            # Convert the DataFrame into a nested dictionary
            nested_dict = []
            for index, row in self.data_frame.iterrows():
                try:
                    entry = {
                        "id": row['id'],  # Use id as the primary identifier
                        "transmitter_info": {  # Group data to do with transmitter info
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
                        "broadcast_info": {  # Group data to do with broadcast info
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
                            "Services": [  # Group services together
                                {f'Serv Label{i} ': row[f'Serv Label{i} '],
                                 f'SId {i} (Hex)': row[f'SId {i} (Hex)'],
                                 f'LSN {i} (Hex)': row[f'LSN {i} (Hex)']}
                                for i in range(1, 33) if pd.notna(row[f'Serv Label{i} '])],
                            "Lat": row['Lat'],
                            "Long": row['Long']
                        }
                    }
                except Exception as error:
                    # Catching error and logging result
                    LoggerFactory.get_logger().error(f"Unable to parse Data Frame Series: {error}")

                LoggerFactory.get_logger().info(f"Adding entry with ID {row['id']} to dictionary")
                nested_dict.append(entry)  # Adding entries

            # Convert the nested dictionary into a JSON string
            LoggerFactory.get_logger().info(f"Converting nested dictionary into a JSON string with indentation")
            # Writing dictionary to JSON object. Using a NaN converter to clean the NaN's into nulls
            nested_json = json.dumps(nested_dict, indent=4, cls=NaNConverter)

            # Write the JSON string to a file
            with open(json_file_name, 'w') as file:
                LoggerFactory.get_logger().info(f"Writing JSON to file {json_file_name}")
                file.write(nested_json)
            LoggerFactory.get_logger().info(f"File written Successfully")
            return True
        except Exception as error:
            LoggerFactory.get_logger().error(f"An error occurred whilst saving Data Frame to .json File: {error}")
            return False

    def clean_csv_json_data(self):
        self.save_data_frame_to_json(self.json_file_name)
        self.remove_unwanted_NGRs({"NZ02553847", "SE213515", "NT05399374", "NT25265908"}, self.json_file_name)
        self.extract_EID_data(["C18A", "C18F", "C188"], self.json_file_name)
        self.read_in_json_data(self.json_file_name)

    def generate_data_for_in_use_erp_total(self):
        # data_frame = pd.read_json("../temp.json")
        broadcast_info_df = pd.DataFrame(self.data_frame["broadcast_info"])

        erp_total = []
        for index in range(0, len(broadcast_info_df)):
            broadcast_dict = broadcast_info_df["broadcast_info"][index]
            # print(broadcast_info_df)
            try:
                eid = broadcast_dict["EID"]
                if type(eid) == dict:
                    key = list(dict(eid).keys())[0]
                    if broadcast_dict["EID"][key]["Site Height"] > 75 and int(broadcast_dict["Date"][-4:]) >= 2001:
                        erp_total.append(broadcast_dict["EID"][key]["Power (kW)"])

            except:
                LoggerFactory.get_logger().info(f"Unable to get EID")

        print(erp_total)
        counter = 0
        while counter != len(erp_total):
            erp_total[counter] = erp_total[counter].replace(".", "")
            erp_total[counter] = float(erp_total[counter].replace(",", "."))
            counter += 1

        print(f"Mean = {statistics.mean(erp_total)}")
        print(f"Median = {statistics.median(erp_total)}")
        print(f"Mode = {statistics.mode(erp_total)}")

        return statistics.mean(erp_total), statistics.median(erp_total), statistics.mode(erp_total)

    def extract_graph_data(self) -> list:

        graph_data_items = []

        broadcast_info_df = pd.DataFrame(self.data_frame["broadcast_info"])

        for index in range(0, len(broadcast_info_df)):
            broadcast_dict = broadcast_info_df["broadcast_info"][index]
            try:
                eid = broadcast_dict["EID"]
                if type(eid) == dict:
                    graph_data_item = GraphDataItem()
                    eid_value = list(dict(eid).keys())[0]
                    graph_data_item.eid = eid_value
                    graph_data_item.site = broadcast_dict["Site"]
                    graph_data_item.freq = broadcast_dict["Freq."]
                    graph_data_item.block = broadcast_dict["Block"]
                    graph_data_item.serv_label_1 = broadcast_dict["Services"][0]["Serv Label1 "]
                    graph_data_item.serv_label_2 = broadcast_dict["Services"][1]["Serv Label2 "]
                    graph_data_item.serv_label_3 = broadcast_dict["Services"][2]["Serv Label3 "]
                    graph_data_item.serv_label_4 = broadcast_dict["Services"][3]["Serv Label4 "]
                    graph_data_item.serv_label_10 = broadcast_dict["Services"][9]["Serv Label10 "]

                    graph_data_items.append(graph_data_item)
                    # print(graph_data_item)
            except Exception as error:
                LoggerFactory.get_logger().info(f"Unable to get EID")

        return graph_data_items


class GraphDataItem:
    eid: str
    site: str
    freq: float
    block: str
    serv_label_1: str
    serv_label_2: str
    serv_label_3: str
    serv_label_4: str
    serv_label_10: str

    def some_method(self) -> str:
        return self.block
