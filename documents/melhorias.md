# Sugestões de Melhorias — Páginas de Gestão de Parcerias

> Central de Parcerias — Departamento de Direitos Humanos / SMDHC  
> Última atualização: maio/2026

---

## 1. Melhorias comuns a ambas as páginas (Visita Técnica e Monitoramento e Avaliação)

### 1.1 Validação antes de exportar/salvar
**Problema atual:** O usuário pode exportar o PDF ou salvar o JSON com campos obrigatórios em branco, gerando documentos incompletos.  
**Sugestão:** Antes de `window.print()` e do download JSON, verificar se os campos marcados com `*` estão preenchidos. Exibir um resumo dos campos vazios em um banner vermelho, com scroll automático até o primeiro campo faltante.

### 1.2 Indicador de progresso de preenchimento
**Problema atual:** Não há feedback visual de quanto do formulário já foi preenchido.  
**Sugestão:** Adicionar uma barra de progresso no topo (ex.: "Seções preenchidas: 3/9") que atualiza conforme o usuário preenche os campos obrigatórios. Pode ser uma barra simples com `<progress>` ou ícones de check por seção.

### 1.3 Pré-preenchimento de dados recorrentes
**Problema atual:** A pessoa gestora precisa redigitar o próprio nome, RF e e-mail a cada novo relatório.  
**Sugestão:** Adicionar uma seção de "Perfil da Pessoa Gestora" acessível pelo painel, que salva nome, RF e e-mail no `localStorage` do perfil gestor. As páginas de relatório verificam esse perfil e preenchem os campos automaticamente.

### 1.4 Histórico de relatórios
**Problema atual:** Cada relatório é um arquivo independente, sem registro de quais já foram gerados.  
**Sugestão:** Criar um índice local (no `localStorage`) que lista os relatórios abertos/salvos, com data, OSC, tipo e nome do arquivo. Exibir no painel como um painel "Relatórios recentes".

### 1.5 Layout de impressão / PDF melhorado
**Problema atual:** O `window.print()` gera o PDF com a formatação de tela, podendo cortar conteúdo.  
**Sugestão:**
- Adicionar `@media print` específico para cada página, forçando layout em coluna única e removendo bordas e sombras.
- Incluir cabeçalho de impressão com logo (texto) da Central de Parcerias, número do documento e data de geração.
- Numerar as páginas automaticamente com CSS `@page { @bottom-right { content: counter(page); } }`.

### 1.6 Tooltips explicativos nos campos
**Problema atual:** Campos como "Período avaliado (mês/semestre)" ou "RF da pessoa gestora" podem gerar dúvidas.  
**Sugestão:** Adicionar um ícone `ℹ️` ao lado do rótulo com tooltip ao passar o mouse (`title=""` ou um componente CSS puro), explicando brevemente o que deve ser preenchido.

### 1.7 Auto-save com indicação visual de tempo
**Problema atual:** O auto-save acontece silenciosamente.  
**Sugestão:** Exibir na status bar o horário do último auto-save (ex.: "Rascunho salvo às 14h32") para dar confiança ao usuário.

### 1.8 Botão "Novo relatório" com confirmação
**Problema atual:** Para iniciar um novo relatório, o usuário precisa usar o botão "Limpar", que destrói os dados sem criar backup.  
**Sugestão:** Renomear para "Novo Relatório" e, antes de limpar, oferecer download do rascunho atual como JSON automaticamente.

---

## 2. Melhorias específicas — Relatório de Visita Técnica (`visita_tecnica.html`)

### 2.1 Campo "Tipo de visita"
**Sugestão:** Adicionar campo select com as opções: "Visita de acompanhamento", "Visita de monitoramento", "Visita emergencial", "Primeira visita". Ajuda na categorização dos relatórios.

### 2.2 Checklist de documentos verificados durante a visita
**Sugestão:** Adicionar uma seção de checklist com documentos comuns verificados em campo (ex.: folhas de frequência, contratos de RH, notas fiscais), usando checkboxes. Cada item marcado pode gerar uma linha automática na seção de observações.

### 2.3 Registro fotográfico (descrição)
**Sugestão:** Adicionar campo textarea "Registro de situações observadas / descrição de evidências visuais" — substitui o upload de fotos (que não é viável em HTML estático) mas permite documentar o que foi visto.

### 2.4 Campo "Número de participantes/beneficiários verificados"
**Sugestão:** Incluir campo numérico para registro do número de beneficiários/participantes atendidos verificado durante a visita, com campo de observação sobre eventuais divergências com o plano de trabalho.

### 2.5 Área de assinatura digital
**Sugestão:** Adicionar ao final da página (visível apenas na impressão) um bloco de assinatura: "Pessoa Gestora: _________________ RF: _____  Data: _____" e "Responsável pela OSC: _________________ CPF: _____". Facilita a impressão e assinatura manual antes do SEI.

---

## 3. Melhorias específicas — Relatório de Monitoramento e Avaliação (`monitoramento_avaliacao.html`)

### 3.1 Cálculo automático de saldo e alertas de inconsistência
**Status atual:** O saldo (Repassado − Utilizado − Devolução) já é calculado automaticamente.  
**Melhoria:** Adicionar alerta visual quando o saldo calculado for negativo (indicando possível inconsistência nos valores) ou quando o valor utilizado for maior que o total da parceria.

### 3.2 Campo "Número de metas atingidas" vs "Número de metas previstas"
**Sugestão:** Expandir a seção 4 para registrar, além do número total de metas, o número de metas efetivamente atingidas. Calcular automaticamente o percentual de cumprimento (ex.: "3 de 5 metas atingidas = 60%") com indicador visual.

### 3.3 Linha do tempo de monitoramento
**Sugestão:** Exibir na seção 1 um resumo visual da duração da parceria (barra com data início → data término + posição do período avaliado), ajudando a contextualizar o relatório dentro do ciclo da parceria.

### 3.4 Vinculação ao relatório de Visita Técnica anterior
**Sugestão:** Adicionar campo "Relatório de Visita Técnica de referência" (texto livre ou upload do JSON) para que o relatório de monitoramento documente a relação com eventuais visitas realizadas no período.

### 3.5 Seção de comparativo entre períodos
**Sugestão:** Para relatórios a partir do 2º semestre, adicionar campo "Observações comparativas em relação ao período anterior" — facilita a análise evolutiva da parceria.

### 3.6 Melhora no print da seção de Recursos
**Sugestão:** Na impressão, exibir os valores de recursos em formato de tabela (Descrição | Valor), com linha de total e saldo, para facilitar leitura e conferência.

---

## 4. Melhorias de acessibilidade (ambas as páginas)

- Adicionar `aria-label` nos campos de rádio e checkbox para leitores de tela.
- Garantir contraste mínimo 4.5:1 nos textos sobre fundo colorido (ex.: labels em fundos azuis).
- Adicionar `focusable` keyboard navigation nos cards da landing page.
- Usar `<fieldset>` + `<legend>` para agrupar radios, seguindo WAI-ARIA.

---

## 5. Melhorias de infraestrutura (servidor e PWA)

- **Porta configurável:** Tornar a porta `8899` um argumento de linha de comando (`python iniciar_servidor.py --porta 9000`).
- **Compressão gzip:** Adicionar suporte a `Accept-Encoding: gzip` no servidor para arquivos estáticos grandes.
- **Modo offline completo:** Registrar todos os assets (CSS inline já está incluso por ser em-linha, mas verificar se `manifest.json` e ícones SVG estão no SW).
- **Versão no rodapé:** Exibir a versão do cache do SW no footer da landing page (`central-parcerias-v6`) para facilitar debug em campo.

---

## 6. Melhorias específicas — Parecer Técnico Conclusivo (`parecer_tecnico.html`)

### 6.1 Geração do texto final formatado
**Problema atual:** O formulário coleta os dados, mas não gera automaticamente o texto corrido no formato exigido pelo SEI/DOC-SP.  
**Sugestão:** Adicionar botão "Gerar Minuta" que monta o texto completo do parecer em uma `<div>` oculta, formatada para impressão, usando os dados preenchidos nos campos — incluindo os blocos exatos do modelo da Portaria (ex.: "Conforme Despacho Autorizatório (SEI XXXXXXXX), publicado..."). Isso elimina o retrabalho de copiar e colar.

### 6.2 Vinculação com relatórios anteriores
**Problema atual:** O parecer é preenchido isoladamente, sem referência aos relatórios de monitoramento e visita técnica já salvos.  
**Sugestão:** Adicionar campo "Importar dados de relatório" (upload de JSON dos relatórios de monitoramento ou visita técnica). O sistema pré-preenche automaticamente OSC, projeto, vigência, valor total, gestora e referências SEI, evitando retrabalho e inconsistências.

### 6.3 Cálculo automático do valor a devolver
**Problema atual:** O campo "Valor a Devolver" é livre, sem base de cálculo.  
**Sugestão:** Importar os valores de repasse, utilização e devolução do relatório de monitoramento. Calcular automaticamente o saldo e sugerir como valor a devolver ao erário, exibindo o memória de cálculo (Repassado − Utilizado − Devolução prévia = Saldo a devolver).

### 6.4 Seleção de resultado com preview do texto legal
**Problema atual:** O usuário seleciona "Aprovação / Ressalvas / Rejeição" mas não vê o texto legal correspondente.  
**Sugestão:** Ao selecionar o resultado, exibir em destaque o texto exato do inciso aplicável do Art. 76 da Portaria 021, para que a pessoa gestora confirme que o enquadramento está correto antes de finalizar.

### 6.5 Checklist de completude antes de exportar
**Problema atual:** O parecer pode ser exportado incompleto sem alertas.  
**Sugestão:** Antes do `window.print()`, verificar os campos críticos obrigatórios — resultado da análise, alcance das metas, forma de execução, análise dos resultados e localização dos documentos no SEI — e exibir lista dos itens faltantes com scroll automático.

### 6.6 Controle de versão do parecer
**Problema atual:** Não há distinção entre rascunho e versão final do parecer.  
**Sugestão:** Adicionar campo "Status do Parecer" (Rascunho / Em revisão / Versão final) e, quando "Versão final", registrar data/hora de finalização no JSON. Exibir o status em destaque no cabeçalho de impressão.

### 6.7 Campo de observações para o encaminhamento à OSC
**Problema atual:** O modelo prevê um ofício de encaminhamento à OSC (Art. 79), mas o formulário não contempla esse texto.  
**Sugestão:** Adicionar seção "9. Texto de Encaminhamento à OSC" (opcional/colapsável) com texto padrão pré-preenchido ("Encaminho o Parecer Técnico Conclusivo...") e campo para complementar, facilitando a elaboração do ofício SEI.

### 6.8 Campos de metas com percentual calculado
**Problema atual:** Os campos "Alcance das Metas" são apenas selects qualitativos.  
**Sugestão:** Adicionar campos numéricos opcionais "Metas previstas" e "Metas atingidas" com cálculo automático do percentual (ex.: "3 de 5 = 60%"), tornando a análise mais objetiva e rastreável.

---

## 7. Melhorias — Checklist de Conferência de Prestação de Contas (`checklist_prestacao_contas.html`)

### 7.1 Protocolo numerado de conferência
**Problema atual:** O checklist não gera um número de protocolo, dificultando o rastreamento das análises.  
**Sugestão:** Gerar automaticamente um número de protocolo no formato `CHECK-{ANO}-{SEQ}` (sequencial por localStorage), exibido no cabeçalho e no e-mail gerado, permitindo que a OSC faça referência ao número nas suas respostas.

### 7.2 Histórico de conferências por OSC
**Problema atual:** Cada checklist é independente; não é possível visualizar o histórico de análises de uma OSC.  
**Sugestão:** Criar um índice local (localStorage) que registra os checklists salvos por OSC, com data, período, resultado e nome do arquivo JSON. Exibir no painel da gestora como "Conferências recentes".

### 7.3 Cálculo de prazo de resposta da OSC
**Problema atual:** O campo de prazo é apenas uma data avulsa, sem cálculo automático.  
**Sugestão:** Calcular automaticamente a data-limite de 5 dias úteis a partir da data de recebimento dos documentos (Art. 67 da Portaria 021), exibindo a data calculada e um alerta se o prazo estiver próximo do vencimento.

### 7.4 Rastreamento do status do recurso (Art. 64)
**Problema atual:** Não há campo para acompanhar se a OSC apresentou recurso à decisão desfavorável.  
**Sugestão:** Adicionar seção "Recurso da OSC" com campos: data do recurso, conteúdo, posição da gestora (mantida/reformada) e, se mantida, encaminhamento à autoridade competente, com campos de prazo e resultado.

### 7.5 Vinculação com relatório de monitoramento
**Problema atual:** O checklist é preenchido isoladamente.  
**Sugestão:** Adicionar campo "Importar dados de relatório de monitoramento" (upload do JSON do Relatório de Monitoramento e Avaliação). Pré-preencher automaticamente OSC, projeto, período e dados financeiros para conferência cruzada.

### 7.6 Exportação do e-mail em formato .eml
**Problema atual:** O e-mail gerado é apenas copiado para a área de transferência.  
**Sugestão:** Disponibilizar botão "Abrir no cliente de e-mail" usando `mailto:` com assunto e corpo pré-preenchidos, ou gerar link `data:` para download do arquivo `.eml`, facilitando o envio sem copiar e colar.

### 7.7 Assinatura configurável da gestora
**Problema atual:** A assinatura do e-mail gerado usa apenas o nome digitado no campo, sem bloco de assinatura completo.  
**Sugestão:** Integrar com o "Perfil da Pessoa Gestora" (melhoria 1.3) para incluir cargo, e-mail institucional e telefone na assinatura do e-mail gerado automaticamente.

---

## 8. Melhorias — Relatório de Execução do Objeto e Cumprimento de Metas (`relatorio_execucao_objeto.html`)

### 8.1 Upload de documentos (futuro — requer storage)
**Problema atual:** A OSC não consegue anexar documentos comprobatórios diretamente no sistema.  
**Sugestão futura:** Quando houver integração com Supabase Storage, adicionar upload de PDFs para notas fiscais, listas de presença, extratos e outros documentos comprobatórios, com link gerado para inclusão no processo SEI. Por enquanto, os campos de localização SEI são suficientes.

### 8.2 Modelo de e-mail de encaminhamento do relatório
**Problema atual:** Ao finalizar o relatório, a OSC não tem um modelo de e-mail para encaminhar à gestora.  
**Sugestão:** Adicionar botão "Gerar E-mail de Envio para SMDHC" com texto padrão informando o período de referência, a data de elaboração e os documentos anexados, pronto para copiar e enviar.

### 8.3 Validação de consistência financeira
**Problema atual:** A OSC pode declarar valores inconsistentes sem alerta.  
**Sugestão:** Alertar quando o Total Utilizado for maior que o Total Repassado, ou quando o saldo calculado for negativo, ou quando o total das rubricas na tabela de despesas divergir do campo "Total Utilizado".

### 8.4 Importação de dados do contrato/plano de trabalho
**Problema atual:** A OSC preenche manualmente os dados do instrumento a cada relatório.  
**Sugestão:** Permitir que a OSC carregue um arquivo JSON de "Dados do Contrato" (criado uma vez no painel) com OSC, CNPJ, instrumento, vigência e metas do plano de trabalho. O formulário pré-preenche automaticamente, reduzindo erros e retrabalho.

### 8.5 Indicador visual de completude antes de exportar
**Problema atual:** A OSC pode exportar o PDF sem preencher campos obrigatórios.  
**Sugestão:** Antes do `window.print()`, verificar os campos críticos (nome OSC, projeto, período, responsável, data, extratos bancários marcados) e exibir lista de itens pendentes com destaque visual.

### 8.6 Assinatura digital simplificada (hash)
**Problema atual:** O relatório não tem nenhum mecanismo de autenticidade.  
**Sugestão:** Ao finalizar, gerar um hash SHA-256 dos dados do formulário e incluí-lo no JSON salvo e no rodapé do PDF impresso. Isso não é assinatura jurídica, mas permite verificar que o PDF não foi alterado após a exportação.

