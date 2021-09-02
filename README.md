### Google Calendar Adapter

A command line application which allows calendar data stored in a MySQL database to be converted and synched with Google Calendar.

Initially, Luigical accepts a .csv file containing calendar data (formatted with Google calendar headers), converts it to the corresponding Google calendar json format, and batch uploads the events to an associated Google account. When changes are made in the MySQL database, a new .csv can be exported and compared to the previous .csv. The changes are recorded, converted to json, and uploaded to Google Calendar. 



```
docker build -t luigical .

docker run -dp 3000:3000 luigical
```
