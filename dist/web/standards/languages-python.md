> Origem: `languages/python.md` — Engineering Standards

# Python

Referências: PEP 8, PEP 257 e documentação oficial de typing.

- SHOULD usar formatter/linter automatizado (ex.: Ruff/Black conforme projeto).
- APIs públicas SHOULD possuir type hints quando isso melhora o contrato.
- Docstrings SHOULD documentar comportamento não trivial, parâmetros, retorno e erros relevantes.
- MUST NOT usar mutable default arguments sem intenção explícita.
- SHOULD preferir pathlib para paths em código moderno quando compatível.
