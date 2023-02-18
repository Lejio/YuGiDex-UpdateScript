from db_create import updateYuGiDECK
from ftplib import FTP
from dotenv import load_dotenv
import git
import os


if __name__ == "__main__":

    load_dotenv()
    repo = git.Repo('./yugioh-card-history')
    


    db_name = "yugidbEN.db"
    
    try:
        os.remove(db_name)
    except FileNotFoundError:
        pass
    
    db = updateYuGiDECK(db_name)
    db.buildDB()

    username = os.getenv('FTP_USERNAME')
    password = os.getenv('FTP_PASSWORD')

    upload = open(db_name, "rb")

    ftp = FTP('ftp.geneni.info', user=f"{username}", passwd=f"{password}")
    ftp.retrlines('LIST')
    ftp.cwd('./yugidexdb')
    ftp.storbinary(f"STOR {db_name}", upload)
    ftp.retrlines('LIST')

    upload.close()
    ftp.close()
    
    print("\n########################################################\n")
    print("Upload Completed.")


    
