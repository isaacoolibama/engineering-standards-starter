# Java Sankhya Review Checklist

- [ ] Modelo do projeto identificado: tradicional/legado ou SDK/Add-on Studio.
- [ ] Versão Java/runtime compatível.
- [ ] APIs Sankhya utilizadas existem no alvo.
- [ ] Entry point está enxuto.
- [ ] Jape/session é fechado corretamente quando aberto manualmente.
- [ ] Limite transacional está claro.
- [ ] SQL nativo usa parâmetros.
- [ ] Campos/entidades foram validados; nenhum nome foi inventado.
- [ ] Hook escolhido corresponde ao evento de negócio.
- [ ] Não há chamadas lentas em regra transacional crítica.
- [ ] Feedback ao usuário é adequado.
- [ ] Logs preservam contexto sem expor secrets.
