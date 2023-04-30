import cherrypy

from common import *
from estoque import Estoque
from cadastro import Cadastro
from lista import ListaProdutos


class Index(object):
    @cherrypy.expose
    def index(self):
        # Adicionar o header de encoding UTF-8
        cherrypy.response.headers['Content-Type'] = 'text/html;charset=utf-8'

        # renderizando a página html com os dados
        with open(relative_path()+"/pages/index.html", "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace("{{hora}}", get_current_time())
        return html


if __name__ == '__main__':
    cherrypy.tree.mount(Index(), "/")
    cherrypy.tree.mount(Cadastro(), "/cadastro")
    cherrypy.tree.mount(ListaProdutos(), "/lista")
    cherrypy.tree.mount(Estoque(), "/estoque")
    cherrypy.engine.start()
    cherrypy.engine.block()
