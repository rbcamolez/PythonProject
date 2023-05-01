import cherrypy

from common import *


class RelatorioProdutos(object):
    @cherrypy.expose
    def index(self, filtro=""):
        # Adicionar o header de encoding UTF-8
        cherrypy.response.headers['Content-Type'] = 'text/html;charset=utf-8'

        # conectando ao banco de dados
        conn = get_db_conn()

        cursor = conn.cursor()

        # extraindo os dados filtrados da tabela
        cursor.execute("SELECT p.sku, p.nome, p.preco_venda AS preco, " +
                       "SUM(CASE WHEN e.qtd < 0 THEN -e.qtd ELSE 0 END) AS compras, " +
                       "SUM(CASE WHEN e.valor < 0 THEN -e.valor ELSE 0 END) AS total_compra, " +
                       "SUM(CASE WHEN e.qtd > 0 THEN e.qtd ELSE 0 END) AS vendas, " +
                       "SUM(CASE WHEN e.valor > 0 THEN e.valor ELSE 0 END) AS total_venda, " +
                       "COALESCE(SUM(e.qtd), 0) AS qtd, " +
                       "COALESCE(SUM(e.valor), 0) AS lucro " +
                       "FROM produtos p " +
                       "LEFT JOIN estoque e ON p.id = e.id_produto " +
                       "GROUP BY p.sku, p.nome")
        data = cursor.fetchall()

        # fechando a conexão
        conn.close()

        # renderizando a página html com os dados
        with open(relative_path()+"/pages/relatorio.html", "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace("{{produtos}}", format_table(data))
        html = html.replace("{{filtro}}", filtro)
        html = html.replace("{{hora}}", get_current_time())
        return html


def format_table(data):
    rows = ""
    for i, (sku, nome, preco,
            qtd_compras, total_compra,
            qtd_vendas, total_venda,
            qtd, lucro) in enumerate(data):
        rows += "<tr>"
        rows += f"<td>{sku}</td>"
        rows += f"<td>{nome}</td>"
        rows += f"<td class='text-end'>{'R$ '+str(preco) if preco else ''}</td>"
        rows += f"<td>{qtd_compras}</td>"
        media_compra = total_compra/qtd_compras if qtd_compras > 0 else 0
        rows += f"<td class='text-end'>R$ {media_compra:.2f}</td>"
        rows += f"<td class='text-end'>R$ {total_compra}</td>"
        rows += f"<td>{qtd_vendas}</td>"
        media_venda = total_venda/qtd_vendas if qtd_vendas > 0 else 0
        rows += f"<td class='text-end'>R$ {media_venda:.2f}</td>"
        rows += f"<td class='text-end'>R$ {total_venda}</td>"
        rows += f"<td>{qtd}</td>"
        rows += f"<td class='text-end'>"
        if lucro < 0:
            rows += f'<span style="color:red">-R$ {abs(lucro)}</span>'
        else:
            rows += f"R$ {lucro}"
        rows += "</td>"
        rows += f'<td>'
        rows += f'<button type="button" class="btn btn-outline-primary py-0" onclick="verEstoque(\'{sku}\')"'
        rows += f'data-bs-toggle="tooltip" data-bs-placement="top" title="Ajustar estoque">'
        rows += f'<span class="bi bi-box-seam"></span></button>'
        rows += f'</td>'
        rows += "</tr>"
    return rows
