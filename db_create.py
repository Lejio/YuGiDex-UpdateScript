import sqlite3
import os
import json


class updateYuGiDECK:
    
    def __init__(self, dbName: str, lang: str = "en") -> None:

        self.NULL = "NULL"
        self.lang = lang

        self.JSON_DIR = f"./yugioh-card-history/{self.lang}"
        self.NEW_DIR = self.JSON_DIR + "/preview"
        
        self._con = sqlite3.connect(dbName)
        self._cur = self._con.cursor()
        
        self.resetCard()


    def createTable(self) -> None:

        if self.lang == "ja":
            
            self._cur.execute("""CREATE TABLE IF NOT EXISTS card (
            id integer PRIMARY KEY,
            type text NOT NULL,
            name text NOT NULL,
            nameRuby test NOT NULL,
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
            
        else:
            
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
            properties text,
            new boolean
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
            # print(card['pendEffect'] == self.NULL)
        if card['pendEffect'] == self.NULL:
            card['pendEffect'] = self.NULL
        else:
            card['pendEffect'] = f"\"{self.formatCardString(card['pendEffect'])}\""
            
        if card['linkArrows'] == self.NULL:
            card['linkArrows'] = self.NULL
        else:
            card['linkArrows'] = f"\"{card['linkArrows']}\""
            
        if card['properties'] == self.NULL:
            card['properties'] = self.NULL
        else:
            card['properties'] = f"\"{card['properties']}\""
        
        
        if self.lang == "ja":
            
            try:
                self._cur.execute(f"""INSERT INTO card VALUES 
                        ({card['id']}, 
                        "{card['type']}", 
                        "{self.formatNameString(card['name'])}", 
                        {self.card['nameRuby']}
                        "{card['englishAttribute']}", 
                        "{card['localizedAttribute']}", 
                        "{self.formatCardString(card['effectText'])}", 
                        {card['pendEffect']}, 
                        {card['pendScale']}, 
                        {card['level']}, 
                        {card['rank']}, 
                        {card['linkRating']}, 
                        {card['linkArrows']}, 
                        {card['atk']}, 
                        {card['def']}, 
                        {card['properties']},
                        {card['new']})""")
            
            except sqlite3.OperationalError:
                print(card)
                exit()
                
        else:
            

            try:
                self._cur.execute(f"""INSERT INTO card VALUES 
                                ({card['id']}, 
                                "{card['type']}", 
                                "{self.formatNameString(card['name'])}", 
                                "{card['englishAttribute']}", 
                                "{card['localizedAttribute']}", 
                                "{self.formatCardString(card['effectText'])}", 
                                {card['pendEffect']}, 
                                {card['pendScale']}, 
                                {card['level']}, 
                                {card['rank']}, 
                                {card['linkRating']}, 
                                {card['linkArrows']}, 
                                {card['atk']}, 
                                {card['def']}, 
                                {card['properties']},
                                {card['new']})""")
            
            except sqlite3.OperationalError:
                print(card)
                exit()

        

    def commitChanges(self) -> None:
        """
            Saves changes to the database.        
        """

        self._con.commit()
        self._con.close()

    def parseJSON(self, link):
        """
            Gets all the JSON cards in the specified language directory.
        """
        return os.listdir(link)


    def createCard(self, card, new) -> None:
        """
            Transfers all the JSON object data into python dictionary.
        """
        self.currCard['new'] = new
        
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
        
        if self.lang == "ja":
            
                self.currCard = {
                "id": self.NULL,
                "type": self.NULL,
                "name": self.NULL,
                "nameRuby": self.NULL,
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
                "properties": self.NULL,
                "new": 0
            }
            
        else:
            
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
                "properties": self.NULL,
                "new": 0
            }

    def buildDB(self):
        """
            Goes to each JSON file and adds the cards into the database.
        """

        self.createTable()
        card_list = self.parseJSON(self.JSON_DIR)

        print("Begin building")
        item = 0
        total = len(os.listdir(self.JSON_DIR))
        
        
        
        for jsonFile in card_list:
            
            if jsonFile == "preview":
                
                total += len(os.listdir(self.NEW_DIR))
                new_card_list = self.parseJSON(self.NEW_DIR)
                for newCard in new_card_list:
                    
                    new = json.load(open(f"{self.NEW_DIR}/{newCard}", encoding="utf-8"))
                    self.createCard(new, 1)
                    self.insertCard(self.currCard)
                    item += 1
                    print('\r', str(total - item), end = ' items remaining. ')
                    self.resetCard()
                
            else:
                c = json.load(open(f"./yugioh-card-history/{self.lang}/{jsonFile}", encoding="utf-8"))
                self.createCard(c, 0)
                self.insertCard(self.currCard)
                item += 1
                print('\r', str(total - item), end = ' items remaining. ')
                self.resetCard()

        self.commitChanges()