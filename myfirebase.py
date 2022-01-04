import pyrebase

config = {
    "apiKey": "AIzaSyA2QGz5kPdvFmg90xhDxy2FzCf9_mKOPWE",
    "authDomain": "freestorage-dfe15.firebaseapp.com",
    "databaseURL": "https://freestorage-dfe15-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "freestorage-dfe15",
    "storageBucket": "freestorage-dfe15.appspot.com",
    "messagingSenderId": "221659926279",
    "appId": "1:221659926279:web:f6a601f45bcf30cc687fa2",
    "measurementId": "G-PNNCK2Z5PC"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()


def upload(path_local, path_on_cloud):
    storage.child(path_on_cloud).put(path_local)
    return True

email = "factsworld1109@gmail.com"
password = "help4youisbest"
user = auth.sign_in_with_email_and_password(email, password)

def getfileurl(path_on_cloud):
    url = storage.child(path_on_cloud).get_url(user['idToken'])
    return url

if __name__ == '__main__':
    pass
