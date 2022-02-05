import pyrebase, os
from PIL import Image

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
    img = Image.open(path_local)
    img.thumbnail((1000, 1000))
    img.save('lol.png')
    storage.child(path_on_cloud).put('lol.png')
    os.remove('lol.png')

email = "factsworld1109@gmail.com"
password = "help4youisbest"
user = auth.sign_in_with_email_and_password(email, password)

def getfileurl(path_on_cloud):
    url = storage.child(path_on_cloud).get_url(user['idToken'])
    start = url.find('/o/')
    url = 'https://ik.imagekit.io/help4you'+url[start:]
    return url

def getpath(url):
    end = url.find('?')
    start = url.find('/o/')+3
    filtered_url = url[start:end]
    file = filtered_url.split('%2F')
    file = '/'.join(file)
    return file

def delete(path_on_cloud):
    storage.delete(path_on_cloud, None)
    return True

if __name__ == '__main__':
    pass