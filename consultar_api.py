from requests import request
from json import loads


# Removi o token por questões de segurança.
# Os executáveis estão compilados com o token, então o programa irá funcionar normalmente.
token = ''


class Consultar:
    def __init__(self, link):
        self.link = link

    def requisicao(self):
        resposta = request('get', self.link)
        resposta = loads(resposta.text)
        return resposta

    def colocar(self, cabecalho, dados):
        resposta = request('put', self.link, headers=cabecalho, data=dados)
        resposta = loads(resposta.text)
        return resposta


class FormatarSaida:
    def formatar_consulta_cidade(elemento, objeto):
        for row in elemento:
            for k, v in row.items():
                objeto.janela.textEditCidadeId.append(
                    str(k) + ' - ' + str(v))
            objeto.janela.textEditCidadeId.append(' ')

    def formatar_registra_cidade(elemento, objeto):
        for k, v in elemento.items():
            objeto.janela.textEditCidadeId.setText(str(k) + ' - ' + str(v))

    def formatar_consulta_clima(elemento, objeto):
        for k, v in elemento.items():
            if isinstance(v, dict):
                for a, b in v.items():
                    objeto.janela.textEditTempo.append(
                        str(a) + ' - ' + str(b))
            else:
                objeto.janela.textEditTempo.append(str(k) + ' - ' + str(v))


class FuncoesJanela:
    def verificar_cidade_registrada():
        resposta = Consultar(
            'http://apiadvisor.climatempo.com.br/api-manager/'
            'user-token/' + token + '/locales')

        resultado = resposta.requisicao()

        return resultado['locales'][0]

    def consulta_cidade(objeto):
        valor = objeto.janela.lineEditConsultaCidade.text()

        if valor == '' or valor.isspace():
            return None

        else:
            valor = valor.strip()
            valor = valor.title()

            objeto.janela.lineEditConsultaCidade.setText('')
            objeto.janela.textEditCidadeId.setText('')
            objeto.janela.lineEditConsultaCidade.setPlaceholderText(
                'Digite o nome da cidade')

            resposta = Consultar(
                'http://apiadvisor.climatempo.com.br/api/v1/locale/'
                'city?name=' + valor + ''
                '&token=' + token + '')

            resultado = resposta.requisicao()
            FormatarSaida.formatar_consulta_cidade(resultado, objeto)

    def registra_cidade(objeto):
        valor = objeto.janela.lineEditResitraId.text()

        if valor == '' or valor.isspace():
            return None

        else:
            valor = valor.strip()

            objeto.janela.lineEditResitraId.setText('')
            objeto.janela.lineEditResitraId.setPlaceholderText('Digite o id')

            registrar = Consultar(
                'http://apiadvisor.climatempo.com.br/api-manager/'
                'user-token/' + token + '/locales',)

            resposta = registrar.colocar(
                {'Content-Type': 'application/x-www-form-urlencoded'},
                'localeId[]=' + valor + '')

            FormatarSaida.formatar_registra_cidade(resposta, objeto)

    def consulta_clima(objeto):
        id_cidade = FuncoesJanela.verificar_cidade_registrada()

        resposta = Consultar(
            'http://apiadvisor.climatempo.com.br/api/v1/weather/locale/'
            '' + str(id_cidade) + '/current?token=' + token + '')

        resultado = resposta.requisicao()

        objeto.janela.textEditTempo.setText('')

        FormatarSaida.formatar_consulta_clima(resultado, objeto)
