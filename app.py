import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

def conectar():
    # Usa o banco localizado na mesma pasta deste arquivo, evitando criar
    # acidentalmente outro manutencao.db ao executar de outro diretório.
    caminho_db = Path(__file__).resolve().parent / 'manutencao.db'
    conn = sqlite3.connect(caminho_db)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def validar_data_hora(valor):
    """Aceita data/hora nos formatos AAAA-MM-DD HH:MM ou AAAA-MM-DD HH:MM:SS."""
    for formato in ('%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'):
        try:
            datetime.strptime(valor.strip(), formato)
            return True
        except ValueError:
            pass
    return False


def salvar_edicoes(df_original, df_editado, tabela, mapeamento):
    """Persiste no SQLite apenas os campos editáveis que foram alterados.

    mapeamento: dicionário {nome_da_coluna_na_tela: nome_da_coluna_no_SQLite}.
    A coluna ID é usada como identificador e nunca é alterada.
    """
    conn = conectar()
    try:
        cursor = conn.cursor()
        originais = df_original.set_index('ID')
        editados = df_editado.set_index('ID')

        for id_registro in editados.index:
            if id_registro not in originais.index:
                continue

            alteracoes = {}
            for coluna_tela, coluna_sql in mapeamento.items():
                valor_antigo = originais.at[id_registro, coluna_tela]
                valor_novo = editados.at[id_registro, coluna_tela]

                antigo_nulo = pd.isna(valor_antigo)
                novo_nulo = pd.isna(valor_novo)
                iguais = (antigo_nulo and novo_nulo) or (
                    not antigo_nulo and not novo_nulo and valor_antigo == valor_novo
                )
                if not iguais:
                    alteracoes[coluna_sql] = None if novo_nulo or valor_novo == '' else valor_novo

            if alteracoes:
                clausula = ', '.join(f'"{coluna}" = ?' for coluna in alteracoes)
                valores = list(alteracoes.values()) + [int(id_registro)]
                cursor.execute(f'UPDATE "{tabela}" SET {clausula} WHERE id = ?', valores)

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

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
            t.valor,
            t.pagamento
        FROM Transacoes t
        JOIN Clientes c ON t.id_cliente = c.id
        JOIN Servicos s ON t.id_servico = s.id
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def adicionar_transacao(id_cliente, id_servico, data_hora, valor, pagamento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Transacoes (id_cliente, id_servico, data_hora, valor, pagamento)
        VALUES (?, ?, ?, ?, ?)
    """, (id_cliente, id_servico, data_hora, valor, pagamento))
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
        editado = st.data_editor(
            df, key='editor_clientes', use_container_width=True, hide_index=True,
            num_rows='fixed',
            disabled=['ID'],
            column_config={'Tipo': st.column_config.SelectboxColumn('Tipo', options=['Física', 'Jurídica'])}
        )
        if st.button('Salvar alterações nos clientes', key='salvar_clientes'):
            try:
                salvar_edicoes(df, editado, 'Clientes', {
                    'Nome': 'nome', 'Tipo': 'pessoa', 'CPF/CNPJ': 'cpf_cnpj',
                    'Telefone': 'telefone', 'Email': 'email', 'Endereço': 'endereco'
                })
                st.success('Alterações dos clientes salvas.')
                st.rerun()
            except sqlite3.Error as erro:
                st.error(f'Não foi possível salvar as alterações: {erro}')

        excluir_id = st.number_input('ID do cliente para excluir', min_value=1, step=1)
        if st.button('Excluir cliente'):
            try:
                excluir_cliente(int(excluir_id))
                st.success('Cliente excluído!')
                st.rerun()
            except sqlite3.IntegrityError:
                st.error('Não foi possível excluir: este registro pode estar vinculado a transações ou agendamentos.')
            except sqlite3.Error as erro:
                st.error(f'Erro ao excluir cliente: {erro}')
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
        if nome.strip() and cpf_cnpj.strip() and telefone.strip():
            try:
                adicionar_cliente(nome.strip(), pessoa, cpf_cnpj.strip(), telefone.strip(), email.strip() or None, endereco.strip() or None)
                st.success('Cliente adicionado!')
                st.rerun()
            except sqlite3.IntegrityError as erro:
                st.error(f'Não foi possível cadastrar o cliente. Verifique CPF/CNPJ duplicado ou campos obrigatórios. Detalhe: {erro}')
            except sqlite3.Error as erro:
                st.error(f'Erro no banco de dados: {erro}')
        else:
            st.error('Nome, CPF/CNPJ e telefone são obrigatórios.')

# ─── ESTOQUE ──────────────────────────────────────────────────────────────────
elif pagina == 'Estoque':
    st.header('Estoque')

    estoque = listar_estoque()
    if estoque:
        st.subheader('Produtos cadastrados')
        df = pd.DataFrame(estoque, columns=['ID', 'Nome', 'Validade', 'Preço (R$)', 'Quantidade'])
        editado = st.data_editor(
            df, key='editor_estoque', use_container_width=True, hide_index=True,
            num_rows='fixed', disabled=['ID'],
            column_config={
                'Preço (R$)': st.column_config.NumberColumn('Preço (R$)', min_value=0.0, format='%.2f'),
                'Quantidade': st.column_config.NumberColumn('Quantidade', min_value=0, step=1)
            }
        )
        if st.button('Salvar alterações no estoque', key='salvar_estoque'):
            try:
                salvar_edicoes(df, editado, 'Estoque', {
                    'Nome': 'nome', 'Validade': 'validade', 'Preço (R$)': 'preco', 'Quantidade': 'quantidade'
                })
                st.success('Alterações do estoque salvas.')
                st.rerun()
            except sqlite3.Error as erro:
                st.error(f'Não foi possível salvar as alterações: {erro}')

        excluir_id = st.number_input('ID do produto para excluir', min_value=1, step=1)
        if st.button('Excluir produto'):
            try:
                excluir_estoque(int(excluir_id))
                st.success('Produto excluído!')
                st.rerun()
            except sqlite3.IntegrityError:
                st.error('Não foi possível excluir: este registro pode estar vinculado a transações ou agendamentos.')
            except sqlite3.Error as erro:
                st.error(f'Erro ao excluir produto: {erro}')
    else:
        st.info('Nenhum produto cadastrado.')

    st.subheader('Adicionar produto')
    with st.form('form_produto'):
        nome = st.text_input('Nome do produto')
        validade = st.text_input('Validade')
        preco = st.number_input('Preço unitário', min_value=0.0, format="%.2f")
        quantidade = st.number_input('Quantidade', min_value=0, step=1)
        salvar = st.form_submit_button('Salvar')

    if salvar:
        if nome.strip():
            try:
                adicionar_estoque(nome.strip(), validade.strip() or None, preco, quantidade)
                st.success('Produto adicionado!')
                st.rerun()
            except sqlite3.Error as erro:
                st.error(f'Erro ao cadastrar produto: {erro}')
        else:
            st.error('O nome do produto é obrigatório.')

# ─── SERVIÇOS ─────────────────────────────────────────────────────────────────
elif pagina == 'Serviços':
    st.header('Serviços')

    servicos = listar_servicos()
    if servicos:
        st.subheader('Serviços disponíveis')
        df = pd.DataFrame(servicos, columns=['ID', 'Nome', 'Tempo Médio (min)', 'Preço (R$)'])
        editado = st.data_editor(
            df, key='editor_servicos', use_container_width=True, hide_index=True,
            num_rows='fixed', disabled=['ID'],
            column_config={
                'Tempo Médio (min)': st.column_config.NumberColumn('Tempo Médio (min)', min_value=0, step=1),
                'Preço (R$)': st.column_config.NumberColumn('Preço (R$)', min_value=0.0, format='%.2f')
            }
        )
        if st.button('Salvar alterações nos serviços', key='salvar_servicos'):
            try:
                salvar_edicoes(df, editado, 'Servicos', {
                    'Nome': 'nome', 'Tempo Médio (min)': 'tempo_medio', 'Preço (R$)': 'preco'
                })
                st.success('Alterações dos serviços salvas.')
                st.rerun()
            except sqlite3.Error as erro:
                st.error(f'Não foi possível salvar as alterações: {erro}')

        excluir_id = st.number_input('ID do serviço para excluir', min_value=1, step=1)
        if st.button('Excluir serviço'):
            try:
                excluir_servico(int(excluir_id))
                st.success('Serviço excluído!')
                st.rerun()
            except sqlite3.IntegrityError:
                st.error('Não foi possível excluir: este registro pode estar vinculado a transações ou agendamentos.')
            except sqlite3.Error as erro:
                st.error(f'Erro ao excluir serviço: {erro}')
    else:
        st.info('Nenhum serviço cadastrado.')

    st.subheader('Adicionar serviço')
    with st.form('form_servico'):
        nome = st.text_input('Nome')
        tempo_medio = st.number_input('Tempo médio (min)', min_value=0, step=1)
        preco = st.number_input('Preço', min_value=0.0, format="%.2f")
        salvar = st.form_submit_button('Salvar')

    if salvar:
        if nome.strip():
            try:
                adicionar_servico(nome.strip(), tempo_medio, preco)
                st.success('Serviço adicionado!')
                st.rerun()
            except sqlite3.Error as erro:
                st.error(f'Erro ao cadastrar serviço: {erro}')
        else:
            st.error('O nome do serviço é obrigatório.')

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
        editado = st.data_editor(
            df, key='editor_agendamentos', use_container_width=True, hide_index=True,
            num_rows='fixed', disabled=['ID', 'Cliente', 'Serviço'],
            column_config={
                'Status': st.column_config.SelectboxColumn(
                    'Status', options=['Agendado', 'Aguardando', 'Concluído', 'Cancelado']
                )
            }
        )
        if st.button('Salvar alterações nos agendamentos', key='salvar_agendamentos'):
            try:
                for valor in editado['Data/Hora']:
                    if not validar_data_hora(str(valor)):
                        raise ValueError('Use AAAA-MM-DD HH:MM ou AAAA-MM-DD HH:MM:SS na coluna Data/Hora.')
                salvar_edicoes(df, editado, 'Agendamentos', {
                    'Data/Hora': 'data_hora', 'Observação': 'observacao', 'Status': 'status'
                })
                st.success('Alterações dos agendamentos salvas.')
                st.rerun()
            except (sqlite3.Error, ValueError) as erro:
                st.error(f'Não foi possível salvar as alterações: {erro}')

        excluir_id = st.number_input('ID do agendamento para excluir', min_value=1, step=1)
        if st.button('Excluir agendamento'):
            try:
                excluir_agendamento(int(excluir_id))
                st.success('Agendamento excluído!')
                st.rerun()
            except sqlite3.IntegrityError:
                st.error('Não foi possível excluir: este registro pode estar vinculado a transações ou agendamentos.')
            except sqlite3.Error as erro:
                st.error(f'Erro ao excluir agendamento: {erro}')
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
        if validar_data_hora(data_hora):
            try:
                adicionar_agendamento(id_cliente, id_servico, data_hora.strip(), status, observacao.strip() or None)
                st.success('Agendamento adicionado!')
                st.rerun()
            except sqlite3.Error as erro:
                st.error(f'Erro ao registrar agendamento: {erro}')
        else:
            st.error('Informe a data e hora no formato AAAA-MM-DD HH:MM (ex.: 2026-10-22 14:30).')

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
        df = pd.DataFrame(transacoes, columns=['ID', 'Cliente', 'Serviço', 'Data/Hora', 'Valor (R$)', 'Pagamento'])
        editado = st.data_editor(
            df, key='editor_transacoes', use_container_width=True, hide_index=True,
            num_rows='fixed', disabled=['ID', 'Cliente', 'Serviço'],
            column_config={
                'Valor (R$)': st.column_config.NumberColumn('Valor (R$)', min_value=0.0, format='%.2f'),
                'Pagamento': st.column_config.SelectboxColumn('Pagamento', options=['Pendente', 'Concluído'])
            }
        )
        if st.button('Salvar alterações nas transações', key='salvar_transacoes'):
            try:
                for valor_data in editado['Data/Hora']:
                    if not validar_data_hora(str(valor_data)):
                        raise ValueError('Use AAAA-MM-DD HH:MM ou AAAA-MM-DD HH:MM:SS na coluna Data/Hora.')
                salvar_edicoes(df, editado, 'Transacoes', {
                    'Data/Hora': 'data_hora', 'Valor (R$)': 'valor', 'Pagamento': 'pagamento'
                })
                st.success('Alterações das transações salvas.')
                st.rerun()
            except (sqlite3.Error, ValueError) as erro:
                st.error(f'Não foi possível salvar as alterações: {erro}')

        excluir_id = st.number_input('ID da transação para excluir', min_value=1, step=1)
        if st.button('Excluir transação'):
            try:
                excluir_transacao(int(excluir_id))
                st.success('Transação excluída!')
                st.rerun()
            except sqlite3.IntegrityError:
                st.error('Não foi possível excluir: este registro pode estar vinculado a transações ou agendamentos.')
            except sqlite3.Error as erro:
                st.error(f'Erro ao excluir transação: {erro}')
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
        pagamento = st.selectbox('Pagamento', ['Pendente', 'Concluído'])
        salvar = st.form_submit_button('Salvar')

    if salvar:
        if validar_data_hora(data_hora):
            try:
                adicionar_transacao(id_cliente, id_servico, data_hora.strip(), valor, pagamento)
                st.success('Transação registrada!')
                st.rerun()
            except sqlite3.IntegrityError as erro:
                st.error(f'Não foi possível registrar a transação. Verifique os vínculos com cliente e serviço. Detalhe: {erro}')
            except sqlite3.Error as erro:
                st.error(f'Erro ao registrar transação: {erro}')
        else:
            st.error('Informe a data e hora no formato AAAA-MM-DD HH:MM (ex.: 2026-10-22 14:30).')
