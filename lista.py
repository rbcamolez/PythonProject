import cherrypy

from common import *


class ListaProdutos(object):
    @cherrypy.expose
    def index(self):
        # Adicionar o header de encoding UTF-8
        cherrypy.response.headers['Content-Type'] = 'text/html;charset=utf-8'

        # conectando ao banco de dados
        conn = get_db_conn()
        cursor = conn.cursor()

        # extraindo os dados da tabela
        cursor.execute("SELECT sku, nome, descricao FROM produtos")
        data = cursor.fetchall()

        # fechando a conexão
        conn.close()

        # renderizando a página html com os dados
        with open(relative_path()+"/pages/lista.html", "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace("{{produtos}}", format_table(data))
        html = html.replace("{{hora}}", get_current_time())
        return html

    @cherrypy.expose
    def filtrar(self, filtro):
        # conectando ao banco de dados
        conn = get_db_conn()

        cursor = conn.cursor()

        # extraindo os dados filtrados da tabela
        cursor.execute(
            "SELECT sku, nome, descricao FROM produtos WHERE sku LIKE '%{0}%' OR nome LIKE '%{0}%'".format(filtro))
        data = cursor.fetchall()

        # fechando a conexão
        conn.close()

        # renderizando a página html com os dados
        with open(relative_path()+"/pages/lista.html", "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace("{{produtos}}", format_table(data))
        html = html.replace("{{hora}}", get_current_time())
        return html

    @cherrypy.expose
    def excluir(self, sku):
        # conectando ao banco de dados
        conn = get_db_conn()

        cursor = conn.cursor()

        # deletando o produto com o SKU especificado
        cursor.execute("DELETE FROM produtos WHERE sku=?", (sku,))
        conn.commit()

        # fechando a conexão
        conn.close()

        # redirecionando para a página principal
        raise cherrypy.HTTPRedirect("/lista")

    @cherrypy.expose
    def atualizar(self, sku, nome, descricao):
        # conectando ao banco de dados
        conn = get_db_conn()

        cursor = conn.cursor()

        # atualizando o produto com o SKU especificado
        cursor.execute(
            "UPDATE produtos SET nome=?, descricao=? WHERE sku=?", (nome, descricao, sku))
        conn.commit()

        # fechando a conexão
        conn.close()

        # redirecionando para a página principal
        raise cherrypy.HTTPRedirect("/lista")


def format_table(data):
    rows = ""
    for i, (sku, nome, descricao) in enumerate(data):
        rows += "<tr>"
        rows += f"<td>{sku}</td>"
        rows += f"<td><input type='text' name='nome' id='nome_{i}' value='{nome}'></td>"
        rows += f"<td><input type='text' name='descricao' id='descricao_{i}' value='{descricao}'></td>"
        rows += f'<td>'
        rows += f'<button type="button" class="btn btn-outline-primary py-0" onclick="verEstoque(\'{sku}\')"'
        rows += f'data-bs-toggle="tooltip" data-bs-placement="top" title="Ver estoque">'
        rows += f'<span class="bi bi-box-seam"></span></button>'
        rows += f'<button type="button" class="btn btn-outline-success py-0" onclick="atualizarProduto(\'{sku}\', document.getElementById(\'nome_{i}\').value, document.getElementById(\'descricao_{i}\').value)" '
        rows += f'data-bs-toggle="tooltip" data-bs-placement="top" title="Atualizar produto">'
        rows += f'<span class="bi bi-check-lg"></span></button>'
        rows += f'<button type="button" class="btn btn-outline-danger py-0" onclick="deletarProduto(\'{sku}\')"'
        rows += f'data-bs-toggle="tooltip" data-bs-placement="top" title="Excluir produto">'
        rows += f'<span class="bi bi-trash"></span></button>'
        rows += f'</td>'
        rows += "</tr>"
    return rows
