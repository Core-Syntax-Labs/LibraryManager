import sqlite3
from datetime import date

# CLASSE LIVRO

class Livro:
    def __init__(self, id, titulo, autor, quantidade):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.quantidade = quantidade

    def emprestar(self):
        if self.quantidade > 0:
            self.quantidade -= 1
            return True
        return False

    def devolver(self):
        self.quantidade += 1

# CLASSE LEITOR

class Leitor:
    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula
        self.emprestimos = []

# CLASSE EMPRESTIMO

class Emprestimo:
    def __init__(self, livro, leitor):
        self.livro = livro
        self.leitor = leitor
        self.data_emprestimo = date.today()
        self.dias_passados = 0
        self.prazo = 7
        self.devolvido = False

    def simular_dias(self):
        for dia in range(9):
            self.dias_passados += 1
            print(f"Dia {self.dias_passados}")

        print("Prazo de empréstimo encerrado!")

    def calcular_multa(self):
        atraso = self.dias_passados - self.prazo

        if atraso > 0:
            multa = atraso * 2.00
            print(f"Dias de atraso: {atraso}")
            print(f"Multa: R$ {multa:.2f}")
        else:
            print("Livro dentro do prazo!")

    def devolver_livro(self):
        if not self.devolvido:
            self.livro.devolver()
            self.devolvido = True
            print("Livro devolvido com sucesso!")
            self.calcular_multa()
        else:
            print("Livro já foi devolvido!")

# CLASSE BIBLIOTECA

class Biblioteca:
    def __init__(self):

        self.conexao = sqlite3.connect("biblioteca.db")
        # Permite acessar os registros usando nomes das colunas
        self.conexao.row_factory = sqlite3.Row
        # Ativa o suporte a chaves estrangeiras
        self.conexao.execute("PRAGMA foreign_keys = ON")
        self.criar_tabelas()
        self.popular_livros_exemplo()

        # Listas mantidas em memória durante a execução do programa.
        self.livros = []
        self.leitores = []
        self.emprestimos = []

        self.carregar_livros()
        self.carregar_leitores()
        self.carregar_emprestimos()

    def criar_tabelas(self):
        cursor = self.conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                quantidade INTEGER NOT NULL CHECK (quantidade >= 0)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leitores (
                matricula TEXT PRIMARY KEY,
                nome TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                livro_id INTEGER NOT NULL,
                leitor_matricula TEXT NOT NULL,

                data_emprestimo TEXT NOT NULL,
                dias_passados INTEGER DEFAULT 0,
                prazo INTEGER DEFAULT 7,
                devolvido INTEGER DEFAULT 0,

                FOREIGN KEY (livro_id)
                    REFERENCES livros(id),

                FOREIGN KEY (leitor_matricula)
                    REFERENCES leitores(matricula)
            )
        """)
        self.conexao.commit()

    def popular_livros_exemplo(self):
        """Insere livros de exemplo apenas se a tabela estiver vazia."""
        cursor = self.conexao.cursor()

        cursor.execute("SELECT COUNT(*) FROM livros")
        if cursor.fetchone()[0] > 0:
            return

        livros_exemplo = [
            ("Crime e Castigo", "Fiódor Dostoiévski", 3),
            ("1984", "George Orwell", 3),
            ("A Biblioteca da Meia-Noite", "Matt Haig", 3),
            ("A Revolução dos Bichos", "George Orwell", 3),
            ("A Metamorfose", "Franz Kafka", 3),
            ("O Médico e o Monstro", "Robert Louis Stevenson", 3),
            ("Capitães de Areia", "Jorge Amado", 3),
        ]

        cursor.executemany("""
            INSERT INTO livros (titulo, autor, quantidade)
            VALUES (?, ?, ?)
        """, livros_exemplo)

        self.conexao.commit()

    def carregar_livros(self):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT id, titulo, autor, quantidade
            FROM livros
        """)

        registros = cursor.fetchall()

        self.livros.clear()

        for registro in registros:

            livro = Livro(
                registro["id"],
                registro["titulo"],
                registro["autor"],
                registro["quantidade"]
            )

            self.livros.append(livro)

        print(f"{len(self.livros)} livro(s) carregado(s).")

    def carregar_emprestimos(self):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                livro_id,
                leitor_matricula,
                data_emprestimo,
                dias_passados,
                prazo,
                devolvido
            FROM emprestimos
        """)

        registros = cursor.fetchall()

        self.emprestimos.clear()

        for registro in registros:

            livro = next(
                (
                    l for l in self.livros
                    if l.id == registro["livro_id"]
                ),
                None
            )

            leitor = next(
                (
                    l for l in self.leitores
                    if l.matricula == registro["leitor_matricula"]
                ),
                None
            )

            # Ignora registros cujos relacionamentos
            # não puderam ser reconstruídos.
            if livro is None or leitor is None:
                continue

            emprestimo = Emprestimo(livro, leitor)

            emprestimo.id = registro["id"]
            emprestimo.data_emprestimo = date.fromisoformat(
                registro["data_emprestimo"]
            )
            emprestimo.dias_passados = registro["dias_passados"]
            emprestimo.prazo = registro["prazo"]
            emprestimo.devolvido = bool(registro["devolvido"])

            self.emprestimos.append(emprestimo)
            leitor.emprestimos.append(emprestimo)

    def cadastrar_livro(self):

        titulo = input("Título: ")
        autor = input("Autor: ")

        try:
            quantidade = int(input("Quantidade: "))

            if quantidade <= 0:
                print("Quantidade inválida!")
                return

            cursor = self.conexao.cursor()

            cursor.execute("""
                INSERT INTO livros (titulo, autor, quantidade)
                VALUES (?, ?, ?)
            """, (titulo, autor, quantidade))

            self.conexao.commit()

            print("Livro cadastrado com sucesso!")

        except ValueError:
            print("Digite uma quantidade válida!")

    def carregar_leitores(self):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT matricula, nome
            FROM leitores
        """)

        registros = cursor.fetchall()

        self.leitores.clear()

        for registro in registros:

            leitor = Leitor(
                registro["nome"],
                registro["matricula"]
            )

            self.leitores.append(leitor)

    def cadastrar_leitor(self):
        nome = input("Nome: ").strip()
        matricula = input("Matrícula: ").strip()

        if not nome or not matricula:
            print("Nome e matrícula são obrigatórios!")
            return

        if any(l.matricula == matricula for l in self.leitores):
            print("Matrícula já cadastrada!")
            return

        try:
            cursor = self.conexao.cursor()

            cursor.execute("""
                INSERT INTO leitores (matricula, nome)
                VALUES (?, ?)
            """, (matricula, nome))

            self.conexao.commit()

        except sqlite3.IntegrityError:
            # Garantia extra: a PRIMARY KEY também barra matrícula duplicada.
            self.conexao.rollback()
            print("Matrícula já cadastrada!")
            return

        # Mantém a lista em memória sincronizada com o banco.
        self.leitores.append(Leitor(nome, matricula))

        print("Leitor cadastrado com sucesso!")

    def emprestar_livro(self):
        if not self.livros or not self.leitores:
            print("Cadastre livros e leitores primeiro!")
            return

        self.listar_livros()

        titulo = input("\nDigite o título do livro: ")
        matricula = input("Matrícula do leitor: ")

        livro = next(
            (l for l in self.livros
             if l.titulo.lower() == titulo.lower()), None
        )

        leitor = next(
            (l for l in self.leitores
             if l.matricula == matricula), None
        )

        if livro is None or leitor is None:
            print("Livro ou leitor não encontrado!")
            return

        # TODO: Implementar a persistência do empréstimo.
        # 1. Verificar a disponibilidade no banco.
        # 2. Registrar o empréstimo na tabela emprestimos.
        # 3. Atualizar a quantidade disponível do livro.
        # 4. Manter os relacionamentos entre Livro e Leitor.

        print("Empréstimo aguardando implementação da persistência.")
        return

        opcao = input("Simular passagem de 9 dias? (s/n): ")

        if opcao.lower() == "s":
            emprestimo.simular_dias()

    def registrar_devolucao(self):
        ativos = [
            e for e in self.emprestimos
            if not e.devolvido
        ]

        if not ativos:
            print("Não existem empréstimos ativos!")
            return

        for i, e in enumerate(ativos):
            print(f"{i + 1} - {e.livro.titulo} | {e.leitor.nome}")

        try:
            escolha = int(input("Escolha o empréstimo: "))
            emprestimo = ativos[escolha - 1]
        except (ValueError, IndexError):
            print("Opção inválida!")
            return

        # TODO: Implementar a persistência da devolução.
        # 1. Atualizar o campo devolvido no SQLite.
        # 2. Restaurar a quantidade disponível do livro.
        # 3. Garantir que a devolução não seja registrada duas vezes.

        print("Devolução aguardando implementação da persistência.")
        return

    def consultar_disponiveis(self):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT titulo, quantidade
            FROM livros
            WHERE quantidade > 0
            ORDER BY titulo
        """)

        livros = cursor.fetchall()

        print("\n--- LIVROS DISPONÍVEIS ---")

        if not livros:
            print("Nenhum livro disponível!")
            return

        for livro in livros:

            print(
                f"{livro['titulo']} - "
                f"{livro['quantidade']} disponíveis"
            )

    def listar_livros(self):

        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT id, titulo, autor, quantidade
            FROM livros
        """)

        livros = cursor.fetchall()

        print("\n--- LIVROS CADASTRADOS ---")

        for livro in livros:

            print(
                f"{livro['titulo']} | "
                f"{livro['autor']} | "
                f"Disponíveis: {livro['quantidade']}"
            )

    def consultar_pendencias(self):

        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT
                leitores.nome,
                livros.titulo
            FROM emprestimos

            INNER JOIN leitores
                ON emprestimos.leitor_matricula = leitores.matricula

            INNER JOIN livros
                ON emprestimos.livro_id = livros.id

            WHERE emprestimos.devolvido = 0

            ORDER BY leitores.nome
        """)

        registros = cursor.fetchall()

        print("\n--- LEITORES COM PENDÊNCIAS ---")

        if not registros:
            print("Nenhuma pendência!")
            return

        leitor_atual = None

        for registro in registros:

            nome = registro["nome"]

            if nome != leitor_atual:

                leitor_atual = nome

                print(f"\nLeitor: {nome}")

            print(f"Livro: {registro['titulo']}")

    def consultar_emprestados(self):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT
                livros.titulo,
                leitores.nome
            FROM emprestimos

            INNER JOIN livros
                ON emprestimos.livro_id = livros.id

            INNER JOIN leitores
                ON emprestimos.leitor_matricula = leitores.matricula

            WHERE emprestimos.devolvido = 0

            ORDER BY leitores.nome
        """)

        registros = cursor.fetchall()

        print("\n--- LIVROS EMPRESTADOS ---")

        if not registros:
            print("Nenhum livro emprestado!")
            return

        for registro in registros:

            print(
                f"{registro['titulo']} - "
                f"{registro['nome']}"
            )

    def relatorio(self):
        cursor = self.conexao.cursor()

        cursor.execute("""
            SELECT
                (SELECT COUNT(*) FROM livros) AS total_livros,

                (SELECT COUNT(*) FROM leitores) AS total_leitores,

                (SELECT COUNT(*) FROM emprestimos) AS total_emprestimos,

                (SELECT COUNT(*)
                FROM emprestimos
                WHERE devolvido = 0) AS ativos,

                (SELECT COUNT(*)
                FROM emprestimos
                WHERE devolvido = 1) AS finalizados
        """)

        dados = cursor.fetchone()

        print("\n========== RELATÓRIO ==========")

        print("Livros:", dados["total_livros"])
        print("Leitores:", dados["total_leitores"])
        print("Empréstimos:", dados["total_emprestimos"])
        print("Ativos:", dados["ativos"])
        print("Finalizados:", dados["finalizados"])

# PROGRAMA PRINCIPAL

def perguntar_continuar():
    """Pergunta se o usuário quer voltar ao menu (1) ou sair (0)."""
    while True:
        escolha = input("\nDigite 1 para voltar ao menu ou 0 para sair: ").strip()

        if escolha == "1":
            return True
        if escolha == "0":
            return False

        print("Opção inválida!")


biblioteca = Biblioteca()

acoes = {
    "1": biblioteca.cadastrar_livro,
    "2": biblioteca.cadastrar_leitor,
    "3": biblioteca.emprestar_livro,
    "4": biblioteca.registrar_devolucao,
    "5": biblioteca.consultar_disponiveis,
    "6": biblioteca.consultar_emprestados,
    "7": biblioteca.consultar_pendencias,
    "8": biblioteca.relatorio,
}

while True:

    print("\n========== BIBLIOTECA ==========")
    print("1 - Cadastrar livro")
    print("2 - Cadastrar leitor")
    print("3 - Realizar empréstimo")
    print("4 - Registrar devolução")
    print("5 - Consultar livros disponíveis")
    print("6 - Consultar livros emprestados")
    print("7 - Consultar leitores com pendências")
    print("8 - Gerar relatório")
    print("0 - Sair")

    opcao = input("\nEscolha uma opção: ").strip()

    if opcao == "0":
        print("Sistema encerrado!")
        break

    acao = acoes.get(opcao)

    if acao is None:
        print("Opção inválida!")
        continue

    acao()

    if not perguntar_continuar():
        print("Sistema encerrado!")
        break