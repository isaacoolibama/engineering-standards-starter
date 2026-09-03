> Origem: `delivery/ci-cd.md` — Engineering Standards

# CI/CD

Fontes: [OpenSSF](https://openssf.org/), [SLSA](https://slsa.dev/).

## Pipeline mínimo

Todo projeto SHOULD ter, proporcional ao risco:

1. build reprodutível;
2. lint e formatação;
3. testes automatizados;
4. verificação de segurança (dependências e segredos);
5. geração e publicação de artefato versionado.

- O pipeline MUST falhar de forma visível; MUST NOT ter etapa crítica em modo apenas informativo.
- Build MUST ser reproduzível a partir do repositório, sem passo manual não documentado.
- Dependências MUST vir de lockfile.

## Segurança do pipeline

- Segredos MUST vir do cofre do provedor; MUST NOT ficar em variáveis de texto plano no repositório.
- Ações/plugins de terceiros SHOULD ser fixados por versão imutável.
- Permissões do job MUST seguir menor privilégio.
- Pipelines de PR de fork MUST NOT ter acesso a segredos de produção.
- Scanner de segredos SHOULD rodar em todo push.

## Entrega

- Deploy MUST ser automatizado e repetível.
- Promoção entre ambientes SHOULD usar o mesmo artefato, mudando apenas configuração.
- Toda entrega MUST ter procedimento de rollback conhecido.
- Migrations de banco MUST ter ordem definida em relação ao deploy da aplicação.
