# Gothon Starship Games

Project with the purpose of learning Python and Flask framework. The project is inspired in the final exercise from "Learn Python 3 the Hard Way" (Zed Shaw) and in the exercises from "Flask Web Development: Developing Web Applications with Python" (Miguel Grinberg).

Three room based games were implemented: 
  - Escape Gothon: simple storytelling webgame adapted from Zed Shaw's book (simple example)
  - Riddle Master: a riddle game
  - World Flag Quiz: country's flag quiz game


## Flask Technologies

- Login system using `flask-login`
- Forms and validators using `flask-wtf`
- Password encryption using `flash-bcrypt`
- ORM using `flask-sqlalchemy` with `SQLite`
- Database migration using `flask-migrate`. The migration commands may be accessed through the `manage.py` (`flask-scripts` functionality)
- E-mail system using `flask-mail` (sends an e-mail when user is registered)
- Locale of timestamps (UTC to client time) is managed using `flask-moment`
- Server-side sessions using `flask-session` (fork from `rayluo/flask-session` to fix werkzeug incompatibility)
- Environments configuration (`development`, `testing`, and `production`)
- Blueprints (`main`, `auth`, `game`) are being used.
- Unitary tests using Pytest


## Features

- Homepage
- Authentication System:
  - Login page
  - Signup page
  - Confirmation e-mail. Tokens are generated using JSON Web Signature from `itsdangerous`
  - Unconfirmed e-mail page. It is possible to resend the confirmation e-mail if expired or invalid
- Games: Gothon | Riddle Master | World Flags Quiz
- Ranking page
    
## TODO

  - Games:
    - Create more rooms for "Riddle Master"
    - Create more rooms for "World Flags Quiz"
  - User:
    - Recover password system
    - Avatar image using Gravatar API
    - Profile page: update avatar image and change password
  - Increase the coverage of automation tests