import http.server
import cgi
import os
import urllib.parse

SAVE_DIR = "/media/joe/A7C8-0792"

HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Flash Drive</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: sans-serif; background: #111; color: #eee; min-height: 100vh; padding: 24px; }
    h2 { color: #0f0; font-size: 22px; margin-bottom: 6px; text-align: center; }
    p.sub { color: #aaa; font-size: 13px; margin-bottom: 24px; text-align: center; }

    .tabs { display: flex; margin-bottom: 24px; border-radius: 8px; overflow: hidden; border: 1px solid #0f0; }
    .tab { flex: 1; padding: 12px; text-align: center; cursor: pointer; font-weight: bold; font-size: 14px; background: #1a1a1a; color: #aaa; }
    .tab.active { background: #0f0; color: #000; }

    .section { display: none; }
    .section.active { display: block; }

    .drop-area { width: 100%; border: 2px dashed #0f0; border-radius: 12px; padding: 32px 16px; text-align: center; cursor: pointer; margin-bottom: 16px; background: #1a1a1a; }
    .drop-icon { font-size: 40px; margin-bottom: 10px; }
    .drop-text { color: #aaa; font-size: 14px; }
    .drop-text span { color: #0f0; font-weight: bold; }
    input[type=file] { display: none; }

    #fileList { margin-bottom: 16px; }
    .file-item { background: #1a1a1a; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; }
    .file-name { color: #eee; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 260px; }
    .file-size { color: #aaa; flex-shrink: 0; margin-left: 8px; }

    button.main { width: 100%; background: #0f0; color: #000; border: none; padding: 14px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; margin-bottom: 16px; }
    button.main:disabled { background: #333; color: #666; cursor: not-allowed; }

    #progress-container { display: none; margin-bottom: 12px; }
    #progress-bar { width: 100%; background: #333; border-radius: 6px; height: 20px; margin-bottom: 6px; }
    #progress-fill { height: 20px; background: #0f0; border-radius: 6px; width: 0%; transition: width 0.2s; }
    #progress-text { color: #aaa; font-size: 13px; text-align: center; }

    #msg { font-size: 15px; font-weight: bold; text-align: center; margin-top: 8px; }
    #msg.success { color: #0f0; }
    #msg.error { color: #f44; }

    .drive-file { background: #1a1a1a; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .drive-file-info { overflow: hidden; }
    .drive-file-name { color: #eee; font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 220px; }
    .drive-file-size { color: #aaa; font-size: 12px; margin-top: 2px; }
    .download-btn { background: #0f0; color: #000; border: none; padding: 8px 14px; border-radius: 6px; font-weight: bold; font-size: 13px; cursor: pointer; flex-shrink: 0; margin-left: 8px; text-decoration: none; }
    .empty { color: #aaa; text-align: center; padding: 32px; font-size: 14px; }
    .refresh-btn { width: 100%; background: #1a1a1a; color: #0f0; border: 1px solid #0f0; padding: 10px; font-size: 14px; border-radius: 8px; cursor: pointer; margin-bottom: 16px; }
  </style>
</head>
<body>
  <h2>Flash Drive</h2>
  <p class="sub">Send to drive or download from drive</p>

  <div class="tabs">
    <div class="tab active" onclick="switchTab('upload')">📤 Send to Drive</div>
    <div class="tab" onclick="switchTab('browse')">📥 Get from Drive</div>
  </div>

  <!-- UPLOAD SECTION -->
  <div class="section active" id="upload-section">
    <div class="drop-area" onclick="document.getElementById('fileInput').click()">
      <div class="drop-icon">📁</div>
      <div class="drop-text">Tap to select files<br><span>Choose multiple at once</span></div>
    </div>
    <input type="file" id="fileInput" multiple accept="*/*">
    <div id="fileList"></div>
    <button class="main" id="sendBtn" onclick="uploadFiles()" disabled>Select files first</button>
    <div id="progress-container">
      <div id="progress-bar"><div id="progress-fill"></div></div>
      <div id="progress-text">0%</div>
    </div>
    <p id="msg"></p>
  </div>

  <!-- BROWSE SECTION -->
  <div class="section" id="browse-section">
    <button class="refresh-btn" onclick="loadFiles()">🔄 Refresh</button>
    <div id="driveFileList"><p class="empty">Loading...</p></div>
  </div>

  <script>
    const input = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const sendBtn = document.getElementById('sendBtn');

    function switchTab(tab) {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
      if (tab === 'upload') {
        document.querySelectorAll('.tab')[0].classList.add('active');
        document.getElementById('upload-section').classList.add('active');
      } else {
        document.querySelectorAll('.tab')[1].classList.add('active');
        document.getElementById('browse-section').classList.add('active');
        loadFiles();
      }
    }

    function loadFiles() {
      document.getElementById('driveFileList').innerHTML = '<p class="empty">Loading...</p>';
      fetch('/files')
        .then(r => r.json())
        .then(files => {
          const container = document.getElementById('driveFileList');
          if (!files.length) {
            container.innerHTML = '<p class="empty">No files on flash drive</p>';
            return;
          }
          container.innerHTML = '';
          files.forEach(f => {
            const div = document.createElement('div');
            div.className = 'drive-file';
            div.innerHTML = `
              <div class="drive-file-info">
                <div class="drive-file-name">${f.name}</div>
                <div class="drive-file-size">${f.size}</div>
              </div>
              <a class="download-btn" href="/download?file=${encodeURIComponent(f.name)}" download="${f.name}">Download</a>
            `;
            container.appendChild(div);
          });
        });
    }

    input.addEventListener('change', function() {
      fileList.innerHTML = '';
      const files = this.files;
      if (!files.length) {
        sendBtn.disabled = true;
        sendBtn.innerText = 'Select files first';
        return;
      }
      for (let f of files) {
        const item = document.createElement('div');
        item.className = 'file-item';
        item.innerHTML = '<span class="file-name">' + f.name + '</span><span class="file-size">' + formatSize(f.size) + '</span>';
        fileList.appendChild(item);
      }
      sendBtn.disabled = false;
      sendBtn.innerText = 'Send ' + files.length + ' file(s) to Flash Drive';
    });

    function uploadFiles() {
      const files = input.files;
      if (!files.length) return;
      const formData = new FormData();
      for (let f of files) formData.append('file', f);
      sendBtn.disabled = true;
      document.getElementById('progress-container').style.display = 'block';
      document.getElementById('msg').innerText = '';
      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/');
      xhr.upload.onprogress = function(e) {
        if (e.lengthComputable) {
          const pct = Math.round((e.loaded / e.total) * 100);
          document.getElementById('progress-fill').style.width = pct + '%';
          document.getElementById('progress-text').innerText = pct + '% — ' + formatSize(e.loaded) + ' / ' + formatSize(e.total);
        }
      };
      xhr.onload = function() {
        const msg = document.getElementById('msg');
        msg.innerText = '✅ Saved to flash drive!';
        msg.className = 'success';
        document.getElementById('progress-text').innerText = '100% — Done!';
        sendBtn.disabled = false;
        sendBtn.innerText = 'Send More Files';
        fileList.innerHTML = '';
        input.value = '';
      };
      xhr.onerror = function() {
        const msg = document.getElementById('msg');
        msg.innerText = '❌ Upload failed. Try again.';
        msg.className = 'error';
        sendBtn.disabled = false;
      };
      xhr.send(formData);
    }

    function formatSize(bytes) {
      if (bytes < 1024) return bytes + ' B';
      if (bytes < 1024*1024) return (bytes/1024).toFixed(1) + ' KB';
      return (bytes/(1024*1024)).toFixed(1) + ' MB';
    }
  </script>
</body>
</html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/files':
            self.serve_file_list()
        elif self.path.startswith('/download'):
            self.serve_download()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())

    def serve_file_list(self):
        import json
        files = []
        for name in sorted(os.listdir(SAVE_DIR)):
            path = os.path.join(SAVE_DIR, name)
            if os.path.isfile(path):
                size = os.path.getsize(path)
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024*1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
                files.append({"name": name, "size": size_str})
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(files).encode())

    def serve_download(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        filename = params.get('file', [''])[0]
        filepath = os.path.join(SAVE_DIR, os.path.basename(filename))
        if not os.path.isfile(filepath):
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(os.path.getsize(filepath)))
        self.end_headers()
        with open(filepath, "rb") as f:
            while chunk := f.read(1024*1024):
                self.wfile.write(chunk)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST",
                     "CONTENT_TYPE": self.headers["Content-Type"]}
        )
        saved = []
        for field in form.keys():
            item = form[field]
            items = item if isinstance(item, list) else [item]
            for f in items:
                if f.filename:
                    dest = os.path.join(SAVE_DIR, os.path.basename(f.filename))
                    data = f.file.read()
                    with open(dest, "wb") as out:
                        out.write(data)
                    saved.append(f.filename)
        msg = f'Saved: {", ".join(saved)}' if saved else 'No file received.'
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(msg.encode())

    def log_message(self, format, *args):
        print(f"[Request] {args[0]} {args[1]}")

if __name__ == "__main__":
    PORT = 8080
    server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Server running on port {PORT}")
    server.serve_forever()
