import pycep_correios


class ListCep(object):
    def loadCep(self, cep):
        endereco = pycep_correios.consultar_cep(cep)
        return endereco
