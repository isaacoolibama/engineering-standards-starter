> Origem: `frontend/nextjs.md` — Engineering Standards

# Next.js

Fonte primária: [documentação da versão instalada](https://nextjs.org/docs). Regras variam entre App Router e Pages Router — MUST identificar qual está em uso.

## Fronteira servidor/cliente

- MUST tratar a fronteira como fronteira de segurança: código de servidor pode acessar segredos, código de cliente não.
- `"use client"` SHOULD ser aplicado o mais abaixo possível na árvore.
- Variáveis com prefixo `NEXT_PUBLIC_` MUST ser consideradas públicas; MUST NOT conter segredo.
- Server Actions MUST validar entrada e autorização no servidor — serem chamadas do cliente não as torna confiáveis.
- MUST NOT vazar objetos de dados internos para o cliente sem seleção de campos.

## Dados e cache

- Estratégia de cache e revalidação MUST ser explícita e documentada.
- Dados por usuário MUST NOT ser servidos de cache compartilhado.
- SHOULD tratar erro e estado de carregamento com os mecanismos do framework.

## Qualidade

- SHOULD usar o componente de imagem e de fonte do framework em vez de tags brutas.
- SHOULD medir Core Web Vitals antes de otimizar.
- Aplicar também react.md (ver `frontend-react.md`) e typescript.md (ver `languages-typescript.md`).
