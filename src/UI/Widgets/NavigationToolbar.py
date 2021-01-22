from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT


class NavigationToolbar(NavigationToolbar2QT):
    toolitems = [
        t
        for t in NavigationToolbar2QT.toolitems
        if t[0] in ("Home", "Pan", "Back", "Forward", "Zoom")
    ]

    def __init__(self, *args, **kwargs):
        super(NavigationToolbar, self).__init__(*args, **kwargs)

    def EnableMoving(self):
        self._actions["home"].setEnabled(True)
        self._actions["back"].setEnabled(True)
        self._actions["forward"].setEnabled(True)
        self._actions["pan"].setEnabled(True)
        self._actions["zoom"].setEnabled(True)

    def DisableMoving(self):
        self._actions["home"].setEnabled(False)
        self._actions["back"].setEnabled(False)
        self._actions["zoom"].setEnabled(False)
        self._actions["pan"].setEnabled(False)
        self._actions["zoom"].setEnabled(False)
