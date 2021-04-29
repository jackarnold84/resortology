## Resortolgy
### CS348 Databases Project

### Authors:
Jack Arnold (github.com/jackarnold84)  
Rohan Shahani (github.com/rshahani999)  
Emily Blanchard (github.com/emlyblnchrd)  

### Description:

A toy-website for managing a hotel/resort. The app will allow users to assign customers to room 
reservations, manage payments, calculate revenue, and more. The target users are hotel staff 
and managers.

### To run locally:

1. cd into the main directory
2. install the requirements `pip install -r requirements.txt`
3. run `python app.py`
4. open a web browser and go to `http://127.0.0.1:5000/`

### Connect to database:

The app uses a MySQL database hosted on Google Cloud Platform. To connect, the appropriate connection
info must be provided in the file `db_connect_info.json`. Additonally, the path variable 
`connect_file_path` must be set accordingly in `database.py`.
