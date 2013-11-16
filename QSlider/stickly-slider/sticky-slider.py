#!/usr/bin/env python

# =============================================================================
# IMPORTS
# =============================================================================

import sys
from PyQt4 import QtCore, QtGui

# =============================================================================
# CLASSES
# =============================================================================
class StickySlider(QtGui.QSlider):

    # =========================================================================
    def __init__(self, parent=None, sticky_value=None, sticky_range=10):
        super(StickySlider, self).__init__(parent)

        self.setOrientation(QtCore.Qt.Horizontal)

        if sticky_value is None:
            sticky_value = (self.maximum() - self.minimum()) / 2.0;

        self._sticky_value = sticky_value
        self._sticky_region = range(int(sticky_value - (sticky_range / 2.0)),
                                    int(sticky_value + (sticky_range / 2.0)))
        self.valueChanged.connect(self._process_value_change)

    # =========================================================================
    def _process_value_change(self, value):

        if value in self._sticky_region:
            self.blockSignals(True)
            self.setValue(self._sticky_value)
            self.blockSignals(False)

# =============================================================================
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    win = StickySlider(None, 50, sticky_range=20)
    win.show()
    sys.exit(app.exec_())

