import cherrypy

from common import *


class Estoque(object):
    @cherrypy.expose
    def index(self, sku=None):
        # Adicionar o header de encoding UTF-8
        cherrypy.response.headers['Content-Type'] = 'text/html;charset=utf-8'

        # conectando ao banco de dados
        conn = get_db_conn()

        cursor = conn.cursor()
        # extraindo os dados do sku da tabela
        cursor.execute(f"SELECT p.sku, p.nome, p.descricao, e.valor, e.qtd, e.data " +
                       f"FROM produtos p " +
                       f"LEFT JOIN estoque e ON p.id = e.id_produto " +
                       f"WHERE sku = '{sku}'" +
                       f"ORDER BY e.data DESC")
        data = cursor.fetchall()

        # fechando a conexão
        conn.close()

        nome = None
        descricao = None
        if data and len(data) > 0:
            nome = data[0][1]
            descricao = data[0][2]

        # renderizando a página html com os dados
        with open(relative_path()+"/pages/estoque.html", "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace("{{sku}}", sku)
        html = html.replace("{{nome}}", nome)
        html = html.replace("{{descricao}}", descricao)
        html = html.replace("{{qtd}}", get_qtd(data))
        html = html.replace("{{lucro}}", get_lucro(data))
        html = html.replace("{{estoque}}", format_table(data))
        html = html.replace("{{hora}}", get_current_time())
        return html

    @cherrypy.expose
    def adicionar(self, sku, valor, qtd):
        conn = get_db_conn()

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO estoque (id_produto, valor, qtd) " +
                       f"SELECT id, -{valor}, {qtd} " +
                       f"FROM produtos " +
                       f"WHERE sku = '{sku}'")

        conn.commit()
        cursor.close()
        conn.close()
        raise cherrypy.HTTPRedirect(f"/estoque?sku={sku}")

    @cherrypy.expose
    def remover(self, sku, valor, qtd):
        conn = get_db_conn()

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO estoque (id_produto, valor, qtd) " +
                       f"SELECT id, {valor}, -{qtd} " +
                       f"FROM produtos " +
                       f"WHERE sku = '{sku}'")

        conn.commit()
        cursor.close()
        conn.close()
        raise cherrypy.HTTPRedirect(f"/estoque?sku={sku}")


def format_table(data):
    rows = ""
    for i, (_, _, _, valor, qtd, data) in enumerate(data):
        if valor:
            rows += "<tr>"
            if valor < 0:
                rows += "<td>COMPRA</td>"
                rows += f'<td class="text-end">R$ {abs(valor)}</td>'
            else:
                rows += "<td>VENDA</td>"
                rows += f'<td class="text-end">R$ {valor}</td>'
            rows += f'<td class="text-end">{abs(qtd)}</td>'
            rows += f'<td class="text-end">R$ {abs(valor/qtd):.2f}</td>'
            rows += f'<td class="text-center">{data}</td>'
            rows += "</tr>"
    return rows

def get_qtd(data):
    qtd = 0
    if data and len(data) > 0 and data[0][4]:
        qtd = sum(c[4] for c in data)
    if qtd < 0:
        return f'<span style="color:red">{qtd}</span>'
    else:
        return f"{qtd}"

def get_lucro(data):
    lucro = 0
    if data and len(data) > 0 and data[0][3]:
        lucro = sum(c[3] for c in data)
    if lucro < 0:
        return f'<span style="color:red">-R$ {abs(lucro)}</span>'
    else:
        return f"R$ {lucro}"
