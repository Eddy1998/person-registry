from backend.database import Base, engine
from backend.models import Person, PersonalData, Residence


Base.metadata.create_all(bind=engine)

print("Tables created successfully.")