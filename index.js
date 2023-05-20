const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();
const PORT = process.env.PORT || 8091;
const targetUrl = process.env.TARGET_URL || 'https://example.com';
//const targetUrl = 'https://github.com/linux-surface/linux-surface/';

app.use('/proxy', createProxyMiddleware({
	target: targetUrl,
	changeOrigin: true,
	pathRewrite: {
		'^/proxy': '', // removes proxy from reqeust path
	},
	onProxyRes: function (proxyRes, req, res) {
		// remove x-frame-options header from response
		delete proxyRes.headers['x-frame-options'];
		proxyRes.headers['x-frame-options'] = 'ALLOWALL';
		//proxyRes.headers['x-frame-options'] = 'ALLOW-FROM https://ur-domain.xyz'; 

		//modify CORS headers
		proxyRes.headers['access-control-allow-origin'] = '*';
		proxyRes.headers['access-control-allow-credentials'] = 'true';
		proxyRes.headers['access-control-allow-headers'] = 'Content-Type, Authorization, X-Requested-With';
		proxyRes.headers['access-control-allow-methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD';

		// to remove the content-security-policy header, uncomment
		delete proxyRes.headers['content-security-policy'];
	}
}));

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});

