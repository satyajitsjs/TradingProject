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
   git clone https://github.com/satyajitsjs/trading-project.git
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

5. **Install Redis Server** (Linux):
   - Install Redis on your system using the appropriate package manager:
     ```bash
     sudo apt update
     sudo apt install redis-server
     ```

   - Start the Redis server using the default configuration:
     ```bash
     sudo systemctl start redis-server
     ```

6. **Configure Celery with Redis**:
   - Open `settings.py` in the Django project directory.
   - Update the Celery broker URL and result backend URL to use Redis:
     ```python
     CELERY_BROKER_URL = 'redis://localhost:6379/0'
     CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
     ```

7. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Start Celery Worker**:
   ```bash
   celery -A TradingProject worker -l info
   ```

9. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

10. **Access the Application**:
    - Open a web browser and go to http://localhost:8000/ to access the file upload page.

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
- Celery: Distributed task queue for asynchronous processing.
- Redis: In-memory data structure store used as a message broker for Celery.


