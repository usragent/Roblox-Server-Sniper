from time import time
from random import randint 
from requests import Session as session
from webbrowser import open as openUrl


class RobloxLauncher:
    def __init__(self, cookie):
        self.session = session()
        self.session.cookies[".ROBLOSECURITY"] = cookie

    def returnAuth(self):
        return self.session.post(url="https://auth.roblox.com/v1/authentication-ticket/", headers={
            "Referer": "https://www.roblox.com",
            "X-CSRF-Token": self.session.post(url="https://auth.roblox.com/v1/authentication-ticket/").headers["X-CSRF-Token"],
        }).headers["RBX-Authentication-Ticket"]

    def launchClient(self, ticket, placeId, jobId):
        openUrl(f"roblox-player:1+launchmode:play+gameinfo:{ticket}+launchtime:{int(time()*1000)}+placelauncherurl:https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DRequestGameJob%26browserTrackerId%3D{randint(10000000000, 99999999999)}%26placeId%3D{placeId}%26gameId%3D{jobId}%26isPlayTogetherGame%3Dfalse+browsertrackerid:{randint(10000000000, 99999999999)}+robloxLocale:en_us+gameLocale:en_us")
