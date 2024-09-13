# EC252 Project: **DoctorFinder**

**DoctorFinder** is a web-based application that simplifies making doctor appointments. It helps users by:
- Displaying estimated wait times
- Providing real-time updates on the number of patients ahead
- Allowing users to search for doctors across multiple clinics in one convenient place

## Project Structure

### 1. **Website Directory**
- **app/**: Contains the core files for the website
  - **templates/**: HTML files for the user interface
  - **static/**: CSS and JavaScript files for styling and interactivity
  - **stuff.py**: Defines the classes used in the project
  - **routs.py**: Manages the routes and handles requests for the website
  - **\_\_init\_\_.py**: Sets up the project configuration, including database connections and session management
- **run.py**: Script to run the application

### 2. **Database**
- **DoctorFinder_Database_creater.sql**: SQL script to create the database schema for the project

## How to Run the App

### Prerequisites
1. Install **MySQL Workbench** (or another MySQL client)
2. Install necessary Python libraries (you can use `pip install` for this)

### Step 1: Set Up the Database
1. Run the **DoctorFinder_Database_creater.sql** file in your MySQL client to create the necessary tables.
2. Open the **\_\_init\_\_.py** file and update the MySQL connection configuration with your own MySQL username and password:

   ```python
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = 'your-password'

### Step 2: Install Required Libraries
Make sure you have all the required libraries installed:
1. flask
   ```bash
   pip install flask
3. flask_mysqldb
   ```bash
   pip install flask_mysqldb

### Step 3: Run the Application
To run the app, run the `run.py` file:
  ```bash
  python run.py
```
it will be accessible at `http://localhost:5000`.


