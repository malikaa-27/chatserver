# Simple Python Chat Server

This workspace contains a minimal TCP chat server (`code.py`) and a simple client (`client.py`). Both use blocking sockets and a tiny protocol:

- Server listens on 127.0.0.1:12345
- When a client connects, server sends `NICK` and the client must reply with a nickname (UTF-8 bytes)
- After that, clients can send text messages; server broadcasts them to other clients

## Run (Windows PowerShell)

1. Start the server in one terminal:

```powershell
python .\code.py
```

2. Start one or more clients in other terminals:

```powershell
python .\client.py
```

3. When the client connects it will prompt for a nickname. Type it and press Enter. Then type messages and press Enter to send.

To exit a client, press Ctrl+C or type `/quit` (client will close the socket).

## Notes and troubleshooting

- Both scripts assume Python 3.x is installed and `python` is on your PATH.
- If port 12345 is in use, change `PORT` in both `code.py` and `client.py` to an available port.
- The client and server use simple blocking sockets; they're intended for local testing and demos only.

## Suggested improvements
- Use `sendall()` for reliable sending
- Add message framing for large messages
- Use thread synchronization when modifying shared lists in `code.py`
