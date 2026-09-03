> Origem: `frontend/electron.md` — Engineering Standards

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
