import sqlite3

def main():
    conn = sqlite3.connect("banco_de_dados\prova\produtos.db")
    cursor = conn.cursor()

    while True:
        opcao = int(input("1-cria tabela\n2-adiciona produto\n3- atualiza produtos\n4-remove produto\n5-busca produto\n6-lista produtos\n7-calcula valor total\n8-venda\n\nEscolha uma: "))
        match opcao:
            case 1:
                cria_tabela(cursor, conn)
            case 2:
                nome = input("Nome: ")
                quantidade = int(input("quantidade: "))
                preco = float(input("preco: "))
                adiciona_produto(cursor, conn, nome, quantidade, preco)
            case 3:
                escolha = input("Voce quer atualizar a quantidade ou o valor? (quantidade / valor)")
                if escolha == "quantidade":
                    id = int(input("id: "))
                    quantidade = int(input("quantidade: "))
                    atualiza_quantidade_produto(cursor, conn, id, quantidade)
                elif escolha == "valor":
                    id = int(input("id: "))
                    valor = float(input("valor"))
                    atualiza_valor_produto(cursor, conn, id, valor)
            case 4:
                id = int(input("id: "))
                remove_produto(cursor, conn, id)
            case 5:
                escolha = input("Voce quer buscar pelo id ou pelo nome do produto? (id / nome)")
                if escolha == "id":
                    id = int(input("id: "))
                    busca_produto_id(cursor, id)
                elif escolha == "nome":
                    nome = input("nome: ")
                    busca_produto_nome(cursor, nome)
            case 6: 
                lista_produtos(cursor)
            case 7:
                nome = input("nome: ")
                calcula_valor_total(cursor, nome)
            case 8:
                id = int(input("id: "))
                busca_produto_id(cursor, id)
                quantidade_venda = int(input("quantidade da venda: "))
                venda(cursor, conn, id, quantidade_venda)

        if deseja_continuar():
            conn.close()
            break
        
def deseja_continuar():
    continuar = input("\ndeseja continuar? (sim / nao)")
    return False if continuar == "sim" else True     

def cria_tabela(cursor, conn):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            quantidade INTEGER,
            preco DECIMAL
            )
    """)
    conn.commit()

def adiciona_produto(cursor, conn, nome, quantidade, preco):
    if quantidade > 0 and preco > 0:
        cursor.execute("""
            INSERT INTO Produtos(nome, quantidade, preco) VALUES (?,?,?)
        """, (nome, quantidade, preco))
        conn.commit()

def lista_produtos(cursor):
    cursor.execute("""
        SELECT * FROM Produtos
    """)
    produtos = cursor.fetchall()
    for produto in produtos:
        print(f"id: {produto[0]} | nome: {produto[1]} | quantidade: {produto[2]} | preco: {produto[3]}")

def atualiza_quantidade_produto(cursor, conn, id, quantidade):
    cursor.execute("""
        UPDATE Produtos SET quantidade = ? WHERE id = ?
    """, (quantidade, id))
    conn.commit()

def atualiza_valor_produto(cursor, conn, id, valor):
    cursor.execute("""
        UPDATE Produtos SET valor = ? WHERE id = ?
    """, (valor, id))
    conn.commit()

def remove_produto(cursor, conn, id):
    cursor.execute(f"""
        DELETE FROM Produtos WHERE id = {id}
    """)
    conn.commit()

def busca_produto_id(cursor, id):
    cursor.execute(f"""
        SELECT * FROM Produtos WHERE id = {id}
    """)
    produtos = cursor.fetchall()
    for produto in produtos:
        print(f"nome: {produto[1]} | quantidade: {produto[2]} | preco: {produto[3]}")

def busca_produto_nome(cursor, nome):
    cursor.execute(f"""
        SELECT * FROM Produtos WHERE nome = '{nome}'
    """)
    produtos = cursor.fetchall()
    for produto in produtos:
        print(f"nome: {produto[1]} | quantidade: {produto[2]} | preco: {produto[3]}")

def calcula_valor_total(cursor, nome):
    cursor.execute(f"""
        SELECT * FROM Produtos WHERE nome = '{nome}'
    """)
    produto = cursor.fetchone()
    valor_total = produto[2] * produto[3]
    print(f"O valor total do {produto[1]} é de R$ {valor_total}")

def venda(cursor, conn,id , quantidade_venda):
    cursor.execute(f"""
        SELECT * FROM Produtos WHERE id = {id}
    """)
    produto = cursor.fetchone()
    estoque_atualizado = produto[2] - quantidade_venda

    cursor.execute("""
        UPDATE Produtos SET quantidade =  ? WHERE id = ?
    """, (estoque_atualizado, id))
    conn.commit()
    
    busca_produto_id(cursor, id)

if __name__ == "__main__":
    main()
