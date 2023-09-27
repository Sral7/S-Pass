# S-Pass

S-Pass is a password mangement website built using Django, orginally built with the wxPython module. I decided to that a good way to practice html/css and Django would be to make that project into a website and have the UI built using html and css.
With S-Pass a user can create an account to securely store their username/email/password for any site. The encryption process uses key dervation to derive an encryption key based on the users master password and their decryption pin. The derived key is then used to 
encrypt and decrypt the data added to S-Pass. If any security flaws or issues presents itself please notify me so I could try and fix it and learn why this could be an issue. The next step for this project is to implement js scripts which I haven't done as I haven't learned Js yet to make a more interactive and pleasing website. Install and run locally with virtual enviroment, steps:

1.Clone the GitHub repository to your local machine using git clone <repository-url>.
2.Navigate to the project folder in the terminal or command prompt.
3.Install pipenv using pip by running the command pip install pipenv.
4.Create a new virtual environment for the project using pipenv by running the command pipenv install. This will create a new virtual environment and install all the required packages specified in the Pipfile.lock file.
5.Activate the virtual environment by running the command pipenv shell.
6.Create a new file named .env in the project folder and add the following lines to it: SECRET_KEY=<your-secret-key>, DEBUG=True
7.Replace <your-secret-key> with a secret key of your choice. 7. Run the Django migrations using the command python manage.py migrate. 
8. Create a superuser account using the command python manage.py createsuperuser and follow the prompts to enter your desired username, email, and password. 
9. Run the development server using the command python manage.py runserver. 
10. Open a web browser and navigate to http://localhost:8000 to view the website. You can log in to the admin panel by navigating to http://localhost:8000/admin and entering your superuser credentials.

