#!/usr/bin/env python

# =============================================================================
# IMPORTS
# =============================================================================

import sys
from PyQt4 import QtCore, QtGui

# =============================================================================
# GLOBALS 
# =============================================================================
BUSY_INDICATOR = './busy.gif'

# =============================================================================
# CLASSES
# =============================================================================
class TreeViewBusyLabel(QtGui.QLabel):

    # =========================================================================
    def __init__(self, tree_view, index):
        super(TreeViewBusyLabel, self).__init__(tree_view)

        self._p_index = QtCore.QPersistentModelIndex(index)

        self._movie = QtGui.QMovie(BUSY_INDICATOR)
        self._movie.setCacheMode(QtGui.QMovie.CacheAll)

        self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.setMovie(self._movie)

        # catch the tree view resizes to reposition the busy indicator
        tree_view.installEventFilter(self)

        # need to update position if header sections are resized 
        tree_view.header().sectionResized.connect(
            lambda i, o, n: self._reposition())

        # reposition when scrolling occurs
        for scrollBar in [tree_view.horizontalScrollBar(),
            tree_view.verticalScrollBar()]:
            scrollBar.valueChanged.connect(lambda v: self._reposition())

    # =========================================================================
    def eventFilter(self, object, event):

        # parent() is the tree view
        if object == self.parent():
            if event.type() in [QtCore.QEvent.Resize, QtCore.QEvent.Show]:  
                self._reposition()
            
        return False

    # =========================================================================
    def hide(self):
        self._movie.stop()
        super(TreeViewBusyLabel, self).hide()

    # =========================================================================
    def show(self):
        self._reposition()
        self._movie.start()
        super(TreeViewBusyLabel, self).show()

    # =========================================================================
    def _reposition(self):

        if not self._p_index.isValid():
            # TODO: probably want to handle this better (deleteLater maybe?)
            self.hide()
            return

        tree_view = self.parent()

        index = tree_view.model().index(self._p_index.row(), 
            self._p_index.column(), self._p_index.parent())

        rect = tree_view.visualRect(index)

        # TODO: there's probably a better way to account for the header
        rect.translate(0, tree_view.header().height())
        self.setGeometry(rect)

# =============================================================================
class TestTreeView(QtGui.QTreeView):

    # =========================================================================
    def __init__(self, parent=None):
        super(TestTreeView, self).__init__(parent=parent)

        model = QtGui.QStandardItemModel()
        for row in range(0, 20):
            row_items = []
            for col in range(0, 3):
                row_items.append(QtGui.QStandardItem(
                    "row: " + str(row) + ", col: " + str(col)))
            model.appendRow(row_items)
                
        self.setModel(model)

        self.clicked.connect(self._make_busy)

    # =========================================================================
    def _make_busy(self, index):

        busyLabel = TreeViewBusyLabel(self, index)
        busyLabel.show()

# =============================================================================
class TestWindow(QtGui.QMainWindow):

    # =========================================================================
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent=parent)
        self.setCentralWidget(TestTreeView())

# =============================================================================
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    win = TestWindow()
    win.show()
    sys.exit(app.exec_())

