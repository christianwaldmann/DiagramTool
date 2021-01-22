from src.Core.Application import Application
from src.Core.Log import Log


def main():
    Log.Init()
    app = Application()
    app.Run()
