import pandas as pd

BIN_MAPPING = {
    "BLACK RUBBISH WHEELIE BIN": "Rubbish",
    "BLUE RECYCLING WHEELIE BIN": "Recycling",
    "FOOD BOX": "Food",
}

def bins_html(df: pd.DataFrame) -> str:
    df = (
        df
        .assign(bin_short=lambda df: df["bin"].map(BIN_MAPPING))
        .sort_values(["next_collection_days"])
    )

    html_all = "<h3>Bins</h3>\n<ul>"
    for idx, row in df.iterrows():
        html_all += f"\n<li>{row['bin_short']} - {row['next_collection_days']} days</li>"

    return html_all
