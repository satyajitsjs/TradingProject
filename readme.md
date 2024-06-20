# Trading Project

The Trading Project is a Django web application that allows users to upload CSV files containing financial data, process the data according to specified timeframes, and download the processed data in JSON format.

## Project Structure

The project structure is as follows:

- **TradingProject**: Django project directory.
  - **MainApp**: Django app for handling file uploads, data processing, and JSON file generation.
  - **templates**: Directory containing HTML templates.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/trading-project.git
   ```

2. **Navigate to Project Directory**:
   ```bash
   cd TradingProject
   ```

3. **Create Virtual Environment** (optional but recommended):
   ```bash
   virtualenv envsmart
   .\envsmamrt\Scripts\activate
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**:
   - Open a web browser and go to http://localhost:8000/upload/ to access the file upload page.

## Usage

1. **Upload CSV File**:
   - Navigate to the upload page and select a CSV file to upload.
   - Enter the desired timeframe (in minutes) for data processing.

2. **Processing and Download**:
   - The uploaded CSV file will be processed.
   - Once processing is complete, a download link for the JSON file will be provided.
   - The JSON file contains the processed data based on the specified timeframe.

## Technologies Used

- Django: Web framework for backend development.
