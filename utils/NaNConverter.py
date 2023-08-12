import math
from json import JSONEncoder

class NaNConverter(JSONEncoder):
    """
        A class that will convert NaN string variables
        to None for .json files.
    """
    def default(self, obj):
        # possible other customizations here
        pass

    def encode(self, obj, *args, **kwargs):
        obj = NaNConverter.nan_to_none(obj)
        return super().encode(obj)

    def iterencode(self, obj, *args, **kwargs):
        obj = NaNConverter.nan_to_none(obj)
        return super().iterencode(obj, *args, **kwargs)

    @staticmethod
    def nan_to_none(obj):
        if isinstance(obj, dict):
            return {k: NaNConverter.nan_to_none(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [NaNConverter.nan_to_none(v) for v in obj]
        elif isinstance(obj, float) and math.isnan(obj):
            return None
        return obj
