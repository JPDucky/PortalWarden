const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();
const PORT = process.env.PORT || 8091;
const targetUrl = process.env.TARGET_URL;

app.use('/', createProxyMiddleware({
	target: targetUrl,
	changeOrigin: true,
	pathRewrite: {
		'^/': '', // removes proxy from request path
	},
	onError: function (err, req, res) {
		console.error('An error has occurred:', err);
		res.status(500).send('Oops, something went wrong.');
		res.json({ error: 'An error has occurred while proxying request' });
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


app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});

