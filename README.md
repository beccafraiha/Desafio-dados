# 📦 LogTrack Pro — Dashboard de Monitoramento Logístico

Sistema inteligente de monitoramento de entregas com tema escuro e visual moderno.

---

## Arquivos do projeto

| Arquivo | Descrição |
|---|---|
| `app.py` | Código principal do dashboard (Streamlit) |
| `dados2.csv` | Base de dados com 50 entregas de exemplo |
| `requirements.txt` | Dependências do projeto |

---

## Como executar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Acesse no navegador: `http://localhost:8501`

---

## Como publicar (link público gratuito)

### Passo 1 — GitHub
1. Acesse [github.com](https://github.com) e faça login
2. Clique em **"+"** → **"New repository"**
3. Nome sugerido: `logtrack-pro`
4. Marque como **Public**
5. Clique em **"Create repository"**
6. Clique em **"Add file"** → **"Upload files"**
7. Envie os 3 arquivos: `app.py`, `dados2.csv`, `requirements.txt`
8. Clique em **"Commit changes"**

### Passo 2 — Streamlit Community Cloud
1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **"Sign up"** → **"Continue with GitHub"**
3. Clique em **"New app"**
4. Preencha:
   - **Repository:** `seu-usuario/logtrack-pro`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Clique em **"Deploy!"**

Seu link público será gerado no formato:
```
https://logtrack-pro-seu-usuario.streamlit.app
```

> ✅ Link permanente, sem login, 100% gratuito.

---

## Como substituir os dados reais

Edite o arquivo `dados2.csv` mantendo as mesmas colunas:

```
ID Entrega, Data, Região, Transportadora, Prazo Previsto, Data Real, Dias de Atraso, Status
```

- **Data** e **Prazo Previsto** e **Data Real** no formato `AAAA-MM-DD`
- **Status** deve ser exatamente `No Prazo` ou `Atrasado`
- **Dias de Atraso** deve ser `0` para entregas no prazo

---

## Sistema de alertas (semáforo)

| Percentual de atraso | Status |
|---|---|
| Até 5% | 🟢 OK |
| De 5% a 15% | 🟠 Atenção |
| Acima de 15% | 🔴 Crítico |

---

## Apresentação do projeto

| Campo | Informação |
|---|---|
| **Nome** | LogTrack Pro |
| **Objetivo** | Monitorar atrasos em entregas por região e transportadora |
| **Ferramenta** | Python + Streamlit + Plotly |
| **Tema visual** | Escuro com destaque em roxo/violeta |
| **Dados** | 50 entregas, 5 regiões, 4 transportadoras |
| **Link** | *(inserir após o deploy)* |

---

<p align="center">
  <small>LogTrack Pro — Projeto Acadêmico · Dashboard Inteligente de Monitoramento Logístico</small>
</p>
