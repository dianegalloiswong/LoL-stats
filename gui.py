import sys
from PyQt4 import QtCore
from PyQt4 import QtGui

import my_lda_model
import run_gensim


class MissingConstructorArgumentException(Exception):
    def __init__(self, obj):
        self.message = 'Missing argument in constructor of {}'.format(obj.__class__.__name__)


class InvalidValueException(Exception):
    def __init__(self, param):
        self.name = param.name
        self.message = "Invalid {}.".format(param.name)
        self.param = param


class Param:
    def __init__(self, parent=None, name=None, init=None, maxlength=None, maxwidth=None):
        if parent is None or name is None:
            raise MissingConstructorArgumentException(self)

        self.name = name

        self.lbl = QtGui.QLabel(parent)
        self.lbl.setText(name)

        self.qle = QtGui.QLineEdit(parent)
        if init is not None:
            self.qle.setText(str(init))
        if maxlength is not None:
            self.qle.setMaxLength(maxlength)
        if maxwidth is not None:
            self.qle.setMaximumWidth(maxwidth)
        self.qle.setAlignment(QtCore.Qt.AlignCenter)

    def setToolTip(self, s):
        self.lbl.setToolTip(s)
        self.qle.setToolTip(s)



    def get_value(self):
        return self.qle.text()


class IntParam(Param):
    def __init__(self, lbound=None, ubound=None, **kwargs):
        Param.__init__(self, **kwargs)

        self.lbound = lbound
        self.ubound = ubound

        if lbound is not None and ubound is not None:
            tooltip = 'between {} and {}'.format(lbound, ubound)
            self.setToolTip(tooltip)

    def get_value(self):
        try:
            s = Param.get_value(self)
            n = int(s)
            if (self.lbound is not None and n < self.lbound) or (self.ubound is not None and n > self.ubound):
                raise InvalidValueException(self)
            return n
        except ValueError:
            raise InvalidValueException(self)


class ParamsWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(ParamsWidget, self).__init__(parent)
        self.grid = QtGui.QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)
        self.params = []
        self.nextrow = 0

    dflt_maxwidth = 60

    def addIntParam(self, name, init=None, lbound=None, ubound=None,
                 maxlength=None, maxwidth=None):
        if maxwidth is None:
            maxwidth = ParamsWidget.dflt_maxwidth
        param = IntParam(parent=self, name=name, init=init, lbound=lbound, ubound=ubound,
                         maxlength=maxlength, maxwidth=maxwidth)
        self.grid.addWidget(param.lbl, *(self.nextrow, 0))
        self.grid.addWidget(param.qle, *(self.nextrow, 1))
        self.nextrow += 1
        self.params.append(param)
        return param # useful?

    def get_values(self):
        d = dict()
        for param in self.params:
            d[param.name] = param.get_value()
        return d


class LDAWidget(QtGui.QWidget):
    def __init__(self):
        super(LDAWidget, self).__init__()

        self.button = QtGui.QPushButton('Run LDA', self)
        self.button.clicked.connect(self.run_lda)

        self.params = ParamsWidget(self)
        self.number_of_topics_str = 'number of topics'
        self.params.addIntParam(self.number_of_topics_str, init=10, maxlength=2, lbound=1, ubound=99)
        self.number_of_iterations_str = 'number of iterations'
        self.params.addIntParam(self.number_of_iterations_str, init=10, maxlength=6, lbound=10, ubound=999999)
        for param in self.params.params: # should be factorised
            param.qle.returnPressed.connect(self.button.click)

        self.qte = QtGui.QTextEdit(self)
        self.qte.setLineWrapMode(0)


        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.params)
        vbox.addWidget(self.button)

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        v2 = QtGui.QVBoxLayout()
        v2.addLayout(hbox)
        v2.addWidget(self.qte)

        self.setLayout(v2)

        self.move(300, 150)
        self.setWindowTitle('LDA on masters')
        self.show()

    def run_lda(self):
        try:
            values = self.params.get_values()
        except InvalidValueException as exn:
            self.label.setText(exn.message)
            exn.param.qle.selectAll()
            return
        s = 'Running LDA on masters   {}'.format(values)
        print(s)

        corpus = run_gensim.make_corpus_master()
        lda = my_lda_model.MyLdaModel(corpus, iterations=values[self.number_of_iterations_str], num_topics=values[self.number_of_topics_str])
        lda.display(display_func=self.qte.append)
        self.qte.append('\n\n')

        width = self.qte.document().idealWidth() + 30
        #self.qte.sizeHint(QtCore.QSize(width,0))
        self.qte.setFixedWidth(width)
        # self.qte.setBaseSize(int(width), self.qte.height())
        # self.qte.resize(int(width), self.qte.height())
        # self.qte.updateGeometry()


def main():

    app = QtGui.QApplication(sys.argv)
    ex = LDAWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()