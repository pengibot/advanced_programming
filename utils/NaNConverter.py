import math
from json import JSONEncoder

from utils import LoggerFactory


class NaNConverter(JSONEncoder):
    """
        A class that will convert NaN string variables
        to None for .json files.
    """
    def default(self, obj):
        """
            Overriding JSONEncoder for possible future enhancements
            to the default behaviour.
        """
        # possible other customizations here
        pass

    def encode(self, obj, *args, **kwargs):
        """
            Overridden method from JSONEncoder
            Call custom nan_to_none() methods
            before calling super for normal behaviour.
        """
        obj = NaNConverter.nan_to_none(obj)  # Call to customized method
        return super().encode(obj)

    def iterencode(self, obj, *args, **kwargs):
        """
            Overriding JSONEncoder to call nan_to_none() method
            on object.
        """
        obj = NaNConverter.nan_to_none(obj)  # Call to customized method
        return super().iterencode(obj, *args, **kwargs)

    @staticmethod
    def nan_to_none(obj):
        """
            A recursive method to drill down and replace NaN objects with None/Null
        """
        if isinstance(obj, dict):  # Check if the object is a Dictionary
            return {k: NaNConverter.nan_to_none(v) for k, v in obj.items()}  # Recursive Call
        elif isinstance(obj, list):  # Check if the obj is a List
            return [NaNConverter.nan_to_none(v) for v in obj]  # Recursive Call
        elif isinstance(obj, float) and math.isnan(obj):  # Check if object is a float and set to NaN
            LoggerFactory.get_logger().debug("Detected a NaN object. Converting NaN to null")
            return None  # return None in its place
        return obj  # return original object
