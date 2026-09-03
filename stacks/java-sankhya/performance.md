# Performance Java Sankhya

Código executado em eventos síncronos do ERP impacta diretamente a experiência do usuário.

- Regras/listeners/callbacks SHOULD executar rapidamente.
- MUST evitar chamadas HTTP síncronas em hooks transacionais críticos quando houver alternativa assíncrona suportada.
- MUST evitar queries repetitivas por linha quando consulta em lote for viável.
- SHOULD buscar somente dados necessários.
- SHOULD medir antes de introduzir cache ou otimização complexa.
- Processamentos longos SHOULD usar mecanismos assíncronos/jobs apropriados ao ambiente.
