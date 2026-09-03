> Origem: `languages/php.md` — Engineering Standards

# PHP

Fontes primárias: [PSR-1](https://www.php-fig.org/psr/psr-1/), [PSR-4](https://www.php-fig.org/psr/psr-4/), [PSR-12](https://www.php-fig.org/psr/psr-12/), [documentação oficial](https://www.php.net/docs.php).

## Ferramentas

- SHOULD usar PHP_CodeSniffer ou PHP-CS-Fixer com PSR-12.
- SHOULD usar análise estática (PHPStan ou Psalm) com nível crescente.
- MUST usar Composer com autoload PSR-4 e `composer.lock` versionado.

## Linguagem

- MUST usar `declare(strict_types=1)` em código novo.
- SHOULD tipar parâmetros, retornos e propriedades.
- MUST usar comparação estrita (`===`) salvo necessidade explícita de coerção.
- MUST NOT suprimir erros com `@`.
- MUST NOT usar `eval` nem `extract` sobre entrada externa.

## Segurança

- MUST usar PDO ou driver com prepared statements; MUST NOT interpolar variáveis em SQL.
- Saída em HTML MUST ser escapada (`htmlspecialchars` ou escape do template engine).
- Senhas MUST usar `password_hash`/`password_verify`; MUST NOT usar MD5 ou SHA1.
- Upload de arquivo MUST validar tipo, tamanho e destino fora do document root quando possível.
- Sessões SHOULD usar cookies `HttpOnly`, `Secure` e `SameSite`.
- MUST NOT expor `display_errors` em produção.
