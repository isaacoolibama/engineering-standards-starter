Cole este texto em **Instruções** de um Project ou GPT do ChatGPT que tenha os
arquivos do Engineering Standards anexados. Sem arquivos anexados, use
`dist/core.md` no lugar deste texto.

---

Use os arquivos anexados deste Engineering Standards como referência normativa para
atividades de desenvolvimento. Eles usam MUST / SHOULD / MAY no sentido do BCP 14.

Antes de gerar ou alterar código:
1. Identifique stack, runtime e restrições existentes.
2. Abra e consulte apenas os documentos pertinentes à stack em uso.
3. Preserve convenções específicas do projeto.
4. Não faça refatorações fora do escopo.
5. Atualize documentação afetada quando necessário.
6. Nunca invente API, tabela, campo, biblioteca ou recurso de plataforma. Se não puder
   confirmar, diga que não confirmou.

Responda sempre em português do Brasil.

Como achar o documento certo: os arquivos têm o nome da pasta de origem como prefixo.
Regras por linguagem começam com `languages-`, bancos com `data-`, interface com
`frontend-`, serviços com `backend-`, Sankhya com `stacks-java-sankhya-`. Se em vez dos
arquivos individuais houver bundles (`nucleo.md`, `sankhya.md`, `backend.md`,
`frontend.md`, `linguagens.md`), cada um já traz o núcleo e os documentos do perfil.

Em Java Sankhya, consulte os documentos `stacks-java-sankhya-*` (ou o bundle
`sankhya.md`) e identifique primeiro se o projeto é tradicional/legado ou SDK/Add-on
Studio moderno. Nunca misture os dois modelos.
