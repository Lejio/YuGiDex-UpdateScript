from db_create import updateYuGiDECK
from ftplib import FTP
from dotenv import load_dotenv
import git
import os

class Update:

    def __init__(self, webserver: str = "ftp.geneni.info", extension: str = ".db"):

        self.DIR_NAME = './yugioh-card-history'
        self.DB_NAME = 'yugidb'
        self.EXTENSION = extension
        self.WEBSERVER = webserver
        load_dotenv()

        repo = git.Repo(self.DIR_NAME)
        repo.remotes.origin.pull()

    def clean(self, lang: list):

        for i in lang:

            db_name = f"{self.DB_NAME}{i}{self.EXTENSION}"
            os.remove(db_name)

    def create(self, lang: list):

        for i in lang:

            db_name = f"{self.DB_NAME}{i}{self.EXTENSION}"
            db = updateYuGiDECK(db_name)
            db.buildDB()

    def upload(self, lang: list):

        username = os.getenv('FTP_USERNAME')
        password = os.getenv('FTP_PASSWORD')

        

        ftp = FTP(self.WEBSERVER, user=f"{username}", passwd=f"{password}")
        ftp.cwd('./yugidexdb')

        for i in lang:

            db_name = f"{self.DB_NAME}{i}{self.EXTENSION}"
            upload = open(db_name, "rb")
            ftp.storbinary(f"STOR {db_name}", upload)
            upload.close()
        
        ftp.retrlines('LIST')
        ftp.close()
