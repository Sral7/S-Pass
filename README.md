# S-Pass

S-Pass is a password management website built using Django, originally built with the wxPython module. The UI is built using HTML and CSS.

With S-Pass, a user can create an account to securely store their username/email/password for any site. The encryption process uses key derivation to derive an encryption key based on the user's master password and their decryption pin. The derived key is then used to encrypt and decrypt the data added to S-Pass. Please feel free to test the site (currently being hosted with Heroku): [https://s-pass-4eb6b9b2c8d8.herokuapp.com/]. However, there is a cap of five sites that can be added to limit costs as this is a personal project. If any security flaws or issues present themselves, please notify me so I can try to fix them and learn why they could be an issue.

Features
- User authentication: Users can create accounts and log in to the application.
- Password management: Users can add, edit, and delete passwords for their websites, which are then encrypted before being saved into a PostgreSQL database.
- Generate passwords: Generate secure and customizable passwords (customizable length, types of characters used, and readability (either full random or employ real words inside the passwords)).
- Settings: Users can change their master passwords, decryption pin, and their default password generation settings, which are used when generating a password in the edit/add site pages.
- UI: Responsive website design and displays the logo of each website added.

    
    

