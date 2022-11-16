# csce5550_group18_ransomware
Ransomeware Project For Group 18: CSCE 5550
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
# Version 1.0a 11/15/2022
#######################################################################################################################
#######################################################################################################################
# Instructions:
# Step 1: CHANGE GLOBAL VARIABLES FOR DIRECTORY USE
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
