import cherrypy

from common import *


class ControleProdutos(object):
    @cherrypy.expose
    def index(self, filtro=""):
        # Adicionar o header de encoding UTF-8
        cherrypy.response.headers['Content-Type'] = 'text/html;charset=utf-8'

        # conectando ao banco de dados
        conn = get_db_conn()

        cursor = conn.cursor()

        # extraindo os dados do sku da tabela
        cursor.execute(f"SELECT p.sku, p.nome, p.descricao, COALESCE(SUM(e.qtd), 0) AS total_qtd " +
                       f"FROM produtos p " +
                       f"LEFT JOIN estoque e ON p.id = e.id_produto " +
                       f"WHERE p.sku LIKE '%{filtro}%' OR p.nome LIKE '%{filtro}%'"
                       f"GROUP BY p.sku, p.nome, p.descricao")
        data = cursor.fetchall()

        # fechando a conexão
        conn.close()

        # renderizando a página html com os dados
        with open(relative_path()+"/pages/controle.html", "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace("{{produtos}}", format_table(data))
        html = html.replace("{{filtro}}", filtro)
        html = html.replace("{{hora}}", get_current_time())
        return html


def format_table(data):
    rows = ""
    for i, (sku, nome, descricao, qtd) in enumerate(data):
        rows += "<tr>"
        rows += f"<td>{sku}</td>"
        rows += f"<td>{nome}</td>"
        rows += f"<td>{descricao}</td>"
        rows += f"<td>{qtd}</td>"
        rows += f'<td>'
        rows += f'<button type="button" class="btn btn-outline-primary py-0" onclick="verEstoque(\'{sku}\')"'
        rows += f'data-bs-toggle="tooltip" data-bs-placement="top" title="Ajustar estoque">'
        rows += f'<span class="bi bi-box-seam"></span></button>'
        rows += f'</td>'
        rows += "</tr>"
    return rows
