# Especificações Técnicas — Páginas de Gestão de Parcerias

> Central de Parcerias — Departamento de Direitos Humanos / SMDHC  
> Portaria de referência: nº 021/SMDHC/2023  
> Última atualização: maio/2026

---

## 1. Visão geral do projeto

A **Central de Parcerias** é um conjunto de ferramentas offline-first para gestão de parcerias entre a SMDHC (Secretaria Municipal de Direitos Humanos e Cidadania) e OSCs (Organizações da Sociedade Civil). Funciona como uma PWA (Progressive Web App) servida por servidor local Python, sem dependência de banco de dados ou nuvem.

### 1.1 Stack técnica

| Camada | Tecnologia |
|--------|-----------|
| Servidor local | Python 3 — `http.server` com `ThreadingMixIn` |
| Frontend | HTML5 + CSS3 + JavaScript ES6 (vanilla, sem frameworks) |
| Armazenamento | `localStorage` (rascunhos) + download de `.json` (persistência) |
| Exportação | `window.print()` → PDF via diálogo do navegador |
| PWA | `manifest.json` + `sw.js` (Service Worker, network-first) |
| Porta | `8899` (configurável em `iniciar_servidor.py`) |

### 1.2 Estrutura de arquivos

```
DemonstrativoAfericaohtml/
├── index.html                     # Landing hub + app Demonstrativo de Aferição
├── sw.js                          # Service Worker PWA
├── manifest.json                  # Metadados PWA
├── iniciar_servidor.py            # Servidor local com hot reload
├── Pages/
│   ├── visita_tecnica.html        # Relatório de Visita Técnica
│   ├── monitoramento_avaliacao.html  # Relatório de Monitoramento e Avaliação
│   ├── demonstrativo.html         # Demonstrativo de Aferição (OSC)
│   ├── oficio.html                # Ofício de Alteração (OSC)
│   ├── relatorio.html             # Relatório de Execução Financeira (OSC)
│   └── encaminhamento.html        # Encaminhamento de Alteração (Gestor)
└── documents/
    ├── melhorias.md               # Sugestões de melhorias
    └── specs.md                   # Este arquivo
```

---

## 2. Servidor local (`iniciar_servidor.py`)

### 2.1 Comportamento

- Sobe na porta `8899` e abre o navegador automaticamente.
- Classe `NoCacheHandler` (herda `SimpleHTTPRequestHandler`) desabilita cache em todos os responses.
- Hot reload via polling `/__reload` a cada 1200ms: o servidor retorna um `version_stamp` (máximo `mtime` dos arquivos monitorados, cacheado por 2 segundos).
- O snippet de hot reload é injetado em todos os HTMLs servidos, antes de `</body>`.
- `ThreadingMixIn`: cada requisição roda em thread própria — elimina bloqueio por polling de hot reload.
- `allow_reuse_address = True`: evita erro "address already in use" ao reiniciar.

### 2.2 Extensões monitoradas para hot reload
`.html`, `.css`, `.js`, `.json`, `.md`

### 2.3 Como iniciar
```powershell
cd "c:\Users\Jefferson\OneDrive - rede.sp\Área de Trabalho\FAF\REF\DemonstrativoAfericaohtml"
python iniciar_servidor.py
```

---

## 3. Service Worker (`sw.js`)

### 3.1 Versão atual
`central-parcerias-v6`

### 3.2 Assets pré-cacheados (ASSETS)
- `./`
- `./index.html`
- `./manifest.json`
- `./Pages/visita_tecnica.html`
- `./Pages/monitoramento_avaliacao.html`

### 3.3 Estratégia de cache
**Network-first** para assets (CSS inline/JS inline não entram no cache de rede).  
**Navegações (`mode === 'navigate'`) são sempre bypassadas** — o SW nunca intercepta cliques em links, evitando que páginas antigas sejam servidas do cache.

### 3.4 Atualização automática
- O SW usa `skipWaiting()` durante a instalação.
- `index.html` e todas as páginas em `Pages/` chamam `reg.update()` a cada carregamento.
- Se há SW em estado `waiting`, é ativado imediatamente via `postMessage({ type: 'SKIP_WAITING' })`.
- Quando o SW troca de controlador (`controllerchange`), a página é recarregada automaticamente.

---

## 4. Especificação — Relatório de Visita Técnica (`Pages/visita_tecnica.html`)

### 4.1 Objetivo
Registrar e documentar visitas técnicas realizadas por Pessoas Gestoras às OSCs parceiras, conforme a Portaria nº 021/SMDHC/2023.

### 4.2 Seções do formulário

| # | Nome | Campos principais |
|---|------|-------------------|
| 1 | Informações da Parceria | Nome OSC, Área Técnica, Nome Projeto, Processo SEI, Instrumento, Nº Termo, Datas, Gestor(a), RF, Responsável OSC, CPF, E-mail OSC, Telefone, Período avaliado, Data/Horário visita |
| 2 | Supervisão Técnica | Infraestrutura (2 sub-questões com rádio + justificativa), Gestão Administrativa (2 sub-questões), Recursos Humanos (1 sub-questão) |
| 3 | Análise da Visita Técnica | Observações gerais, Recomendações, Parecer final |

### 4.3 Persistência
- **Auto-save:** `localStorage` — chave `visita_tecnica_autosave`
- **Exportação:** download `.json` via `Blob` + `URL.createObjectURL`
- **Importação:** `FileReader` + `JSON.parse`
- **PDF:** `window.print()` com estilos `@media print`

### 4.4 Navegação
- Botão "Painel Gestor" → `voltarPainel()` → `../index.html#gestor`
- Atalho `Ctrl+S` → salvar
- `beforeunload` → aviso se há alterações não salvas (`isDirty === true`)

### 4.5 Chave localStorage
```
visita_tecnica_autosave
```

---

## 5. Especificação — Relatório de Monitoramento e Avaliação (`Pages/monitoramento_avaliacao.html`)

### 5.1 Objetivo
Elaborar o Relatório Técnico de Monitoramento e Avaliação de parcerias entre SMDHC e OSCs, conforme Portaria nº 021/SMDHC/2023.

### 5.2 Seções do formulário

| # | Nome | Campos principais |
|---|------|-------------------|
| 1 | Identificação do Projeto | Checkbox "Último período", Processo SEI, Período avaliado (select), Nome OSC, Nome projeto, Área Técnica, Instrumento, Datas, Nº Termo, Nome/RF gestora, E-mail elaborador, Nome/CPF responsável OSC |
| 2 | Recursos | Valor total parceria, Valor repassado, Valor utilizado, Contrapartida, Devolução, Saldo calculado (readonly) |
| 3 | Adequações sob orientação | Textarea livre |
| 4 | Metas e impacto social | Número de metas, Rádio: REF solicitado? |
| 5 | Análise da pessoa gestora | 3 selects (Sim/Não/Parcialmente) + textarea discursiva |
| 6 | Participação de órgãos e entidades | Rádio Sim/Não + textarea condicional |
| 7 | Auditorias | Select Sim/Não + textarea condicional |
| 8 | Orientações, recomendações e advertências | 3 textareas independentes |
| 9 | Determinação de Glosa ou Retenção de Repasse | Checkboxes multi-seleção de motivos + textarea de detalhe |

### 5.3 Comportamentos especiais
- **Saldo calculado:** Campo readonly, atualizado automaticamente: `Repassado − Utilizado − Devolução`.
- **Seções condicionais:**
  - Seção 6 textarea: visível apenas se rádio "Houve participação?" = "Sim"
  - Seção 7 textarea: visível apenas se select "Foram realizadas auditorias?" = "Sim"
- **Período avaliado:** select com opções de semestres (2024–2026) e meses (2025–2026).

### 5.4 Estrutura do JSON salvo
```json
{
  "_version": 1,
  "_form": "monitoramento_avaliacao",
  "ultimoPeriodo": false,
  "processoSEI": "...",
  "periodoAvaliado": "1º Semestre / 2026",
  "nomeOSC": "...",
  "nomeProjeto": "...",
  "areaTecnica": "...",
  "instrumentoParceria": "Termo de Colaboração",
  "dataInicio": "YYYY-MM-DD",
  "dataTermino": "YYYY-MM-DD",
  "numeroTermo": "...",
  "nomeGestora": "...",
  "rfGestora": "...",
  "emailElaborador": "...",
  "nomeResponsavelOSC": "...",
  "cpfResponsavelOSC": "...",
  "valorTotalParceria": "...",
  "valorRepassado": "...",
  "valorUtilizado": "...",
  "valorContrapartida": "...",
  "valorDevolucao": "...",
  "adequacoes": "...",
  "numMetas": "0",
  "relExecFinanc": "Sim|Não|",
  "recursosAdequados": "Sim|Não|Parcialmente|",
  "itensAdquiridos": "Sim|Não|Parcialmente|",
  "equipeContratada": "Sim|Não|Parcialmente|",
  "analiseDiscursiva": "...",
  "participacaoOrgaos": "Sim|Não|",
  "orgaosDesc": "...",
  "auditoriasRealizadas": "Sim|Não|",
  "auditoriaDesc": "...",
  "orientacao": "...",
  "recomendacao": "...",
  "advertencia": "...",
  "glosaMotivos": ["Execução parcial do objeto"],
  "glosaSancao": "..."
}
```

### 5.5 Chave localStorage
```
monitoramento_avaliacao_autosave
```

### 5.6 Navegação
- Botão "Painel Gestor" → `voltarPainel()` → `../index.html#gestor`
- Atalho `Ctrl+S` → salvar
- `beforeunload` → aviso se `isDirty === true`

---

## 6. Padrões de desenvolvimento

### 6.1 CSS
- Variáveis de cor principal: `#0D47A1` (header), `#1565C0` (destaque), `#1E88E5` (interação)
- Todas as páginas usam CSS embutido no `<style>` do mesmo HTML (sem arquivos externos)
- Grid de formulário: `display: grid; grid-template-columns: 1fr 1fr; gap: 16px`
- Cards de seção: `border-left: 4px solid #1565C0` + `box-shadow`

### 6.2 JavaScript
- `'use strict'` em todos os scripts
- Sem frameworks ou bibliotecas externas
- `parseDecimal()` aceita formatos `1.234,56` (pt-BR) e `1234.56` (en-US)
- `markDirty()` / `clearDirty()` controlam o estado de edição não salva
- `autoSave()` chamado em todo `markDirty()`

### 6.3 Nomenclatura de arquivos JSON exportados
- Visita Técnica: `{nomeOSC}_visita_tecnica.json`
- Monitoramento: `{nomeOSC}_monitoramento_{periodo}.json`

---

## 7. Navegação entre páginas (Landing)

```
index.html (landing)
├── Sou OSC → landingOSC
│   ├── Demonstrativo de Aferição       → Pages/demonstrativo.html  (alias: Pages/demonstrativo.html via entrarComoOSC())
│   ├── Ofício de Alteração             → Pages/oficio.html
│   ├── Relatório de Execução Financeira → Pages/relatorio.html
│   └── Prestação de Contas             → (EM BREVE)
└── Sou Pessoa Gestora → landingGestor
    ├── Relatório de Visita Técnica      → Pages/visita_tecnica.html  ✅
    ├── Relatório de Monitoramento       → Pages/monitoramento_avaliacao.html  ✅
    ├── Encaminhamento de Alteração      → Pages/encaminhamento.html
    └── Parecer Técnico Conclusivo       → (EM BREVE)
```

---

## 8. Convenções de campos obrigatórios

Campos marcados com `*` são considerados obrigatórios para fins de completude do relatório.  
Atualmente a validação é apenas visual (nenhum `required` HTML está ativo para não bloquear saves parciais de rascunho).  
Ver [melhorias.md](melhorias.md) — item 1.1 para especificação de validação futura.
