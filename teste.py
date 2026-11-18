
from datetime import date


# ==========================
# CLASSE LIVRO
# ==========================

class Livro:
    def __init__(self, titulo, autor, quantidade):
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


# ==========================
# CLASSE LEITOR
# ==========================

class Leitor:
    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula
        self.emprestimos = []


# ==========================
# CLASSE EMPRESTIMO
# ==========================

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


# ==========================
# CLASSE BIBLIOTECA
# ==========================

class Biblioteca:
    def __init__(self):
        self.livros = []
        self.leitores = []
        self.emprestimos = []

    def cadastrar_livro(self):
        titulo = input("Título: ")
        autor = input("Autor: ")
        quantidade = int(input("Quantidade: "))

        if quantidade <= 0:
            print("Quantidade inválida!")
            return

        livro = Livro(titulo, autor, quantidade)
        self.livros.append(livro)

        print("Livro cadastrado com sucesso!")

    def cadastrar_leitor(self):
        nome = input("Nome: ")
        matricula = input("Matrícula: ")

        if any(l.matricula == matricula for l in self.leitores):
            print("Matrícula já cadastrada!")
            return

        leitor = Leitor(nome, matricula)
        self.leitores.append(leitor)

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

        if not livro.emprestar():
            print("Livro indisponível!")
            return

        emprestimo = Emprestimo(livro, leitor)

        self.emprestimos.append(emprestimo)
        leitor.emprestimos.append(emprestimo)

        print("Empréstimo realizado com sucesso!")

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

        emprestimo.devolver_livro()

    def listar_livros(self):
        print("\n--- LIVROS CADASTRADOS ---")

        for livro in self.livros:
            print(
                f"{livro.titulo} | {livro.autor} | "
                f"Disponíveis: {livro.quantidade}"
            )

    def consultar_disponiveis(self):
        print("\n--- LIVROS DISPONÍVEIS ---")

        for livro in self.livros:
            if livro.quantidade > 0:
                print(f"{livro.titulo} - {livro.quantidade} disponíveis")

    def consultar_emprestados(self):
        print("\n--- LIVROS EMPRESTADOS ---")

        for e in self.emprestimos:
            if not e.devolvido:
                print(f"{e.livro.titulo} - {e.leitor.nome}")

    def consultar_pendencias(self):
        print("\n--- LEITORES COM PENDÊNCIAS ---")

        encontrou = False

        for leitor in self.leitores:
            pendentes = [
                e for e in leitor.emprestimos
                if not e.devolvido
            ]

            if pendentes:
                encontrou = True
                print(f"\nLeitor: {leitor.nome}")

                for e in pendentes:
                    print(f"Livro: {e.livro.titulo}")

        if not encontrou:
            print("Nenhuma pendência!")

    def relatorio(self):
        ativos = sum(not e.devolvido for e in self.emprestimos)

        print("\n========== RELATÓRIO ==========")
        print("Livros:", len(self.livros))
        print("Leitores:", len(self.leitores))
        print("Empréstimos:", len(self.emprestimos))
        print("Ativos:", ativos)
        print("Finalizados:", len(self.emprestimos) - ativos)


# ==========================
# PROGRAMA PRINCIPAL
# ==========================

biblioteca = Biblioteca()

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

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        biblioteca.cadastrar_livro()

    elif opcao == "2":
        biblioteca.cadastrar_leitor()

    elif opcao == "3":
        biblioteca.emprestar_livro()

    elif opcao == "4":
        biblioteca.registrar_devolucao()

    elif opcao == "5":
        biblioteca.consultar_disponiveis()

    elif opcao == "6":
        biblioteca.consultar_emprestados()

    elif opcao == "7":
        biblioteca.consultar_pendencias()

    elif opcao == "8":
        biblioteca.relatorio()

    elif opcao == "0":
        print("Sistema encerrado!")
        break

    else:
        print("Opção inválida!")
