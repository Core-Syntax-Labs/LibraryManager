# 📚 LibraryManager

O **LibraryManager** é um sistema de linha de comando (CLI) desenvolvido em Python para o gerenciamento básico de uma biblioteca. Ele permite o controle de acervo, cadastro de leitores, realização e devolução de empréstimos, cálculo automático de multas por atraso e geração de relatórios, contando com persistência de dados local via **SQLite**.

---

## 🚀 Funcionalidades

* **Gestão de Acervo:** Cadastro de livros (título, autor e quantidade disponível) e consulta de exemplares disponíveis.
* **Gestão de Leitores:** Cadastro de usuários com validação de matrícula única.
* **Controle de Empréstimos:**
  * Registro de empréstimo vinculando um leitor a um livro disponível.
  * Baixa automática no estoque do livro.
  * Simulação de passagem de tempo (9 dias) para testes de atraso.
* **Devolução e Multas:**
  * Baixa de empréstimos ativos e reposição no estoque.
  * Cálculo automático de multa para devoluções fora do prazo.
* **Consultas e Relatórios:**
  * Listagem de livros disponíveis e emprestados.
  * Consulta de leitores com pendências de devolução.
  * Relatório geral com totais de livros, leitores e status dos empréstimos (ativos e finalizados).

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x** (Biblioteca padrão `datetime` e `sqlite3`)
* **SQLite** (Armazenamento local leve e sem necessidade de servidor dedicado)

---

## 🏗️ Arquitetura do Sistema

O projeto é estruturado sob o paradigma de **Orientação a Objetos**, dividido em quatro classes principais:

1. **`Livro`**: Representa uma obra do acervo. Controla a quantidade disponível através dos métodos `emprestar()` e `devolver()`.
2. **`Leitor`**: Representa o usuário da biblioteca, armazenando `nome`, `matricula` e o histórico de seus `emprestimos`.
3. **`Emprestimo`**: Gerencia a transação entre `Livro` e `Leitor`. Controla datas, prazo, status de devolução, simulação de dias (`simular_dias()`) e cálculo de penalidades (`calcular_multa()`).
4. **`Biblioteca`**: Classe controladora que centraliza as operações do sistema, validações de entrada, comunicação com o banco de dados e exibição de relatórios.

---

## 🗄️ Armazenamento Local (SQLite)

Para garantir que os dados não sejam perdidos ao encerrar o programa, o sistema utiliza um banco de dados local (`biblioteca.db`) gerado automaticamente na raiz do projeto.

### Estrutura das Tabelas

* **`livros`**
  * `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
  * `titulo` (TEXT, NOT NULL)
  * `autor` (TEXT, NOT NULL)
  * `quantidade` (INTEGER, NOT NULL)

* **`leitores`**
  * `matricula` (TEXT, PRIMARY KEY)
  * `nome` (TEXT, NOT NULL)

* **`emprestimos`**
  * `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
  * `livro_id` (INTEGER, FOREIGN KEY -> `livros.id`)
  * `leitor_matricula` (TEXT, FOREIGN KEY -> `leitores.matricula`)
  * `data_emprestimo` (DATE, NOT NULL)
  * `dias_passados` (INTEGER, DEFAULT 0)
  * `prazo` (INTEGER, DEFAULT 7)
  * `devolvido` (BOOLEAN, DEFAULT 0)

---

## 📏 Regras de Negócio

* **Estoque:** Um livro só pode ser emprestado se sua quantidade disponível for maior que `0`.
* **Matrícula Única:** Não é permitido cadastrar dois leitores com o mesmo número de matrícula.
* **Prazo de Empréstimo:** O prazo padrão para devolução é de **7 dias**.
* **Cálculo de Multa:** Caso `dias_passados` ultrapasse o `prazo` de 7 dias, é cobrada uma multa de **R$ 2,00 por dia de atraso**.

---

## 💻 Como Executar

1. Certifique-se de ter o **Python 3** instalado em sua máquina.
2. Clone ou baixe o arquivo principal do projeto (ex: `main.py`).
3. Abra o terminal na pasta do projeto e execute:

```bash
python main.py
```

4. Utilize o menu interativo digitando o número correspondente à operação desejada:

```text
========== BIBLIOTECA ==========
1 - Cadastrar livro
2 - Cadastrar leitor
3 - Realizar empréstimo
4 - Registrar devolução
5 - Consultar livros disponíveis
6 - Consultar livros emprestados
7 - Consultar leitores com pendências
8 - Gerar relatório
0 - Sair
```