# Auction System- Django

### Requirements

- `Python3.10.8 frameworks/packages` :
  - `Django`
  - `Pillow`
- `Browser` (Preferably `Chrome`)

### Setup

- Clone the repo using `git clone https://github.com/Hamza-Azeem1/Auction-system.git`

- Using a Python virtual environment recommended

- If you have `Python` installed but not `Django` or `Pillow`:

  - run `pip install django pillow`

- Then run the following command to install dependencies:
  - `pip install -r requirements.txt`

- Then run these commands:
 - `python manage.py makemigrations`
 - `python manage.py migrate`

- To run the website in a development server:
  -run `python manage.py runserver`

### Additional Setup

- To create a super user for the website simply run:

  - `python manage.py createsuperuser`

- Then, enter credentials such as username, email and password for the account

- After running the website in a local port (Django defaults to port 8000) using `python manage.py runserver`:
  - Visit `localhost:8000/admin` and login with the credentials created earlier
  - Upon logging in successfully, you should be able to access the **django admin interface**

### Files and Directories

- The crucial files in the repo home directory are:

  - `manage.py` : the python file required to run the website

- The `auctions` directory has the files for the auction application which includes:

  - `views.py`: server side code for the website
  - `urls.py`: the urls that determine which associates url extensions to the views from `views.py` file
  - `models.py`: the tables needed for the `sqlite3` database
  - `decorators.py`: functions that add a layer of security concerning logged-in and logged-out users
  - `admin.py`: adds the database tables to be modified in the django admin interface
  - `forms.py`: to create forms for easier access of `POST` data from the `HTML` forms
  - `templates` directory: consists of all the `HTML` files to be rendered
  - `static` directory: consists of files such as `CSS` and images used in the web page
  - `uploads` directory: consists of images from the ImageField in the database table

- The `commerce` directory has the files for crucial for the functions of the auction application which includes:

  - `settings.py`: consists of all the settings for the whole web application
  - `urls.py`: the main urls file with the urls from all the apps in the web application (such as auctions)

### Credits

- Implemented by **Hamza Azeem**
- Contact me at: <hamzaazeem023@gmail.com>
