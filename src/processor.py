import pandas as pd

def process_data(df):
    result = df.copy()
    result["packets_per_second"] = result["packet_count"] / result["duration"].clip(lower=0.1)
    result["bytes_per_second"] = result["bytes"] / result["duration"].clip(lower=0.1)
    result["port_range"] = pd.cut(result["destination_port"], [0, 1024, 49151, 65535], labels=[0, 1, 2], include_lowest=True).astype(int)
    return result