# Política de segurança

## Versões suportadas

O branch `main` recebe correções de segurança. Commits antigos não recebem
backports garantidos.

## Reportar uma vulnerabilidade

Não abra uma issue pública. Use **Security → Report a vulnerability** neste
repositório para enviar o relato de forma privada.

Inclua o commit afetado, o impacto, os passos mínimos para reprodução e, se
possível, uma mitigação. O objetivo é confirmar o recebimento em até 3 dias
úteis e publicar uma avaliação inicial em até 7 dias úteis.

## Escopo sensível

A aplicação recebe planilhas e coordenadas enviadas pelo usuário e roda um
solver com limite de tempo. São especialmente relevantes relatos sobre:

- arquivos de entrada (CSV/XLSX) que travem o parser ou o solver, ou consumam
  memória sem limite;
- caminhos de arquivo controlados pelo usuário que leiam ou gravem fora de
  `data/`;
- exposição de dados de clientes carregados em uma sessão para outra sessão
  do Streamlit;
- dependências com vulnerabilidade conhecida (o Dependabot e o CodeQL cobrem
  o básico, mas relatos manuais são bem-vindos).

Não inclua planilhas reais de clientes no relato.
