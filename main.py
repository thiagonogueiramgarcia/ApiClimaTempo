from PyQt5 import uic, QtWidgets

from consultar_api import Consultar, FuncoesJanela


class ConsultaApiJanela:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.janela = uic.loadUi('./Janelas/formClimaTempoApi.ui')

        self.janela.pushButtonConsultaCidade.clicked.connect(
            lambda: FuncoesJanela.consulta_cidade(tetas))

        self.janela.pushButtonRegistraId.clicked.connect(
            lambda: FuncoesJanela.registra_cidade(tetas))

        self.janela.pushButtonConsulaTempo.clicked.connect(
            lambda: FuncoesJanela.consulta_clima(tetas))

    def executar_janela(self):
        self.janela.show()
        self.app.exec()


tetas = ConsultaApiJanela()
tetas.executar_janela()
