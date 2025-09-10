/**
 * Cloudflare Worker for Jonathan Nguyen's Digital Garden
 * Serves Jekyll static site with clean URLs and proper navigation
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Handle asset requests with proper caching
    if (url.pathname.startsWith('/assets/')) {
      return handleAssetRequest(request, env);
    }
    
    // Handle clean URL routing for Jekyll
    const response = await handlePageRequest(request, env);
    
    // Add security headers
    return addSecurityHeaders(response);
  },
};

/**
 * Handle static asset requests (CSS, JS, images)
 */
async function handleAssetRequest(request, env) {
  const url = new URL(request.url);
  
  try {
    // Try to get asset from static files
    const asset = await env.ASSETS.fetch(request);
    
    if (asset.status === 200) {
      // Clone response to add caching headers
      const response = new Response(asset.body, asset);
      
      // Add long-term caching for assets
      response.headers.set('Cache-Control', 'public, max-age=31536000, immutable');
      
      return response;
    }
    
    return new Response('Asset not found', { status: 404 });
  } catch (error) {
    return new Response('Error loading asset', { status: 500 });
  }
}

/**
 * Handle page requests with clean URL routing
 */
async function handlePageRequest(request, env) {
  const url = new URL(request.url);
  let pathname = url.pathname;
  
  // Handle root path
  if (pathname === '/') {
    pathname = '/index.html';
  }
  
  // Handle clean URLs - try exact match first
  let assetRequest = new Request(url.origin + pathname, request);
  let response = await env.ASSETS.fetch(assetRequest);
  
  // If not found, try adding .html
  if (response.status === 404 && !pathname.endsWith('.html')) {
    pathname = pathname.endsWith('/') ? pathname + 'index.html' : pathname + '.html';
    assetRequest = new Request(url.origin + pathname, request);
    response = await env.ASSETS.fetch(assetRequest);
  }
  
  // If still not found, try without trailing slash
  if (response.status === 404 && pathname.endsWith('/')) {
    pathname = pathname.slice(0, -1) + '.html';
    assetRequest = new Request(url.origin + pathname, request);
    response = await env.ASSETS.fetch(assetRequest);
  }
  
  // If still not found, try directory index
  if (response.status === 404) {
    pathname = url.pathname + (url.pathname.endsWith('/') ? '' : '/') + 'index.html';
    assetRequest = new Request(url.origin + pathname, request);
    response = await env.ASSETS.fetch(assetRequest);
  }
  
  // Return 404 page if nothing found
  if (response.status === 404) {
    const notFoundRequest = new Request(url.origin + '/404.html', request);
    const notFoundResponse = await env.ASSETS.fetch(notFoundRequest);
    
    if (notFoundResponse.status === 200) {
      return new Response(notFoundResponse.body, {
        status: 404,
        headers: notFoundResponse.headers
      });
    }
    
    return new Response('Page not found', { status: 404 });
  }
  
  return response;
}

/**
 * Add security headers to responses
 */
function addSecurityHeaders(response) {
  const newResponse = new Response(response.body, response);
  
  // Security headers
  newResponse.headers.set('X-Frame-Options', 'DENY');
  newResponse.headers.set('X-Content-Type-Options', 'nosniff');
  newResponse.headers.set('X-XSS-Protection', '1; mode=block');
  newResponse.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  
  // Cache control for HTML pages
  if (response.headers.get('Content-Type')?.includes('text/html')) {
    newResponse.headers.set('Cache-Control', 'public, max-age=300, s-maxage=3600');
  }
  
  return newResponse;
}