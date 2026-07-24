# Letra da Lei

A Letra da Lei traz o acervo jurídico brasileiro para o Claude: **legislação** e **jurisprudência**, com texto autoritativo em nível de artigo/precedente, verificação de vigência e fontes verificáveis no Planalto. Sobre essa base de pesquisa, o plugin também **redige peças processuais** com fundamentação verificada dispositivo por dispositivo.

## Pré-requisito

O servidor MCP **`letra-da-lei`** (`https://mcp.letradalei.com/mcp`) deve estar conectado — autenticação via **OAuth** (login no primeiro uso). As skills verificam a conexão antes de operar e nunca respondem de memória.

## Ferramentas do MCP (grupo · operação)

| Ferramenta | O que faz |
|---|---|
| `acervo · listar` | Descobre a cobertura — áreas e leis (`dominio: "legislacao"`) ou tribunais/tipos/eficácia (`dominio: "jurisprudencia"`). |
| `legislacao-federal · buscar_artigos` | Busca semântica de artigos; retorna `texto`, `citacao`, `situacao`, `source_url`. |
| `legislacao-federal · explorar_contexto` | Navega o sumário da lei e as relações de um artigo (`cita`/`citado_por`/`altera`). |
| `acervo · consultar` | Texto **integral** (não truncado) de artigos ou precedentes. |
| `jurisprudencia-federal · buscar_precedentes` | Súmulas, temas, OJs e acórdãos do STF/STJ/TST/CARF. |
| `jurisprudencia-federal · buscar_vinculantes` | Só precedentes vinculantes (art. 927 CPC). |
| `jurisprudencia-estadual · buscar_vinculantes` | IRDRs dos TJs (parâmetro `localidade` obrigatório). |
| `acervo · reclame_aqui` | Registra lacunas/erros do acervo para a equipe da Letra da Lei. |

Todas retornam `situacao` (vigência) e `is_truncated` — confira antes de citar.

## Skills

| Skill | Faz |
|---|---|
| `/letra-da-lei:pesquisa` | **Skill-base.** Pesquisa e cita legislação e jurisprudência pelo MCP, com verificação de vigência e texto integral. As demais skills a carregam. |
| `/letra-da-lei:peticao` | Redige petição inicial (CPC art. 319) com fundamentação verificada. |
| `/letra-da-lei:contestacao` | Redige contestação cível (CPC arts. 335–342), preliminares, mérito e eventual reconvenção. |
| `/letra-da-lei:fundamentacao` | Estrutura a fundamentação de sentença/decisão com checagem do art. 489, § 1º do CPC. |
| `/letra-da-lei:analise` | Diagnostica a fase processual e redige a peça cabível (réplica, recursos, cumprimento, embargos, ações autônomas etc.). |

As skills de redação produzem **rascunhos revisáveis**, não peças prontas: quem assina, decide estratégia e protocola é o(a) advogado(a) ou magistrado(a) habilitado(a).

## Quando usar / não usar

- **Usar:** consultar o que a lei diz, localizar artigo/precedente, verificar uma citação, ou redigir uma peça com base legal verificada.
- **Não usar:** aconselhamento jurídico ou prognóstico — o plugin recupera e estrutura fontes; a aplicação aos fatos é do(a) profissional habilitado(a). Legislação estadual/municipal e normas infralegais estão fora do acervo.

### Links

- **Site:** https://letradalei.com
- **Documentação:** https://letradalei.com/docs
- **Suporte:** suporte@letradalei.com
