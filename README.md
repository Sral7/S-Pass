# S-Pass

S-Pass is a password mangement website built using Django, orginally built with the wxPython module. I decided to that a good way to practice html/css and Django would be to make that project into a website and have the UI built using html and css.
With S-Pass a user can create an account to securely store their username/email/password for any site. The encryption process uses key dervation to derive an encryption key based on the users master password and their decryption pin. The derived key is then used to 
encrypt and decrypt the data added to S-Pass. Please feel free to test the site[currently being hosted with heroku]: [ https://s-pass-4eb6b9b2c8d8.herokuapp.com/ ]. However I've set a cap of five sites which can be added to limit costs as this is a personal project. If any security flaws or issues presents itself please notify me so I could try and fix it and learn why this could be an issue. 
 
Features

    User authentication: Users can create accounts and log in to the application.
    Password management: Users can add, edit, and delete passwords for their websites which are then encrypted before being saved into a postgres database.
    Generate Passwords: Generate secure and customizable passwords [customizable length, types of characters used, and readability(either full random or employ real words inside the passwords)].
    Settings: Users can change their master passwords, decryprion pin and their default password generation settings which are used when generating a password in the edit/add site pages.
    UI: Responsize website design and displays logo of each webiste added.
    
    

