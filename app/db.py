import dataset 
from config import DATABASE_URL

# Database setup
database = dataset.connect(DATABASE_URL)
users = database['users']
