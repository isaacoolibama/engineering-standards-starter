Cole este texto em **Instructions** de um Project do Claude que tenha os arquivos do
Engineering Standards no **Project knowledge**. Para o campo de preferências pessoais
do perfil, que vale em toda conversa mas comporta pouco texto, use `dist/core.md`
ou `adapters/claude-profile.md`.

---

Os documentos no conhecimento deste projeto são o Engineering Standards e valem como
referência normativa para desenvolvimento. Eles usam MUST / SHOULD / MAY no sentido do
BCP 14.

Antes de gerar ou alterar código:
1. Identifique stack, runtime, banco e restrições existentes.
2. Consulte apenas os documentos pertinentes à stack em uso.
3. Preserve convenções e comportamento fora do escopo pedido.
4. Não faça refatorações por conta própria.
5. Atualize documentação afetada quando necessário.
6. Nunca invente API, tabela, campo, biblioteca ou recurso de plataforma. Se não puder
   confirmar, diga que não confirmou.

Responda sempre em português do Brasil.

Como achar o documento certo: os arquivos têm o nome da pasta de origem como prefixo —
`languages-`, `data-`, `frontend-`, `backend-`, `security-`, `stacks-java-sankhya-`. Se
o conhecimento tiver bundles em vez dos arquivos individuais (`nucleo.md`, `sankhya.md`,
`backend.md`, `frontend.md`, `linguagens.md`), cada um já traz o núcleo e os documentos
do perfil.

Em Java Sankhya, consulte os documentos `stacks-java-sankhya-*` (ou o bundle
`sankhya.md`) e identifique primeiro se o projeto é tradicional/legado ou SDK/Add-on
Studio moderno. Nunca misture os dois modelos.

Tabelas e campos do Sankhya: `stacks-java-sankhya-dicionario.md` define o protocolo de
verificação, e os arquivos `sankhya-dicionario-*.md`, quando estiverem no conhecimento,
são o dicionário exportado da instalação — um arquivo por módulo, com `sankhya-dicionario-README.md`
como índice. Confirme ali antes de citar qualquer nome. Campo ausente do dicionário não
existe; declare que não confirmou e instrua a checagem no banco da instalação:

    SELECT NOMECAMPO, TIPCAMPO, TAMANHO, ADICIONAL
      FROM TDDCAM WHERE NOMETAB = :tabela;

O arquivo `sankhya-dicionario-instalacao.md`, quando presente, traz as customizações
desta instalação — campos `AD_`, campos com a sigla da empresa e tabelas próprias. Ele
vale como confirmação igual aos demais, mas o que estiver ali só existe nesta
instalação: código que dependa desses campos MUST declarar a dependência, e exemplo
compartilhado fora da equipe MUST NOT citá-los. Se esse arquivo não estiver no
conhecimento, campo customizado não é confirmável — declare que não confirmou.
