from flask import Flask, request, Response
import requests
from urllib.parse import urljoin, urlparse
import re

app = Flask(__name__)

@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/styles.css')
def styles():
    with open('styles.css', 'r') as f:
        return f.read(), 200, {'Content-Type': 'text/css'}

@app.route('/script.js')
def script():
    with open('script.js', 'r') as f:
        return f.read(), 200, {'Content-Type': 'application/javascript'}

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    
    if not url:
        return 'Error: No URL provided', 400
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if 'text/html' in response.headers.get('Content-Type', ''):
            content = response.text
            content = rewrite_urls(content, url)
            return content
        else:
            return response.content, 200, {'Content-Type': response.headers.get('Content-Type', 'application/octet-stream')}
    
    except requests.exceptions.RequestException as e:
        return f'Error fetching URL: {str(e)}', 500

def rewrite_urls(html, base_url):
    def rewrite_url(match):
        url = match.group(1)
        if url.startswith('http://') or url.startswith('https://'):
            return f'href="/proxy?url={url}"'
        elif url.startswith('/'):  
            parsed = urlparse(base_url)
            full_url = f"{parsed.scheme}://{parsed.netloc}{url}"
            return f'href="/proxy?url={full_url}"'
        else:
            full_url = urljoin(base_url, url)
            return f'href="/proxy?url={full_url}"'
    
    html = re.sub(r'href=["']([^"']+)["']', rewrite_url, html)
    return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)