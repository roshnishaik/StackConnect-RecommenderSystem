import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


if (not len(firebase_admin._apps)):
	# Fetch the service account key JSON file contents
	cred = credentials.Certificate('firebase_key.json')
	# Initialize the app with a service account, granting admin privileges
	firebase_admin.initialize_app(cred, {
	    'databaseURL': 'https://stackconnect.firebaseio.com/'
	})

ref = db.reference('/active_user')



def upload_user(data):
	ref.set(data)