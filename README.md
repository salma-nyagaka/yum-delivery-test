# yum-delivery-test
Simple backend to that has an authentication API and displays a leave management system

#### How to setup the project
- Clone the repository 
- Change directory to yum-delivery-test
- Setup the virtual environment
`virtualenv venv`
`source venv/bin/activate`
- Install the dependancies
`pip3 install -r requirements.txt`
- Create a database and a .env file to have your database url
- Run source .env to export the variables for your environment
- Make migrations to your database
`python manage.py migrate`
-Start the development server
`python manage.py runserver`
