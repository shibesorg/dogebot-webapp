import dataset 
from config import DATABASE_URI

# Database setup
database = dataset.connect(DATABASE_URI)
users = database['users']
