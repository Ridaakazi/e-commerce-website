# ECommerce Website 

## Description
This is a fully functional e-commerce website with user authentication. It allows users to search for products, view details of items they are interested in, and complete the checkout process. it has also been deployed on this and can be accessed on :http://rida.pythonanywhere.com/

## Features

- List key features of your eCommerce website, such as:
  - User authentication and registration
  - Product browsing and search functionality
  - Shopping cart and checkout process

### Running Flask Application on Windows and macOS

#### Prerequisites:
- Python 3.x installed on your system.
- pip package manager installed.

### E-Commerce Website README

#### Features:
- Search functionality to search for products.
- User authentication for secure login and registration.
- Shopping cart and checkout functionality.
- Integration with SQL database for storing product details, user information, and orders.

#### Technologies Used:
- Flask: Micro web framework for Python.
- SQLAlchemy: Python SQL toolkit and Object-Relational Mapper.
- HTML/CSS: Frontend development.
- Jinja2: Template engine for Flask.
- MySQL: Database.

#### Setup Instructions:

1. **Download Zip file:**

2. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Set Environment Variables:**
   - Create a `.env` file in the root directory.
   - Add your environment variables:
     ```
     FLASK_APP=app.py
     FLASK_ENV=development
     SECRET_KEY=your_secret_key
     DATABASE_URL=your_database_url
     ```

4. **Database Setup:**
   - Create the necessary tables in your database. You can use SQLAlchemy to handle this.

5. **Running the Application:**

   On Windows:
   ```
   set FLASK_APP=app.py
   set FLASK_ENV=development
   flask run
   ```

   On macOS/Linux:
   ```
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run
   ```

6. **Access the Application:**
   Open your web browser and go to `http://localhost:5000`.

#### Usage:

- Visit the homepage to browse products, register, or log in.
- Use the search bar to find specific products.
- Add products to the shopping cart and proceed to checkout.
- Only logged-in users can checkout. 
