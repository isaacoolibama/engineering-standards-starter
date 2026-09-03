> Origem: `languages/cpp.md` — Engineering Standards

# C++

Fontes primárias: [ISO C++](https://isocpp.org/), [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html).

## Ferramentas

- SHOULD usar `clang-format` e `clang-tidy` com configuração versionada.
- SHOULD compilar com `-Wall -Wextra` e tratar avisos relevantes como erro.
- SHOULD usar sanitizers (ASan/UBSan/TSan) na suíte de testes.
- MUST declarar o padrão da linguagem no build (`-std=`/`CMAKE_CXX_STANDARD`).

## Gerenciamento de recursos

- MUST seguir RAII; recursos MUST ser liberados por destrutor.
- MUST NOT usar `new`/`delete` explícitos em código novo — usar `std::unique_ptr`/`std::make_unique`.
- `shared_ptr` SHOULD ser usado apenas quando a propriedade for realmente compartilhada.
- MUST respeitar a regra de zero/três/cinco.

## Segurança de memória

- MUST NOT retornar referência ou ponteiro para objeto local.
- MUST NOT usar iterador ou referência após invalidação do container.
- SHOULD usar `std::span`/`std::string_view` em vez de ponteiro + tamanho, atentando ao tempo de vida.
- MUST NOT usar funções C inseguras (`strcpy`, `sprintf`, `gets`).
- Conversões SHOULD usar casts nomeados; MUST NOT usar cast estilo C.

## Design

- `const` SHOULD ser o padrão em parâmetros e métodos.
- SHOULD preferir algoritmos da biblioteca padrão a laços manuais.
- Exceções SHOULD ser lançadas por valor e capturadas por referência const.
