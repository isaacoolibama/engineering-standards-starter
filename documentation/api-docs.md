# API Documentation

APIs públicas SHOULD possuir contrato legível por máquina quando houver padrão adequado.

- HTTP: OpenAPI.
- Eventos/mensageria: AsyncAPI.
- Estruturas JSON: JSON Schema.
- gRPC: Protocol Buffers como contrato primário.

Documentação MUST refletir o comportamento publicado e SHOULD ser validada no CI.
