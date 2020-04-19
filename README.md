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


## Pages

- Game (index)
- Login
- Ranking
    
## TODO
  
  - Quem está logado (nav-bar)
  - Sistema de ajuda
  - Melhorar aparência HTML  
  - Sistema de pontuação
  - Escolha de jogo (incluir quizzes)
  - Aumentar a complexidade do mapa
  - Aumentar a cobertura dos testes automatizados