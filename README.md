# PortalWarden

This Node.js application serves as a simple and customizable proxy server intended to provide a convenient way to embed content from another domain in an iframe on your personal dashboard.

## Description

The application uses the http-proxy-middleware library to set up a proxy server that forwards requests and responses between the client and the target URL. This allows bypassing certain restrictions and modifying headers, such as 'x-frame-options' and 'content-security-policy', which could otherwise prevent the content from being displayed in an iframe on a different domain.

## Warnings

Please be aware that the proxy server doesn't have any form of authentication or rate limiting, so it should not be used to proxy sensitive or restricted content. Use this only with content that you are allowed to access and display.
Setup


## Deployment

To deploy this project run

To set up the application:

1. Clone the repository to your local machine.

``` git clone https://github.com/JPDucky/PortalWarden``` 

2. Open the .env.example file and specify your desired environment variables, then save it as `.env`.

```
# Specify the port you want running on localhost, this is useful for accessing from behind firewall (REQUIRED)
PORT=8091 

# Enter the URL of the site you want to proxy to (REQUIRED)
TARGET_URL=https://example.com 

# Enter the name for your traefik middleware
TRAEFIK_NAME=proxy_1 
#or proxy_2, proxy_3, etc., this is useful for spinning up multiple instances for multiple URLs

# Enter the name of the subdomain you wish to use (REQUIRED)
SUBDOMAIN=example

# Enter the name of your public facing domain that traefik controls (REQUIRED)
DOMAIN=example.com 
```

3. Start the Docker container by running   `docker-compose up -d`

## Configuration

The application can be configured using the following environment variables:

    PORT: The port on which the proxy server listens. Defaults to 8091 if not specified.
    TARGET_URL: The URL of the target server to which requests should be proxied.
    TRAEFIK_NAME: The name of the traefik middleware you want controlling this proxy
    SUBDOMAIN: The name of the subdomain you want traefik to expose
    DOMAIN: The name of you public facing domain that traefik controls

