# Gothon Web

Final exercise from "Learn Python 3 the Hard Way" (Zed Shaw).

Simple storytelling webgame with the purpose of learning Python and Flask framework.


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
  - Unconfirmed e-mail page. It is allowed to resend confirmation e-mail if expired or invalid

- Games: Gothon | Riddle Master | World Flags Quiz
- Login
- Signup
- Ranking
    
## TODO

  - Melhorar aparência HTML  
  - Sistema de ajuda  
  - Sistema de pontuação
  - Jogos: 
    - Melhorar GothonWeb
    - Criar Riddle Master
    - Criar World Flags Quiz
  - Aumentar a cobertura dos testes automatizados