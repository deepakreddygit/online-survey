
# Online Survey Platform

## Project Overview
The Online Survey Platform is a web-based application that allows users to:
- **Create Surveys**: Design surveys with titles and descriptions.
- **Manage Surveys**: View a list of created surveys.
- **Collect Responses**: Allow users to respond to surveys.
- **Visualize Data**: Display survey responses in a chart for better data analysis.

## Steps to Set Up and Run the Code

### 1. Clone the Repository
```bash


git clone <repository_url>
cd OnlineSurveyPlatform


2. Set Up a Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\\Scripts\\activate    # For Windows


3. Install Dependencies
pip install -r requirements.txt
4. Set Up the Database
For SQLite (Development): Ensure app/models.py is set up to use SQLite.


flask db init
flask db migrate -m "Initial migration"
flask db upgrade
For PostgreSQL (Production): Update your DATABASE_URL in the environment variables.



5. Run the Flask Application
flask run
The app will run on http://127.0.0.1:5000/.

6. Access the Application
Open your browser and navigate to http://127.0.0.1:5000/.
Register or log in to start creating surveys and collecting responses.