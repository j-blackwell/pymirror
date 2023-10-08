# Smart Mirror

This is the code for a smart mirror in python.
The code needs two services to run:

## Services

### Web
The first service is to serve the web page that renders the widgets.

```bash
uvicorn app.main:app --reload
```

### Updates
The second service is to run the python script that handles the widget updates.
```bash
python3 ./widgets/update.py
```


## ENV vars needed

- SQLITE
- WEATHER_API_KEY
- WEATHER_LAT
- WEATHER_LON
- POST_CODE
- TFL_LINE_IDS
- TFL_STOP_POINT_IDS
- TFL_API_KEY
- TIMEZONE
- TEAM_ID