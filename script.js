function proxyFetch() {
    const url = document.getElementById('urlInput').value;
    const resultDiv = document.getElementById('result');
    
    if (!url) {
        resultDiv.innerHTML = '<p style="color: red;">Please enter a URL</p>';
        return;
    }
    
    let fullUrl = url;
    if (!fullUrl.startsWith('http://') && !fullUrl.startsWith('https://')) {
        fullUrl = 'https://' + fullUrl;
    }
    
    resultDiv.innerHTML = '<p>Loading...</p>';
    
    fetch('/proxy?url=' + encodeURIComponent(fullUrl))
        .then(response => response.text())
        .then(data => {
            resultDiv.innerHTML = data;
        })
        .catch(error => {
            resultDiv.innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
        });
}