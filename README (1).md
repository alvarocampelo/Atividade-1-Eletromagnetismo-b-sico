# Atividade 1 – Eletromagnetismo Básico (TI0166)

**Universidade Federal do Ceará – Departamento de Engenharia de Teleinformática**  
Prof. João Batista

Resolução analítica e computacional da Atividade 1, baseada na Lista de Exercícios 2.

---

## Estrutura do repositório

```
.
├── utils.py               # Funções compartilhadas (Lei de Coulomb, visualização)
├── problema_01.py         # Força e campo de duas cargas sobre Q em P(1,−3,7)
├── problema_06.py         # Carga total com densidade volumétrica (integração tripla)
├── problema_07.py         # Força resultante sobre Q3 em sistema de três cargas
├── problema_09.py         # Cargas totais: linha, cilindro e esfera
├── problema_10.py         # Campo em P(0,0,6) de quatro cargas nos vértices do quadrado
├── problema_12.py         # Campo geral e valor em P(1,1,2) de Q=−10 nC na origem
├── questao_02_linha.py    # Linha finita: analítico vs. N cargas pontuais
└── questao_03_anel.py     # Anel de carga: analítico vs. N cargas pontuais
```

---

## Dependências

```bash
pip install numpy scipy plotly
```

Python ≥ 3.8 recomendado.

---

## Como executar

Cada arquivo é independente e pode ser executado diretamente:

```bash
python problema_01.py
python problema_06.py
python problema_07.py
python problema_09.py
python problema_10.py
python problema_12.py
python questao_02_linha.py
python questao_03_anel.py
```

> **Nota:** `questao_03_anel.py` importa funções de `questao_02_linha.py`
> para a comparação final. Ambos devem estar no mesmo diretório.

---

## Resumo dos problemas

| Arquivo | Problema | Tema |
|---|---|---|
| `problema_01.py` | Lista 2 – Q1 | Força e campo de cargas pontuais |
| `problema_06.py` | Lista 2 – Q6 | Integração tripla em esféricas |
| `problema_07.py` | Lista 2 – Q7 | Superposição de forças (3 cargas) |
| `problema_09.py` | Lista 2 – Q9 | Cargas totais (linha, superfície, volume) |
| `problema_10.py` | Lista 2 – Q10 | Campo de 4 cargas nos vértices |
| `problema_12.py` | Lista 2 – Q12 | Campo geral de carga pontual |
| `questao_02_linha.py` | Atividade 1 – Q2 | Linha finita: analítico × N pontos |
| `questao_03_anel.py` | Atividade 1 – Q3 | Anel: analítico × N pontos + análise O(N⁻²) |

---

## Destaques técnicos

- **`utils.py`** centraliza `calculate_force_on_charge`, `electric_field`,
  `normalize_vector` e `add_vector_arrow`, seguindo a estrutura do notebook
  Colab disponibilizado pelo professor.
- Todos os problemas de cargas pontuais geram **gráficos 3D interativos**
  com `plotly`, incluindo ponta de seta (`go.Cone`) para vetores de força/campo.
- A convergência das questões 2 e 3 é exibida em dois gráficos:
  valor de E vs N e erro relativo em escala logarítmica.
- A análise log-log da Questão 3 confirma ordem **O(N⁻²)** (quadratura
  trapezoidal para funções periódicas suaves).

---

## Recursos auxiliares

- Notebook Colab do professor:  
  <https://colab.research.google.com/drive/1eRm3435ruglRhfesoj5e_6m6Tw9q1uRq>
- Material de ensino UFC:  
  <https://pettelecom.ufc.br/pt/notebooks-de-ensino/>
