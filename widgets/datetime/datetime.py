import datetime as dt

def get_datetime_widget():

    current_time = dt.datetime.now().strftime("%H:%M")
    current_date = dt.datetime.now().strftime("%Y-%m-%d")
    datetime_widget = f"""
    <div><h1>{current_time}</h1></div>
    <div><h3>{current_date}</h3></div>
    """

    return datetime_widget