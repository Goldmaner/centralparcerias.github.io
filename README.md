# Central de Parcerias DDH

> Plataforma web unificada de apoio à gestão de parcerias entre OSCs e Unidades Gestoras públicas, referenciada na Lei Federal n.º 13.019/2014.

🔗 **Acesso direto:** [https://goldmaner.github.io](https://goldmaner.github.io)

---

## Estrutura do sistema

A Central de Parcerias é uma **PWA (Progressive Web App)** composta por módulos independentes, organizados por perfil de usuário: **Sou OSC** e **Sou Pessoa Gestora**.

```
index.html            ← Hub de navegação (landing page)
demonstrativo.html    ← Demonstrativo de Aferição (perfil OSC)
oficio.html           ← Formulário de Ofício de Solicitação (perfil OSC)
relatorio.html        ← Relatório de Execução Financeira (perfil OSC)
encaminhamento.html   ← Encaminhamento ao Setor Competente (perfil Gestora)
sw.js                 ← Service Worker (suporte offline)
manifest.json         ← Manifesto PWA
```

---

## Módulos

### 📊 Demonstrativo de Aferição — `demonstrativo.html`

Calcula automaticamente o **PA (Percentual Acumulado)** de remanejamento orçamentário mês a mês, indicando se a execução está dentro do limite de autonomia de **15% sobre o VTP** (Valor Total da Parceria).

**Abas:**
| # | Nome | Descrição |
|---|------|-----------|
| 1 | Instruções | Guia de uso do módulo |
| 2 | Cabeçalho | Dados da OSC, projeto, VTP, datas e valores |
| 3 | Conciliação Bancária | Em desenvolvimento |
| 4 | Previsto | Plano orçamentário aprovado, por item e mês |
| 5 | Executado | Valores efetivamente gastos; destaca extrapolações |
| 6 | % de Alteração | PRA por célula e PA total com semáforo de 15% |

**Funcionalidades:**
- Colar planilha do Excel diretamente na tabela (Ctrl+V)
- Mover, inserir e remover linhas de despesa
- Exportar PDF por seção (divisão automática a cada 8 meses)
- Exportar CSV (3 arquivos: Previsto, Executado, % Alteração)
- Salvar projeto como `.daf.json` e recarregar
- Auto-save silencioso no navegador (localStorage)
- Atalhos: `Ctrl+S` salvar, `Ctrl+O` abrir

---

### 📝 Formulário de Ofício — `oficio.html`

Gera o **Ofício de Solicitação de Alterações Orçamentárias** preenchido pela OSC para envio à Unidade Gestora.

**Funcionalidades:**
- Identificação automática via dados do Demonstrativo (localStorage compartilhado)
- 27 tipos de alteração com checkboxes
- Campos de Identificação, Demarcação, Fundamentação e Assinatura
- Exportar como PDF imprimível (A4 retrato, layout de ofício com timbre)
- Auto-save no navegador

---

### 📅 Relatório de Execução Financeira — `relatorio.html`

Módulo em construção para geração periódica de relatórios de execução físico-financeira da parceria.

**Aba 1 — Dados Gerais (disponível):**

| Campo | Formato |
|-------|---------|
| Número do Termo | Texto livre |
| CNPJ da OSC | Máscara XX.XXX.XXX/XXXX-XX |
| Nome da Organização | Texto livre |
| Nome do Projeto | Texto livre |
| Data de Início / Encerramento | Seletor de data |
| Valor Total do Projeto | Máscara monetária R$ |
| Valor Repassado | Máscara monetária R$ |
| Conta Específica | Texto livre (banco / agência / conta) |
| Endereço do Projeto | Texto livre |

Salva como `.ref.json`; auto-save no navegador.

**Próximas abas (em desenvolvimento):**
- Orçamento Anual
- Cronograma de Metas
- Conciliação Bancária

---

### 📋 Encaminhamento ao Setor Competente — `encaminhamento.html`

Ferramenta para a **Pessoa Gestora** gerar o bloco de HTML formatado para colar no sistema SEI, com o encaminhamento formal da solicitação da OSC.

**Funcionalidades:**
- 30 tipos de alteração (checkboxes)
- Seção de Demarcação (texto livre)
- Seção de Fundamentação — aparece automaticamente apenas quando **Prorrogação de Vigência** está marcada
- Botão "📋 Copiar HTML para SEI" — gera código HTML pronto para colar no editor do SEI
- Preview do documento e do código gerado
- Auto-save no navegador

---

## Tecnologia

| Item | Detalhe |
|------|---------|
| Stack | HTML + CSS + JavaScript ES2020 puro |
| Dependências externas | **nenhuma** |
| Hospedagem | GitHub Pages (gratuito, HTTPS automático) |
| Offline | Service Worker — estratégia network-first |
| Instalação | PWA — instala direto do navegador (Chrome/Edge) |
| Persistência local | `localStorage` por módulo |
| Formato de arquivo | `.daf.json` (Demonstrativo), `.ref.json` (Relatório) |

---

## Desenvolvimento local

```bash
# Clone
git clone https://github.com/Goldmaner/goldmaner.github.io.git
cd goldmaner.github.io

# Servidor local sem cache (recomendado)
python iniciar_servidor.py
# acesse http://localhost:8899
```

---

## Licença

Uso interno — Gestão de Parcerias OSC / DDH / FAF.
