import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Firebase setup
cred = credentials.Certificate(r'C:\Users\Archit Bhullar\OneDrive\Documents\code\SI2255.1P\gyroscope-data-capture-firebase-adminsdk-6slb0-bcd12bd707.json')  
firebase_admin.initialize_app(cred)
db = firestore.client()

# Fetch data from Firebase
print("Fetching data from Firebase...")

docs = db.collection('gyroscope_data').stream()

data_list = []
for doc in docs:
    data = doc.to_dict()
    data_list.append([data['timestamp'], data['gx'], data['gy'], data['gz']])

# Convert the list to a pandas DataFrame
df = pd.DataFrame(data_list, columns=['timestamp', 'gx', 'gy', 'gz'])

# Save the DataFrame to a CSV file
df.to_csv('gyroscope_data_firebase.csv', index=False)

print(f"Data saved to CSV file. {len(data_list)} records collected.")
