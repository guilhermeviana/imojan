from app import Base, engine

# Você precisa informar as classes que representam tabelas
from app.models.tables import User, Homes

print('Apagando banco de dados')
# apagando o BD
Base.metadata.drop_all(engine)




print('Criando banco de dados ...')
# criando o BD
Base.metadata.create_all(engine)

print('Banco de dados criado')
