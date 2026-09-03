> Origem: `stacks/java-sankhya/security.md` — Engineering Standards

# Segurança Java Sankhya

- MUST respeitar permissões e controles nativos da plataforma.
- Ações modernas SHOULD manter controle de acesso habilitado quando suportado.
- MUST validar parâmetros de ações/serviços no backend.
- MUST usar bind/parametrização em SQL.
- MUST NOT expor credenciais no código-fonte.
- Integrações externas MUST definir armazenamento seguro de credenciais.
- SHOULD aplicar menor privilégio para usuários/conexões de integração.
- MUST NOT confiar que esconder botão/tela constitui autorização.
