class GraphDataItem:
    """
        Data Item to hold required data for the Graph and Correlation Data
        Used like a Data Transfer Object, DTO
    """

    # Data that can be stored in this Data Item
    eid: str
    site: str
    freq: float
    block: str
    serv_label_1: str
    serv_label_2: str
    serv_label_3: str
    serv_label_4: str
    serv_label_10: str
