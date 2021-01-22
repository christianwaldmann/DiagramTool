from src.Logic.DiagramCreator import DiagramCreator
from src.UI.DiagramCreatorUI import DiagramCreatorUI

import sys


class Application:
    def __init__(self):
        self.creator = DiagramCreator()
        self.interface = DiagramCreatorUI(self.creator)

    def Run(self):
        return sys.exit(self.interface.Run())
