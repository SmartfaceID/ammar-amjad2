# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 21:32:29 2025

@author: Obaid
"""

import json
from getpass import getpass
from live_verify import verify_live_face

def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("[!] users.json not found.")
        return []

def login_with_credentials():
    users = load_users()
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print(f"[✓] Welcome, {username}!")
            return True

    print("[!] Invalid username or password.")
    return False

def login_menu():
    while True:
        print("\n=== Login Menu ===")
        print("1. Login with Face ID (Camera)")
        print("2. Login with Username & Password")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            print("[+] Starting Face ID login...")
            verify_live_face()  # سيتم عرض التعرف والكاميرا
        elif choice == "2":
            login_with_credentials()
        elif choice == "3":
            print("[!] Exiting login system.")
            break
        else:
            print("[!] Invalid choice. Try again.")
