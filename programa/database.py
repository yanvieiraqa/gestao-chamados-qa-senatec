"""
Camada de dados do Gestão de Chamados Senatec.
Concentra todo o acesso ao banco de dados SQLite.
"""

import os
import shutil
import sqlite3
from datetime import datetime

from config import DB_PATH, BACKUP_DIR, STATUS_INFO, LOCAIS_PADRAO, DIAS_ALERTA_PENDENTE


class ChamadosDB:
    """Concentra todo o acesso ao banco de dados SQLite."""

    def __init__(self, caminho=DB_PATH):
        self.conn = sqlite3.connect(caminho)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._criar_tabela()

    def _criar_tabela(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS chamados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                contrato TEXT NOT NULL,
                local TEXT NOT NULL,
                descricao TEXT NOT NULL,
                equipamento TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                prioridade TEXT NOT NULL DEFAULT 'Normal',
                tecnico TEXT,
                status TEXT NOT NULL DEFAULT 'Pendente',
                data_abertura TEXT
            )
        """)
        # Migração leve para bancos antigos (colunas que podem não existir ainda)
        cols = [c[1] for c in self.conn.execute("PRAGMA table_info(chamados)")]
        for coluna, definicao in [
            ("data_abertura", "TEXT"),
            ("prioridade", "TEXT NOT NULL DEFAULT 'Normal'"),
            ("tecnico", "TEXT"),
        ]:
            if coluna not in cols:
                self.conn.execute(f"ALTER TABLE chamados ADD COLUMN {coluna} {definicao}")
        # Chamados antigos que estavam como "Previsão" (aba removida) viram Pendente
        self.conn.execute("UPDATE chamados SET status='Pendente' WHERE status='Previsão'")
        self.conn.commit()

    def inserir(self, dados: dict):
        self.conn.execute("""
            INSERT INTO chamados
            (cliente, contrato, local, descricao, equipamento, quantidade,
             prioridade, tecnico, status, data_abertura)
            VALUES (:cliente, :contrato, :local, :descricao, :equipamento, :quantidade,
                    :prioridade, :tecnico, :status, :data_abertura)
        """, dados)
        self.conn.commit()

    def atualizar(self, chamado_id, dados: dict):
        dados = dict(dados, id=chamado_id)
        self.conn.execute("""
            UPDATE chamados SET
                cliente=:cliente, contrato=:contrato, local=:local,
                descricao=:descricao, equipamento=:equipamento, quantidade=:quantidade,
                prioridade=:prioridade, tecnico=:tecnico, status=:status,
                data_abertura=:data_abertura
            WHERE id=:id
        """, dados)
        self.conn.commit()

    def alterar_status(self, chamado_id, novo_status):
        self.conn.execute("UPDATE chamados SET status=? WHERE id=?", (novo_status, chamado_id))
        self.conn.commit()

    def excluir(self, chamado_id):
        self.conn.execute("DELETE FROM chamados WHERE id=?", (chamado_id,))
        self.conn.commit()

    def buscar(self, status=None, termo=None, locais=None):
        query = """SELECT id, cliente, contrato, local, descricao, equipamento, quantidade,
                          prioridade, tecnico, status, data_abertura FROM chamados"""
        condicoes, params = [], []
        if status:
            condicoes.append("status=?")
            params.append(status)
        if termo:
            condicoes.append("(cliente LIKE ? OR contrato LIKE ? OR local LIKE ? OR equipamento LIKE ?)")
            params.extend([f"%{termo}%"] * 4)
        if locais:
            placeholders = ",".join("?" for _ in locais)
            condicoes.append(f"local IN ({placeholders})")
            params.extend(locais)
        if condicoes:
            query += " WHERE " + " AND ".join(condicoes)
        query += " ORDER BY CASE prioridade WHEN 'Urgente' THEN 0 ELSE 1 END, id DESC"
        return self.conn.execute(query, params).fetchall()

    def ultimo_local(self, cliente, contrato):
        row = self.conn.execute(
            "SELECT local FROM chamados WHERE cliente=? AND contrato=? ORDER BY id DESC LIMIT 1",
            (cliente, contrato)
        ).fetchone()
        return row[0] if row else None

    def contagem_por_status(self):
        rows = self.conn.execute("SELECT status, COUNT(*) FROM chamados GROUP BY status").fetchall()
        contagem = {s: 0 for s in STATUS_INFO}
        contagem.update(dict(rows))
        return contagem

    def pendentes_atrasados(self, dias=DIAS_ALERTA_PENDENTE):
        """Conta chamados pendentes cuja data de abertura já passou de X dias."""
        total = 0
        hoje = datetime.now()
        for (data_txt,) in self.conn.execute("SELECT data_abertura FROM chamados WHERE status='Pendente'"):
            if not data_txt:
                continue
            try:
                data = datetime.strptime(data_txt.split(" ")[0], "%d/%m/%Y")
            except ValueError:
                continue
            if (hoje - data).days >= dias:
                total += 1
        return total

    def locais_conhecidos(self):
        rows = self.conn.execute("SELECT DISTINCT local FROM chamados").fetchall()
        locais = sorted({r[0] for r in rows if r[0]})
        for l in LOCAIS_PADRAO:
            if l not in locais:
                locais.append(l)
        return sorted(locais)

    def backup(self):
        """Faz uma cópia do banco de dados uma vez por dia na pasta 'backups'."""
        try:
            os.makedirs(BACKUP_DIR, exist_ok=True)
            nome = f"chamados_{datetime.now().strftime('%Y-%m-%d')}.db"
            destino = os.path.join(BACKUP_DIR, nome)
            if not os.path.exists(destino) and os.path.exists(DB_PATH):
                shutil.copy2(DB_PATH, destino)
        except Exception:
            pass  # backup nunca deve travar o app
