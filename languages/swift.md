# Swift

Fontes primárias: [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/), [DocC](https://www.swift.org/documentation/docc/).

## Nomes

- Nomes MUST priorizar clareza no ponto de uso, não brevidade.
- Métodos com efeito colateral SHOULD usar verbo imperativo (`sort()`); sem efeito, forma nominal (`sorted()`).
- SHOULD nomear parâmetros de forma a compor uma frase legível na chamada.

## Segurança e opcionais

- MUST NOT usar force unwrap (`!`) fora de invariante comprovada e comentada.
- SHOULD usar `guard let` para saída antecipada.
- SHOULD preferir `struct` a `class` quando não houver necessidade de identidade ou herança.
- MUST evitar retain cycles com `[weak self]`/`[unowned self]` em closures que capturam `self`.

## Erros e concorrência

- Falhas esperadas SHOULD usar `throws` e `Result`, não códigos de retorno.
- MUST NOT usar `try!` sem invariante garantida.
- Código concorrente SHOULD usar `async/await` e atores em vez de locks manuais.
- SHOULD habilitar checagem de concorrência estrita nos projetos que a suportem.

## Documentação

- APIs públicas SHOULD usar comentários DocC (`///`) descrevendo parâmetros, retorno e erros.
