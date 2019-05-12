from sqlalchemy import create_engine

from barlibrary.models.meta import Base

def main():
    engine = create_engine('sqlite:///recipeDB.db', echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
