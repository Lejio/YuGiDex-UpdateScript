import sqlite3
import os
import json


class updateYuGiDECK:
    
    def __init__(self, dbName: str, lang: str = "en") -> None:

        self.NULL = "NULL"
        self.lang = lang


        self.JSON_DIR = f"./yugioh-card-history/{self.lang}"
        self._con = sqlite3.connect(dbName)
        self._cur = self._con.cursor()
        self.currCard = {
            "id": self.NULL,
            "type": self.NULL,
            "name": self.NULL,
            "englishAttribute": self.NULL,
            "localizedAttribute": self.NULL,
            "effectText": self.NULL,
            "pendEffect": self.NULL,
            "pendScale": self.NULL,
            "level": self.NULL,
            "rank": self.NULL,
            "linkRating": self.NULL,
            "linkArrows": self.NULL,
            "atk": self.NULL,
            "def": self.NULL,
            "properties": self.NULL
        }


    def createTable(self) -> None:

        self._cur.execute("""CREATE TABLE IF NOT EXISTS card (
        id integer PRIMARY KEY,
        type text NOT NULL,
        name text NOT NULL,
        englishAttribute NOT NULL,
        localizedAttribute NOT NULL,
        effectText text NOT NULL,
        pendEffect text,
        pendScale integer,
        level integer,
        rank integer,
        linkRating integer,
        linkArrows integer,
        atk integer,
        def integer,
        properties text 
        )""")


    def formatNameString(self, cardName: str):
        """
            Only formats the " that exists in card names.
        """
        return cardName.replace(r'"', "[quotes]")


    def formatCardString(self, cardDesc):
        """
            Formats the card descriptions so it does not conflict with sqlite syntax.
            Replaces /n and /".
        """

        if cardDesc != self.NULL:
           
            return cardDesc.replace("\n", "[newline]").replace("\"", "[quotes]")


    def insertCard(self, card) -> None:
        """
            Adds a card into the card table.
        """

        try:
            self._cur.execute(f"""INSERT INTO card VALUES ({card['id']}, "{card['type']}", "{self.formatNameString(card['name'])}", "{card['englishAttribute']}", "{card['localizedAttribute']}", "{self.formatCardString(card['effectText'])}", "{self.formatCardString(card['pendEffect'])}", {card['pendScale']}, {card['level']}, {card['rank']}, {card['linkRating']}, "{card['linkArrows']}", {card['atk']}, {card['def']}, "{card['properties']}")
        """)
        except sqlite3.OperationalError:
            print(card)
            exit()

        

    def commitChanges(self) -> None:
        """
            Saves changes to the database.        
        """

        self._con.commit()
        self._con.close()

    def parseJSON(self):
        """
            Gets all the JSON cards in the specified language directory.
        """
        return os.listdir(f"./yugioh-card-history/{self.lang}")


    def createCard(self, card) -> None:
        """
            Transfers all the JSON object data into python dictionary.
        """
        
        for param in card:
            # print(type(card[param]))
            if (param == "type" or param == "englishAttribute"):
                self.currCard[param] = card[param].title()
            else:
                self.currCard[param] = card[param]

    def resetCard(self):
        """
            Resets the current card back to it's original null state.
        """

        self.currCard = {
            "id": self.NULL,
            "type": self.NULL,
            "name": self.NULL,
            "englishAttribute": self.NULL,
            "localizedAttribute": self.NULL,
            "effectText": self.NULL,
            "pendEffect": self.NULL,
            "pendScale": self.NULL,
            "level": self.NULL,
            "rank": self.NULL,
            "linkRating": self.NULL,
            "linkArrows": self.NULL,
            "atk": self.NULL,
            "def": self.NULL,
            "properties": self.NULL
        }

    def buildDB(self):
        """
            Goes to each JSON file and adds the cards into the database.
        """

        self.createTable()
        card_list = self.parseJSON()

        print("Begin building")
        item = 0
        total = len(os.listdir(f"./yugioh-card-history/{self.lang}"))
        for jsonFile in card_list:
            c = json.load(open(f"./yugioh-card-history/{self.lang}/{jsonFile}", encoding="utf-8"))
            self.createCard(card=c)
            self.insertCard(self.currCard)
            item += 1
            print('\r', str(total - item), end = ' items remaining. ')
            self.resetCard()

        self.commitChanges()