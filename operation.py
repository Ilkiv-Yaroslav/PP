from main import *

session = Session()

user2 = User(id = 1,
                     username="petro228",
                     firstName="Peter",
                     lastName="Dada",
                     email="petro.dada.hnm@lpnu.ua",
                     password="drowssap",
                     phone="88005553535",
                     userStatus="1")
session.add(user2)
session.commit()


user4 = User(id = 2,
                     username="Peret1337",
                     firstName="Peret",
                     lastName="Nene",
                     email="Peret.Nene.hnm@lpnu.ua",
                     password="psadasd",
                     phone="88005553535",
                     userStatus="2")
session.add(user4)
session.commit()


user7 = Student(
                    id = 1,
                    name = "Peter",
                    lastName = "Dada",
                    avarageMark = 88,
                    User_id = user2.id)

user8 = Student(
                    id = 2,
                    name = "Peret",
                    lastName = "Nene",
                    avarageMark = 20,
                    User_id = user4.id)


session.add(user7)
session.commit()
session.add(user8)
session.commit()

print(session.query(User).all()[0])


#cd C:\Users\s\PycharmProjects\PythonWeb\env\Scripts
#activate.bat
#alembic upgrade head
#alembic revision --autogenerate