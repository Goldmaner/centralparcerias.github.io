# ═══════════════════════════════════════════════════════════════
# CENTRAL DE PARCERIAS — SERVIDOR LOCAL
# ═══════════════════════════════════════════════════════════════
# 
# COMO EXECUTAR:
# 1. Abra o Terminal (PowerShell ou CMD)
# 2. Copie e cole o caminho abaixo:
#    cd "c:\Users\Jefferson\OneDrive - rede.sp\Área de Trabalho\FAF\REF\DemonstrativoAfericaohtml"
# 3. Execute o servidor:
#    python iniciar_servidor.py
#
# O navegador abrirá automaticamente em http://localhost:8899
# Para parar o servidor, pressione Ctrl+C no terminal
# ═══════════════════════════════════════════════════════════════

import http.server
import socketserver
import webbrowser
import os
import json
from urllib.parse import urlparse

PORTA = 8899
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)


_version_cache = {'value': None, 'expires': 0.0}

def build_version_stamp():
    """Retorna um carimbo numérico baseado na última modificação dos arquivos do projeto.
    O resultado é cacheado por 2 s para não bloquear o servidor a cada poll do hot reload."""
    import time
    now = time.monotonic()
    if _version_cache['value'] is not None and now < _version_cache['expires']:
        return _version_cache['value']

    latest_mtime = 0.0
    watched_ext = ('.html', '.css', '.js', '.json', '.md')

    for root, _, files in os.walk(BASE_DIR):
        if '.git' in root or '__pycache__' in root:
            continue
        for name in files:
            if not name.lower().endswith(watched_ext):
                continue
            try:
                path = os.path.join(root, name)
                latest_mtime = max(latest_mtime, os.path.getmtime(path))
            except OSError:
                continue

    stamp = int(latest_mtime * 1000)
    _version_cache['value'] = stamp
    _version_cache['expires'] = now + 2.0
    return stamp


RELOAD_SNIPPET = """
<script>
(() => {
  let lastVersion = null;
  async function checkReload() {
    try {
      const r = await fetch('/__reload?ts=' + Date.now(), { cache: 'no-store' });
      const data = await r.json();
      if (lastVersion === null) {
        lastVersion = data.version;
        return;
      }
      if (data.version !== lastVersion) {
        location.reload();
      }
    } catch (_) {
      // Ignora falhas temporárias de rede durante desenvolvimento local.
    }
  }
  setInterval(checkReload, 1200);
  checkReload();
})();
</script>
"""

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    """Desabilita cache e injeta hot reload para desenvolvimento local."""

    def _send_reload_version(self):
        payload = json.dumps({"version": build_version_stamp()}).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _serve_html_with_reload(self, path):
        local_path = self.translate_path(path)
        if os.path.isdir(local_path):
            for index in ('index.html', 'index.htm'):
                candidate = os.path.join(local_path, index)
                if os.path.exists(candidate):
                    local_path = candidate
                    break

        if not os.path.exists(local_path):
            self.send_error(404, 'File not found')
            return

        try:
            with open(local_path, 'rb') as f:
                content = f.read()
        except OSError:
            self.send_error(404, 'File not found')
            return

        lower = content.lower()
        marker = b'</body>'
        if marker in lower:
            idx = lower.rfind(marker)
            content = content[:idx] + RELOAD_SNIPPET.encode('utf-8') + content[idx:]
        else:
            content += RELOAD_SNIPPET.encode('utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/__reload':
            self._send_reload_version()
            return

        if parsed.path == '/':
            self._serve_html_with_reload('/index.html')
            return

        if parsed.path.lower().endswith(('.html', '.htm')):
            self._serve_html_with_reload(parsed.path)
            return

        super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

class ThreadingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Servidor multi-threaded: cada requisição roda em thread própria,
    evitando que polls do hot-reload travem o carregamento das páginas."""
    allow_reuse_address = True
    daemon_threads = True

print(f"✅ Servidor iniciado em http://localhost:{PORTA}")
print("   Pressione Ctrl+C para encerrar.\n")

webbrowser.open(f"http://localhost:{PORTA}")

with ThreadingServer(("", PORTA), NoCacheHandler) as httpd:
    httpd.serve_forever()
