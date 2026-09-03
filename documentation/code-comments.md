# Code Comments

Comentários devem responder preferencialmente **por quê?** e não **o quê?**.

## MUST documentar quando relevante

- regra de negócio não óbvia;
- workaround;
- limitação de plataforma;
- comportamento contraintuitivo;
- risco de concorrência/transação;
- requisito de compatibilidade;
- formato/protocolo não autoexplicativo.

## MUST NOT

```java
// Incrementa contador
contador++;
```

## Preferível

```java
// Incrementa antes da persistência porque a sequência é calculada
// a partir do valor corrente na mesma transação.
contador++;
```

Código morto não deve permanecer comentado; use controle de versão.
