import sqlite3
import re
import sys
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def backup():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
# Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    exists = False
    for file1 in file_list:
        if (file1['title'] == 'contacts.db'):
            exists = True
            fileid = file1['id']
            break
    if(exists):
        with open("contacts.db", "r") as file:
            file = drive.CreateFile({'id': fileid})
            file.SetContentFile("contacts.db")
            file.Upload()
    else:
        with open("contacts.db","r") as file:
            file = drive.CreateFile()
            file.SetContentFile("contacts.db")
            file.Upload()
            print('Backup successful!!!')


conn = sqlite3.connect('contacts.db')
c = conn.cursor()


def insert(user_id):
    flag = True
    while(flag):
        print('Enter name')
        name = input()
        if len(name)>50 or len(name)<=0:
            print('Invalid name try again')
        else:
            flag = False

    flag = True
    while flag:
        print('Enter number')
        number = input()
        if len(number)!=10 or not number.isdigit():
            print('Invalid number try again')
        else:
            number = int(number)
            rows = c.execute('SELECT number FROM contacts WHERE number=? AND user_id=?', (number, user_id))
            l = 0
            for row in rows:
                l += 1
                if(l > 0):
                    break
            if(l > 0):
                print('This number already exists!')
            else:
                flag = False
    flag = True
    while flag:
        print('Enter Address')
        address = input()
        if(len(address) < 10 or len(address)>200):
            print('Invalid address try again')
        else:
            flag = False
    flag = True
    while flag:
        print('Enter Email')
        email = input()
        if(not re.search("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email)):
            print('Invalid email try again')
        else:
            flag = False

    c.execute('INSERT INTO contacts VALUES(?, ?, ?, ?, ?)', (name, number, address, email, user_id))
    conn.commit()
    print('Contact inserted successfully')

def delete(user_id):
    print('Enter a number to delete')
    num = int(input())
    rows = c.execute('SELECT number FROM contacts WHERE number=? AND user_id=?', (num, user_id))
    l = 0
    for row in rows:
        l += 1
    if (l == 0):
        print('No contact found with given number:(')
    else:
        c.execute('DELETE FROM contacts WHERE number=? AND user_id=?', (num, user_id))
        conn.commit()
        print('Contact deleted successfully')

def show(user_id):
    c.execute('SELECT * FROM contacts WHERE user_id=? ORDER BY name', (user_id, ))
    rows = c.fetchall()
    l = 0
    for row in rows:
        l += 1
        if(l > 0):
            break
    if(l == 0):
        print('no contacts found :(')
    else:
        c.execute('SELECT name, number, address, email FROM contacts WHERE user_id=? ORDER BY name', (user_id,))
        rows = c.fetchall()
        for row in rows:
            print(row)

def update(user_id):
    print('Enter a contact number to update')
    num = int(input())
    rows = c.execute('SELECT number FROM contacts WHERE number=? AND user_id=?', (num, user_id))
    l = 0
    for row in rows:
        l += 1
    if(l == 0):
        print('No contact found with given number:(')
    else:
        flag = True
        while (flag):
            print('Enter name')
            name = input()
            if len(name) > 50 or len(name) <= 0:
                print('Invalid name try again')
            else:
                flag = False

        flag = True
        while flag:
            print('Enter number')
            number = input()
            if len(number) != 10 or not number.isdigit():
                print('Invalid number try again')
            else:
                number = int(number)
                rows = c.execute('SELECT number FROM contacts WHERE number=? AND user_id=? AND number!=?', (number, user_id, num))
                l = 0
                for row in rows:
                    l += 1
                    if (l > 0):
                        break
                if (l > 0):
                    print('This number already exists!')
                else:
                    flag = False
        flag = True
        while flag:
            print('Enter Address')
            address = input()
            if (len(address) < 10 or len(address) > 200):
                print('Invalid address try again')
            else:
                flag = False
        flag = True
        while flag:
            print('Enter Email')
            email = input()
            if (not re.search("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email)):
                print('Invalid email try again')
            else:
                flag = False
        c.execute('UPDATE contacts SET name=?, number=?, address=?, email=? WHERE number=? AND user_id=?', (name, number, address, email, num, user_id))
        conn.commit()
        print('Contact updated successfully')

def search(user_id):
    print('1-Search by name')
    print('2-search ny number')
    num = int(input())
    if(num == 1):
        print('Enter a name')
        name = input()
        l = 0
        rows = c.execute('SELECT * FROM contacts WHERE name=? AND user_id=?', (name, user_id))
        for row in rows:
            l += 1
            if(l > 0):
                break
        if(l==0):
            print('No contacts found by this name :(')
        else:
            rows = c.execute('SELECT name, number, address, email FROM contacts WHERE name=? AND user_id=?', (name, user_id))
            for row in rows:
                print(row)
    elif(num == 2):
        print('Enter a number')
        n = int(input())
        l = 0
        rows = c.execute('SELECT * FROM contacts WHERE number=? AND user_id=?', (n, user_id))
        for row in rows:
            l += 1
            if (l > 0):
                break
        if (l == 0):
            print('No contacts found by this name :(')
        else:
            rows = c.execute('SELECT * FROM contacts WHERE number=? AND user_id=?', (n, user_id))
            for row in rows:
                print(row)
    else:
        print('Invalid choice')

def menu(user_id):
    while True :
        print('1-Insert Contact')
        print('2-Delete contact')
        print('3-Update Contact')
        print('4-Show Contact')
        print('5-Search Contact')
        print('6-Exit')
        option = int(input())
        if option == 1:
            insert(user_id)
        elif option == 2:
            delete(user_id)
        elif option == 3:
            update(user_id)
        elif option == 4:
            show(user_id)
        elif option == 5:
            search(user_id)
        elif option == 6:
            conn.close()
            sys.exit()
        else:
            print('Invalid input')


rows = c.execute('SELECT * FROM users')
for row in rows:
    print(row)
print('1-Register')
print('2-Login')
print('3-Exit')
print('4-Backup')
opt = int(input())
if(opt == 1):
    flag = True
    while(flag):
        username = input('Enter a username')
        if(len(username) <3 or len(username)>25):
            print('username length should be between 3 and 25')
            flag = True
        else:
            rows = c.execute('SELECT username FROM users WHERE username=?', (username, ))
            l = 0
            for row in rows:
                l += 1
                if(l > 0):
                    break
            if(l > 0):
                print('Username taken try another')
            else:
                password = input('Enter a password')
                if(len(password) < 8 or len(password) > 16):
                    print('password length should be between 8 and 16')
                    flag = True
                else:
                    c.execute('INSERT INTO users VALUES(null, ?, ?)', (username, password, ))
                    conn.commit()
                    print('Successfully registered. Start making contacts!')
                    rows = c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password,))
                    for row in rows:
                        user_id = row[0]
                    menu(user_id)
                    flag = False

elif(opt == 2):
    flag = True
    while(flag):
        username = input('Enter your username')
        rows = c.execute('SELECT username FROM users WHERE username=?', (username, ))
        l = 0
        for row in rows:
            l += 1
            if(l > 0):
                break
        if(l != 1):
            print('Username doesn\'t exist. Try again')
        else:
            password = input('Enter your password')
            rows = c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password, ))
            l = 0
            for row in rows:
                l += 1
                if (l > 0):
                    break
            if(l == 0):
                print('username and password didn\'t match. Try again')
            else:
                rows = c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password,))
                print('You are logged in!!')
                for row in rows:
                    user_id = row[0]
                flag = False
                menu(user_id)
elif(opt == 3):
    conn.close()
    sys.exit()
elif(opt == 4):
    backup()
else:
    print('Invalid input')
