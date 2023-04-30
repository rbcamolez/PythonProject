import cherrypy

from common import *


class Cadastro(object):
    @cherrypy.expose
    def index(self, sucesso=False):
        # Adicionar o header de encoding UTF-8
        cherrypy.response.headers['Content-Type'] = 'text/html;charset=utf-8'

        # renderizando a página html com os dados
        with open(relative_path()+"/pages/cadastro.html", "r", encoding="utf-8") as f:
            html = f.read()
            if sucesso:
                html = html.replace(
                    "{{messagem_sucesso}}", f'<script>confirm("SKU {sucesso} cadastrado com secesso!")</script>')
            else:
                html = html.replace("{{messagem_sucesso}}", "")
            html = html.replace(
                "{{hora}}", get_current_time())
            return html

    @cherrypy.expose
    def cadastrar(self, sku, nome, descricao):
        conn = get_db_conn()

        cursor = conn.cursor()
        query = "INSERT INTO produtos (sku, nome, descricao) VALUES (%s, %s, %s)"
        values = (sku, nome, descricao)
        cursor.execute(query, values)

        conn.commit()
        cursor.close()
        conn.close()
        raise cherrypy.HTTPRedirect(f"/cadastro?sucesso={sku}")
