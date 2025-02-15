## Holiday Management Application

## Overview

This is the backend service for the Holiday Management Application, built with Django and Django REST Framework (DRF). It interacts with the Calendarific API to fetch holiday data, caches the results, and serves them to the frontend.

## Features

1. Fetch holidays from Calendarific API.

2. Cache holiday data for each country and year combination to reduce API calls.

3. Search holidays by name.

4. Provide a REST API for the frontend to consume.

## Tech Stack

1. Django

2. Django REST Framework (DRF)

3. SQLite (default database)

4. Django's caching framework

5. Python-dotenv (for environment variable management)


## Installation

1. Clone the Repository
   git clone https://github.com/anshaduk/HolidayManagement-Backend.git

2. Create and Activate a Virtual Environment
   python -m venv myenv
   myenv\Scripts\activate 

3. Install Dependencies
   pip install -r requirements.txt

4. Set Up Environment Variables
   Create a .env file in the root directory and add the following:
   CALENDARIFIC_API_KEY=your_api_key_here

5. Run Migrations

6. Run Server

## API Endpoints
-  /holidays/
-  /holidays/search/


