# Engineering Standards — frontend

Interface web e desktop, com as linguagens que a acompanham.

## Núcleo

Responda sempre em português do Brasil.

Antes de escrever ou alterar código:
1. Identifique linguagem, framework, runtime, banco e as convenções já usadas no projeto.
2. Aplique somente as regras da stack em uso.
3. Não invente API, tabela, campo, biblioteca ou recurso de plataforma. Se não puder confirmar, diga que não confirmou.
4. Preserve o comportamento fora do escopo pedido; não refatore por conta própria.

Segurança (obrigatório):
- Toda entrada externa é não confiável.
- SQL sempre parametrizado, nunca concatenado.
- Nenhum segredo no código-fonte.
- Autorização validada no servidor, nunca apenas na interface.
- Nenhuma falha silenciosa: erro não pode ser engolido.

Qualidade:
- Função com responsabilidade única e nome que revela intenção.
- Teste proporcional ao risco; correção de bug acompanha teste de regressão.
- Comentário explica o porquê, não o quê.
- Mudança pequena, verificável e reversível.
- Documentação afetada é atualizada junto.

Sankhya: identifique primeiro se o projeto é legado (AcaoRotinaJava, Jape, DynamicVO, NativeSql) ou Add-on Studio (@ActionButton, @Service, @Listener). Nunca misture os dois modelos. Nunca cite tabela ou campo sem confirmar no dicionário de dados (TDDTAB/TDDCAM).

---

<!-- frontend/electron.md -->

# Electron

Fonte primária: [Security Checklist oficial](https://www.electronjs.org/docs/latest/tutorial/security).

## Isolamento (obrigatório)

- `contextIsolation` MUST permanecer habilitado.
- `nodeIntegration` MUST permanecer desabilitado no renderer.
- `sandbox` SHOULD ser habilitado.
- `webSecurity` MUST NOT ser desabilitado.
- Conteúdo remoto MUST NOT ser carregado com privilégios de Node.

## IPC

- A superfície exposta pelo preload MUST ser mínima e específica; MUST NOT expor `ipcRenderer` inteiro via `contextBridge`.
- Todo handler IPC MUST validar os argumentos recebidos — o renderer é tratado como não confiável.
- MUST NOT expor APIs genéricas de execução, leitura arbitrária de arquivo ou acesso a shell.

## Navegação e conteúdo

- MUST restringir navegação e abertura de janelas para origens permitidas.
- Links externos SHOULD abrir no navegador do sistema.
- SHOULD definir Content-Security-Policy restritiva.
- MUST NOT injetar HTML derivado de entrada externa sem sanitização.

## Distribuição

- MUST manter o Electron atualizado — vulnerabilidades do Chromium são herdadas.
- Aplicações distribuídas SHOULD ser assinadas e ter atualização por canal seguro.

---

<!-- frontend/html-css.md -->

# HTML / CSS

HTML:
- SHOULD seguir WHATWG HTML Living Standard.
- MUST priorizar semântica e acessibilidade.

CSS:
- SHOULD evitar especificidade excessiva.
- SHOULD organizar tokens/variáveis de design de forma consistente.
- MUST respeitar prefers-reduced-motion quando animações puderem afetar acessibilidade.

---

<!-- frontend/nextjs.md -->

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

---

<!-- frontend/react.md -->

# React

- Components e Hooks MUST permanecer puros durante renderização.
- Props e state MUST ser tratados como imutáveis.
- Hooks MUST ser chamados no top-level de componentes/hooks.
- Side effects SHOULD ocorrer em mecanismos apropriados, não durante render.
- useEffect SHOULD NOT ser usado para estado derivável sem necessidade externa.
- Componentes SHOULD manter responsabilidade coerente.

---

<!-- frontend/standard.md -->

# Frontend

- MUST usar HTML semântico quando aplicável.
- SHOULD atender WCAG 2.2 no nível exigido pelo produto.
- MUST tratar dados vindos do backend como não confiáveis para renderização/HTML.
- SHOULD separar apresentação de lógica complexa.
- SHOULD evitar estado duplicado derivável.
- SHOULD medir performance antes de micro-otimizações.

---

<!-- frontend/tailwind.md -->

# Tailwind CSS

- SHOULD usar utilitários de forma consistente com a versão instalada.
- MUST NOT construir fragmentos arbitrários de classes quando isso impedir detecção pelo compilador/scanner.
- SHOULD extrair componentes quando a repetição representar um componente real, não apenas para reduzir número de classes.
- MUST preservar acessibilidade independentemente do framework CSS.

---

<!-- languages/typescript.md -->

# TypeScript

- SHOULD habilitar `strict` em projetos novos.
- SHOULD preferir `unknown` a `any` para valores não confiáveis.
- `any` SHOULD exigir justificativa quando evitável.
- Tipos públicos SHOULD representar o domínio e o contrato, não apenas satisfazer o compilador.
- Runtime validation MUST existir quando dados entram de fronteira externa; TypeScript não substitui validação em runtime.

---

<!-- languages/javascript.md -->

# JavaScript

- SHOULD usar ESLint e Prettier conforme configuração do projeto.
- MUST evitar globals acidentais.
- Promises MUST ter tratamento de erro adequado.
- SHOULD preferir módulos e APIs modernas compatíveis com o runtime alvo.
- Entradas externas MUST ser validadas em fronteiras de confiança.
