# Gothon Web

Final exercise from "Learn Python 3 the Hard Way" (Zed Shaw).

Simple storytelling webgame with the purpose of learning Python and Flask framework.


## Flask

- Login system using `flask-login`
- Forms and validators using `flask-wtf`
- Password encryption using `flash-bcrypt`
- ORM using `flask-sqlalchemy` with `SQLite`
- Database migration using `flask-migrate`. The migration commands may be accesses through the `manage.py` (`flask-scripts` functionality)
- E-mail system using `flask-mail` (sends an e-mail when user is registered)
- Locale of timestamps (UTC to client time) is managed using `flask-moment`
- Configuration environments (`development`, `testing`, and `production`) and Blueprints (`main`) are being used.
- Unitary tests using Pytest

## Pages

- Home
- Games: Gothon | Riddle Master | World Flags Quiz
- Login
- Signup
- Ranking
    
## TODO

  - Bug no handler do next page do login
  - Melhorar aparência HTML  
  - Sistema de ajuda  
  - Sistema de pontuação
  - Jogos: 
    - Melhorar GothonWeb
    - Criar Riddle Master
    - Criar World Flags Quiz
  - Aumentar a cobertura dos testes automatizados