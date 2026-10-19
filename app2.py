import streamlit as st
import sqlite3
import pandas as pd

def conectar():
    return sqlite3.connect('manutencao.db')

# ─── CLIENTES ────────────────────────────────────────────────────────────────
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clientes")
    dados = cursor.fetchall()
    conn.close()
    return dados

def adicionar_cliente(nome, pessoa, cpf_cnpj, telefone, email, endereco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Clientes (nome, pessoa, cpf_cnpj, telefone, email, endereco)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, pessoa, cpf_cnpj, telefone, email, endereco))
    conn.commit()
    conn.close()

def excluir_cliente(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# ─── ESTOQUE ────────────────────────────────────────────────────────────────
def listar_estoque():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Estoque")
    dados = cursor.fetchall()
    conn.close()
    return dados

def adicionar_estoque(nome, validade, preco, quantidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Estoque (nome, validade, preco, quantidade)
        VALUES (?, ?, ?, ?)
    """, (nome, validade, preco, quantidade))
    conn.commit()
    conn.close()

def excluir_estoque(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Estoque WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# ─── SERVIÇOS ────────────────────────────────────────────────────────────────
def listar_servicos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id,
            nome,
            tempo_medio,
            preco
        FROM Servicos
        """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def adicionar_servico(nome, tempo_medio, preco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Servicos (nome, tempo_medio, preco)
        VALUES (?, ?, ?)
    """, (nome, tempo_medio, preco))
    conn.commit()
    conn.close()

def excluir_servico(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Servicos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# ─── TRANSAÇÕES ────────────────────────────────────────────────────────────────
def listar_transacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            t.id,
            c.nome AS cliente,
            t.data_hora,
            t.valor
        FROM Transacoes t
        JOIN Clientes c ON t.id_cliente = c.id
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def adicionar_transacao(id_cliente, id_servico, data_hora, valor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Transacoes (id_cliente, id_servico, data_hora, valor)
        VALUES (?, ?, ?, ?)
    """, (id_cliente, id_servico, data_hora, valor))
    conn.commit()
    conn.close()

def excluir_transacao(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Transacoes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# ─── TRANSAÇÕES ────────────────────────────────────────────────────────────────
def listar_agendamentos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            t.id,
            c.nome,
            s.nome,
            t.data_hora,
            t.observacao,
            t.status
        FROM Agendamentos t
        JOIN Clientes c ON t.id_cliente = c.id
        JOIN Servicos s ON t.id_servico = s.id
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def adicionar_agendamento(id_cliente, id_servico, data_hora, status, observacao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Agendamentos (id_cliente, id_servico, data_hora, status, observacao)
        VALUES (?, ?, ?, ?, ?)
    """, (id_cliente, id_servico, data_hora, status, observacao))
    conn.commit()
    conn.close()

def excluir_agendamento(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Agendamentos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# ─── INTERFACE ────────────────────────────────────────────────────────────────

st.title('Sistema Galvão')
st.sidebar.title('Menu')
pagina = st.sidebar.selectbox('Banco de dados', ['Clientes', 'Estoque', 'Serviços', 'Agendamentos', 'Transações'])


# CLIENTE
if pagina == 'Clientes':
    st.header('Clientes')

    # Listar
    clientes = listar_clientes()
    if clientes:
        st.subheader('Clientes cadastrados')
        for c in clientes:
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{c[1]}** | {c[2]} | {c[3]} | {c[4]}")
            if col2.button('Excluir', key=f'del_{c[0]}'):
                excluir_cliente(c[0])
                st.rerun()
    else:
        st.info('Nenhum cliente cadastrado.')

    # Adicionar
    st.subheader('Adicionar cliente')
    with st.form('form_cliente'):
        nome = st.text_input('Nome')
        pessoa = st.selectbox('Tipo', ['Física', 'Jurídica'])
        cpf_cnpj = st.text_input('CPF / CNPJ')
        telefone = st.text_input('Telefone')
        email = st.text_input('Email')
        endereco = st.text_input('Endereço')
        salvar = st.form_submit_button('Salvar')

    if salvar:
        if nome and cpf_cnpj:
            adicionar_cliente(nome, pessoa, cpf_cnpj, telefone, email, endereco)
            st.success('Cliente adicionado!')
            st.rerun()
        else:
            st.error('Nome e CPF/CNPJ são obrigatórios.')

# ESTOQUE
elif pagina == 'Estoque':
    st.header('Estoque')

    # Listar
    estoque = listar_estoque()
    if estoque:
        st.subheader('Produtos cadastrados')
        for produto in estoque:
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{produto[1]}** | {produto[2]} | {produto[3]} | {produto[4]}")
            if col2.button('Excluir', key=f'del_{produto[0]}'):
                excluir_estoque(produto[0])
                st.rerun()
    else:
        st.info('Nenhum produto cadastrado.')

    # Adicionar
    st.subheader('Adicionar produto')
    with st.form('form_produto'):
        nome = st.text_input('Nome')
        validade = st.text_input('Validade')
        preco = st.number_input('Preço', min_value=0, format="%.2f")
        quantidade = st.number_input('Quantidade', min_value=0, step=1)
        salvar = st.form_submit_button('Salvar')

    if salvar:
        if nome and preco and quantidade:
            adicionar_estoque(nome, validade, preco, quantidade)
            st.success('Produto adicionado!')
            st.rerun()
        else:
            st.error('Nome, preço e quantidade são obrigatórios.')

# SERVIÇOS
if pagina == 'Serviços':
    st.header('Serviços')

    # Listar
    servicos = listar_servicos()
    if servicos:
        st.subheader('Serviços disponíveis')
        df = pd.DataFrame(servicos, columns=['ID', 'Nome', 'Tempo Médio (min)', 'Preço (R$)'])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info('Nenhum registro disponível.')

    # Adicionar
    st.subheader('Adicionar serviço')
    with st.form('form_servico'):
        nome = st.text_input('Nome')
        tempo_medio = st.text_input('Tempo médio')
        preco = st.number_input('Preço', min_value=0, format="%.2f")
        salvar = st.form_submit_button('Salvar')

    if salvar:
        if nome and preco:
            adicionar_servico(nome, tempo_medio, preco)
            st.success('Serviço adicionado!')
            st.rerun()
        else:
            st.error('Nome e valor são obrigatórios.')

# TRANSAÇÕES
elif pagina == 'Transações':
    st.header('Transações')

    # Listar
    transacoes = listar_transacoes()
    if transacoes:
        st.subheader('Serviços Prestados')
        for servico in transacoes:
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{servico[1]}** | {servico[2]} | {servico[3]}")
            if col2.button('Excluir', key=f'del_{servico[0]}'):
                excluir_transacao(servico[0])
                st.rerun()
    else:
        st.info('Nenhum serviço realizado.')

    # Adicionar
    st.subheader('Adicionar serviço')
    with st.form('form_transacoes'):
        id_cliente = st.number_input('id do cliente')
        id_servico = st.number_input('id do serviço')
        data_hora = st.text_input('data/hora')
        valor = st.number_input('Valor', min_value=0, format="%.2f")
        salvar = st.form_submit_button('Salvar')

    if salvar:
        if id_cliente and id_servico and data_hora and valor:
            adicionar_transacao(id_cliente, id_servico, data_hora, valor)
            st.success('Serviço realizado adicionado!')
            st.rerun()
        else:
            st.error('Adicione todas as informações!')

# AGENDAMENTOS
if pagina == 'Agendamentos':
    st.header('Agendamentos')

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM Clientes")
    clientes = cursor.fetchall()
    conn.close()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM Servicos")
    servicos = cursor.fetchall()
    conn.close()

    # Verifica se tem dados
    if not clientes:
        st.warning('Nenhum cliente cadastrado. Cadastre um cliente primeiro.')
        st.stop()

    if not servicos:
        st.warning('Nenhum serviço cadastrado. Cadastre um serviço primeiro.')
        st.stop()

    # Listar
    agendamento = listar_agendamentos()
    if agendamento:
        st.subheader('Serviços Agendados')
        for a in agendamento:
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{a[1]}** | {a[2]} | {a[3]} | {a[4]}")
            if col2.button('Excluir', key=f'del_{a[0]}'):
                excluir_cliente(a[0])
                st.rerun()
    else:
        st.info('Nenhum agendamento.')

    # Adicionar
    st.subheader('Adicionar Agendamento')
    with st.form('form_agendamentos'):
        # Cliente
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM Clientes")
        clientes = cursor.fetchall()
        conn.close()

        cliente_selecionado = st.selectbox(
            'Cliente',
            options=clientes,
            format_func=lambda x: x[1]
        )
        id_cliente = cliente_selecionado[0]

        # Serviço
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM Servicos")
        servicos = cursor.fetchall()
        conn.close()

        servico_selecionado = st.selectbox(
            'Serviço',
            options=servicos,
            format_func=lambda x: x[1]
        )
        id_servico = servico_selecionado[0]

        data_hora = st.text_input('Data e Hora')
        status = st.selectbox('Status', ['Aguardando', 'Agendado'])
        observacao = st.text_input('Observações')
        salvar = st.form_submit_button('Salvar')
    if salvar:
        if nome and preco:
            adicionar_servico(nome, tempo_medio, preco)
            st.success('Serviço adicionado!')
            st.rerun()
        else:
            st.error('Nome e valor são obrigatórios.')