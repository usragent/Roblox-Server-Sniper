import requests, re, json, os, time, threading
from packages.launcher import RobloxLauncher
from packages.scraper import WebScraper

class RobloxSniper:
    def __init__(self, placeId, cookie, target):
        self.placeId = placeId
        self.target = target
        self.cookie = cookie
        self.cursor = ""
        self.playerCount = 0
        self.foundMatch = False
        self.targetToken = self.selfUserToken()
        self.playerTokens = []
        self.separators = ['|', '/', '-', '\\']
        self.sepIdx = 0
        self.titleThread = threading.Thread(target=self.animateTitle, daemon=True)
        self.titleThread.start()

    def animateTitle(self):
        while True:
            self.sepIdx = (self.sepIdx + 1) % len(self.separators)
            time.sleep(1)

    def calculateTime(self, tokens):
        x = 1500
        y = int(WebScraper(f"https://www.roblox.com/games/{self.placeId}").returnPlayers()) - tokens
        z = 4

        os.system("title " + f"ETA: {str(round(y / x * z, 2))} seconds    ^{self.separators[self.sepIdx]}^    Processed Tokens: {tokens}    ^{self.separators[self.sepIdx]}^    {self.target} in {self.placeId}...")

    def joinServer(self, serverId):
        choice = input("[Y/N] - Would you like to join the server > ").lower()
        if choice == "y":
            launcher = RobloxLauncher(self.cookie)
            launcher.launchClient(launcher.returnAuth(), self.placeId, serverId)

    def selfUserToken(self):
        url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={self.target},0&size=150x150&format=Png&isCircular=false"

        response = requests.get(url, headers={'accept': 'application/json', 'Content-Type': 'application/json'}).json()

        image = response['data'][0]['imageUrl']
        match = re.search(r'-([A-F0-9]+)-Png', image)
        if match:
            return match.group(1)
        else:
            print("Pattern not found in URL:", image)
            return None
        
    def sendTokens(self, tokens):
        url = "https://thumbnails.roblox.com/v1/batch"
        response = requests.post(url, headers={'accept': 'application/json', 'Content-Type': 'application/json'}, json=tokens).json()

        print(f"[*] Validating {len(self.playerTokens)} playerTokens")

        if not self.foundMatch: 
            for x in response['data']:
                image = x['imageUrl']
                self.playerCount += 1
                match = re.search(r'-([A-F0-9]+)-Png', image)
                if match:
                    extract = match.group(1)
                    if extract == self.targetToken:
                        self.foundMatch = True
                        print("Match found! Server ID:", x['requestId'])
                        self.joinServer(x['requestId'])

    def appendPlayers(self):
        if self.targetToken is None:
            return 

        url = f"https://games.roblox.com/v1/games/{self.placeId}/servers/Public?limit=100"
        nextPageCursor = None

        while not self.foundMatch and url:
            if nextPageCursor:
                url = f"https://games.roblox.com/v1/games/{self.placeId}/servers/Public?limit=100&cursor={nextPageCursor}"

            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                for server in data['data']:
                    if 'playerTokens' in server:
                        for playerToken in server['playerTokens']:
                            playerData = {
                                'token': playerToken,
                                'type': 'AvatarHeadshot',
                                'size': '150x150',
                                'requestId': server['id']
                            }
                            self.playerCount += 1
                            self.playerTokens.append(playerData)

                            if len(self.playerTokens) == 100 and not self.foundMatch:
                                print(f"[+] Appending -> {len(self.playerTokens)}")
                                self.calculateTime(self.playerCount)
                                self.sendTokens(self.playerTokens)
                                self.playerTokens = []

                nextPageCursor = data.get('nextPageCursor', None)
                if nextPageCursor and not self.foundMatch:
                    os.system('cls||clear')
                    print(f"[*] Checking Next Page: {nextPageCursor}")
                elif not self.foundMatch:
                    url = None
                    print("[!] Couldnt find target")

            else:
                print("[-] Error with request")
        
        if len(self.playerTokens) > 0 and not self.foundMatch:
            print(f"[*] Appending leftover -> {len(self.playerTokens)}")
            self.sendTokens(self.playerTokens)


if __name__ == "__main__":
    Sniper = RobloxSniper(input("[*] Place ID: "), json.load(open('data/config.json'))['Credentials']['Cookie'], json.load(open('data/config.json'))['Credentials']['Target']).appendPlayers()
