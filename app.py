import streamlit as st
import sqlite3
import pandas as pd

def conectar():
    return sqlite3.connect('manutencao.db')

# ─── CLIENTES ────────────────────────────────────────────────────────────────
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, pessoa, cpf_cnpj, telefone, email, endereco FROM Clientes")
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

# ─── ESTOQUE ─────────────────────────────────────────────────────────────────
def listar_estoque():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, validade, preco, quantidade FROM Estoque")
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

# ─── SERVIÇOS ─────────────────────────────────────────────────────────────────
def listar_servicos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, tempo_medio, preco FROM Servicos")
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

# ─── TRANSAÇÕES ──────────────────────────────────────────────────────────────
def listar_transacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            t.id,
            c.nome AS cliente,
            s.nome AS servico,
            t.data_hora,
            t.valor
        FROM Transacoes t
        JOIN Clientes c ON t.id_cliente = c.id
        JOIN Servicos s ON t.id_servico = s.id
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

# ─── AGENDAMENTOS ─────────────────────────────────────────────────────────────
def listar_agendamentos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            t.id,
            c.nome AS cliente,
            s.nome AS servico,
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
pagina = st.sidebar.selectbox('Navegação', ['Clientes', 'Estoque', 'Serviços', 'Agendamentos', 'Transações'])

# ─── CLIENTES ─────────────────────────────────────────────────────────────────
if pagina == 'Clientes':
    st.header('Clientes')

    clientes = listar_clientes()
    if clientes:
        st.subheader('Clientes cadastrados')
        df = pd.DataFrame(clientes, columns=['ID', 'Nome', 'Tipo', 'CPF/CNPJ', 'Telefone', 'Email', 'Endereço'])
        st.dataframe(df, use_container_width=True, hide_index=True)

        excluir_id = st.number_input('ID do cliente para excluir', min_value=1, step=1)
        if st.button('Excluir cliente'):
            excluir_cliente(excluir_id)
            st.success('Cliente excluído!')
            st.rerun()
    else:
        st.info('Nenhum cliente cadastrado.')

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

# ─── ESTOQUE ──────────────────────────────────────────────────────────────────
elif pagina == 'Estoque':
    st.header('Estoque')

    estoque = listar_estoque()
    if estoque:
        st.subheader('Produtos cadastrados')
        df = pd.DataFrame(estoque, columns=['ID', 'Nome', 'Validade', 'Preço (R$)', 'Quantidade'])
        st.dataframe(df, use_container_width=True, hide_index=True)

        excluir_id = st.number_input('ID do produto para excluir', min_value=1, step=1)
        if st.button('Excluir produto'):
            excluir_estoque(excluir_id)
            st.success('Produto excluído!')
            st.rerun()
    else:
        st.info('Nenhum produto cadastrado.')

    st.subheader('Adicionar produto')
    with st.form('form_produto'):
        nome = st.text_input('Nome')
        validade = st.text_input('Validade')
        preco = st.number_input('Preço', min_value=0.0, format="%.2f")
        quantidade = st.number_input('Quantidade', min_value=0, step=1)
        salvar = st.form_submit_button('Salvar')

    if salvar:
        if nome and preco and quantidade:
            adicionar_estoque(nome, validade, preco, quantidade)
            st.success('Produto adicionado!')
            st.rerun()
        else:
            st.error('Nome, preço e quantidade são obrigatórios.')

# ─── SERVIÇOS ─────────────────────────────────────────────────────────────────
elif pagina == 'Serviços':
    st.header('Serviços')

    servicos = listar_servicos()
    if servicos:
        st.subheader('Serviços disponíveis')
        df = pd.DataFrame(servicos, columns=['ID', 'Nome', 'Tempo Médio (min)', 'Preço (R$)'])
        st.dataframe(df, use_container_width=True, hide_index=True)

        excluir_id = st.number_input('ID do serviço para excluir', min_value=1, step=1)
        if st.button('Excluir serviço'):
            excluir_servico(excluir_id)
            st.success('Serviço excluído!')
            st.rerun()
    else:
        st.info('Nenhum serviço cadastrado.')

    st.subheader('Adicionar serviço')
    with st.form('form_servico'):
        nome = st.text_input('Nome')
        tempo_medio = st.number_input('Tempo médio (min)', min_value=0, step=1)
        preco = st.number_input('Preço', min_value=0.0, format="%.2f")
        salvar = st.form_submit_button('Salvar')

    if salvar:
        if nome and preco:
            adicionar_servico(nome, tempo_medio, preco)
            st.success('Serviço adicionado!')
            st.rerun()
        else:
            st.error('Nome e preço são obrigatórios.')

# ─── AGENDAMENTOS ─────────────────────────────────────────────────────────────
elif pagina == 'Agendamentos':
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

    if not clientes:
        st.warning('Nenhum cliente cadastrado. Cadastre um cliente primeiro.')
        st.stop()

    if not servicos:
        st.warning('Nenhum serviço cadastrado. Cadastre um serviço primeiro.')
        st.stop()

    agendamentos = listar_agendamentos()
    if agendamentos:
        st.subheader('Serviços Agendados')
        df = pd.DataFrame(agendamentos, columns=['ID', 'Cliente', 'Serviço', 'Data/Hora', 'Observação', 'Status'])
        st.dataframe(df, use_container_width=True, hide_index=True)

        excluir_id = st.number_input('ID do agendamento para excluir', min_value=1, step=1)
        if st.button('Excluir agendamento'):
            excluir_agendamento(excluir_id)
            st.success('Agendamento excluído!')
            st.rerun()
    else:
        st.info('Nenhum agendamento.')

    st.subheader('Adicionar Agendamento')
    with st.form('form_agendamentos'):
        cliente_selecionado = st.selectbox('Cliente', options=clientes, format_func=lambda x: x[1])
        id_cliente = cliente_selecionado[0]

        servico_selecionado = st.selectbox('Serviço', options=servicos, format_func=lambda x: x[1])
        id_servico = servico_selecionado[0]

        data_hora = st.text_input('Data e Hora (ex: 2026-10-20 14:00)')
        status = st.selectbox('Status', ['Agendado', 'Aguardando', 'Concluído', 'Cancelado'])
        observacao = st.text_input('Observações')
        salvar = st.form_submit_button('Salvar')

    if salvar:
        if data_hora:
            adicionar_agendamento(id_cliente, id_servico, data_hora, status, observacao)
            st.success('Agendamento adicionado!')
            st.rerun()
        else:
            st.error('Data e hora são obrigatórios.')

# ─── TRANSAÇÕES ───────────────────────────────────────────────────────────────
elif pagina == 'Transações':
    st.header('Transações')

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

    if not clientes:
        st.warning('Nenhum cliente cadastrado. Cadastre um cliente primeiro.')
        st.stop()

    if not servicos:
        st.warning('Nenhum serviço cadastrado. Cadastre um serviço primeiro.')
        st.stop()

    transacoes = listar_transacoes()
    if transacoes:
        st.subheader('Serviços Prestados')
        df = pd.DataFrame(transacoes, columns=['ID', 'Cliente', 'Serviço', 'Data/Hora', 'Valor (R$)'])
        st.dataframe(df, use_container_width=True, hide_index=True)

        excluir_id = st.number_input('ID da transação para excluir', min_value=1, step=1)
        if st.button('Excluir transação'):
            excluir_transacao(excluir_id)
            st.success('Transação excluída!')
            st.rerun()
    else:
        st.info('Nenhuma transação registrada.')

    st.subheader('Registrar serviço prestado')
    with st.form('form_transacoes'):
        cliente_selecionado = st.selectbox('Cliente', options=clientes, format_func=lambda x: x[1])
        id_cliente = cliente_selecionado[0]

        servico_selecionado = st.selectbox('Serviço', options=servicos, format_func=lambda x: x[1])
        id_servico = servico_selecionado[0]

        data_hora = st.text_input('Data e Hora (ex: 2026-10-20 14:00)')
        valor = st.number_input('Valor (R$)', min_value=0.0, format="%.2f")
        salvar = st.form_submit_button('Salvar')

    if salvar:
        if data_hora and valor:
            adicionar_transacao(id_cliente, id_servico, data_hora, valor)
            st.success('Transação registrada!')
            st.rerun()
        else:
            st.error('Data/hora e valor são obrigatórios.')
