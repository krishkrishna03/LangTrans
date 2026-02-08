# Netlify Deployment Troubleshooting & Setup

## Issues Fixed

### 1. ❌ "Failed to load module script: application/octet-stream"
**Cause:** This error occurs when:
- The JavaScript file is being served with the wrong MIME type
- SPA routing isn't configured (404 on navigation redirects to index.html but as text/html, not JS)
- Netlify's SPA redirect isn't properly set up

**Solution:** ✅ Added `_redirects` file and `netlify.toml` with proper SPA configuration

### 2. ❌ "Failed to load resource: vite.svg 404"
**Cause:** Missing favicon/icon file in public folder

**Solution:** ✅ Removed the non-existent vite.svg reference from index.html

---

## Netlify Setup Instructions

### Step 1: Connect Your Repository
1. Go to [Netlify](https://app.netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Select GitHub repository: `krishkrishna03/LangTrans`
4. Connect to your GitHub account

### Step 2: Configure Build Settings
When Netlify asks for build settings, use these:

**Build Command:**
```bash
cd frontend && npm install && npm run build
```

**Publish Directory:**
```
frontend/dist
```

**Node Version (Optional but recommended):**
```
18.17.0
```

### Step 3: Set Environment Variables
In Netlify Dashboard → Site Settings → Build & Deploy → Environment:

Add these variables:
```
VITE_API_URL = https://your-backend-url.com/api
NODE_ENV = production
```

**⚠️ IMPORTANT:** Replace `https://your-backend-url.com/api` with your actual backend API URL!

### Step 4: Update Configuration Files

The following files have been updated:

✅ **netlify.toml** - Main Netlify configuration
- Build settings
- SPA redirect rules  
- Cache headers
- Environment variables

✅ **frontend/public/_redirects** - Redirect all routes to index.html
```
/* /index.html 200
```

✅ **frontend/vite.config.js** - Optimized Vite configuration
- Base URL set to `/`
- Vendor chunking for better caching
- Dependency optimization

✅ **frontend/index.html** - Removed non-existent vite.svg favicon

✅ **frontend/.env.production** - Production environment variables

---

## Complete Deployment Checklist

### Before Deploying

- [ ] Update `VITE_API_URL` in your Netlify environment variables
- [ ] Ensure your backend is deployed and accessible
- [ ] Test backend API endpoints with curl:
  ```bash
  curl https://your-backend-url.com/api/health
  ```

### Netlify Configuration Files

**netlify.toml:**
```toml
[build]
  command = "cd frontend && npm install && npm run build"
  publish = "frontend/dist"
  node_version = "18.17.0"

[build.environment]
  NODE_ENV = "production"
  VITE_API_URL = "https://your-backend-url.com/api"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

**frontend/public/_redirects:**
```
/* /index.html 200
```

---

## Testing After Deployment

### 1. Test Frontend Loads
```bash
# Visit your Netlify site
https://your-site.netlify.app/
```

### 2. Check Console for Errors
- Open Browser DevTools (F12)
- Go to Console tab
- Should have NO errors
- Check Network tab - all requests should have 200 status

### 3. Test Language Detection
```bash
# Open DevTools Console and run:
fetch('https://your-backend-url.com/api/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

### 4. Test Translation
1. Enter text in the input box
2. Should auto-detect language
3. Select target language
4. Click Translate
5. Should see result

---

## Common Issues & Solutions

### Issue 1: Still Getting "Failed to load module script"
**Solution:**
1. Clear browser cache (Ctrl+Shift+Del)
2. Hard refresh (Ctrl+Shift+R)
3. Check if `_redirects` file exists in `frontend/public/`
4. Verify netlify.toml has the redirect rules

### Issue 2: "Cannot GET /"
**Solution:**
- Ensure `_redirects` file is at: `frontend/public/_redirects`
- Ensure netlify.toml has the wildcard redirect
- Check build logs in Netlify Dashboard → Deploys → View log

### Issue 3: API Not Responding (CORS Error)
**Solution:**
1. Check if backend is running/deployed
2. Verify `VITE_API_URL` is correct
3. Check backend has CORS enabled for your Netlify domain:
   ```python
   CORS_ORIGINS=https://your-site.netlify.app
   ```
4. Test API directly:
   ```bash
   curl https://your-backend-url.com/api/health
   ```

### Issue 4: Blank Page After Deploy
**Solution:**
1. Check browser console (F12) for JavaScript errors
2. Check Netlify Deploy logs
3. Verify `index.html` loads properly
4. Check if `root` div exists in HTML

### Issue 5: 404 on Reload/Direct Navigation
**Solution:**
- Already fixed with `_redirects` file
- Make sure file is in `frontend/public/` directory
- Verify netlify.toml has redirect rules

---

## Environment Variables

### Frontend (.env.production)
```env
VITE_API_URL=https://your-backend-api.com/api
NODE_ENV=production
```

### Netlify Build Environment
Set in Netlify Dashboard:
```
VITE_API_URL = https://your-backend.com/api
NODE_ENV = production
```

---

## Build Command Breakdown

```bash
cd frontend                  # Navigate to frontend directory
npm install                  # Install dependencies
npm run build                # Build with Vite (creates dist/)
```

Netlify publishes the `frontend/dist` directory to your site.

---

## Verify Everything Works

After deployment, run these tests:

### Test 1: Frontend Loads
```bash
curl https://your-site.netlify.app/ | grep "root"
# Should contain: <div id="root"></div>
```

### Test 2: No 404s
Open DevTools (F12) → Network tab → reload page
- All files should be 200 or 304 (not 404)

### Test 3: API Connection
```bash
curl https://your-backend.com/api/health
# Should return JSON with status: "healthy"
```

### Test 4: Language Detection Works
1. Open your site
2. Type some text
3. Wait 500ms (debounce)
4. Should see "Detected: [Language]"
5. Check DevTools Network tab for POST to `/api/detect-language`

---

## Next Steps

1. **Update Backend URL:**
   - Get your deployed backend URL
   - Update `VITE_API_URL` in Netlify environment

2. **Enable CORS on Backend:**
   - Add your Netlify URL to backend `CORS_ORIGINS`
   - If deployed on Heroku/Railway/etc: `https://your-site.netlify.app`

3. **Monitor Deployment:**
   - Netlify Dashboard → Deploys
   - Check build logs if issues occur

4. **Custom Domain (Optional):**
   - Netlify Dashboard → Domain Management
   - Connect your custom domain
   - Configure HTTPS (automatic)

---

## File Structure for Netlify

```
LangTrans/
├── netlify.toml              ← Main Netlify config (in root)
├── frontend/
│   ├── public/
│   │   └── _redirects        ← SPA redirect rules
│   ├── dist/                 ← Built output (auto-generated)
│   ├── src/
│   ├── .env.production       ← Production env vars
│   ├── vite.config.js
│   ├── index.html
│   └── package.json
└── backend/                  ← Keep for reference
```

---

## Quick Fixes Summary

✅ **Fixed:** 
- Removed vite.svg reference (404 error)
- Added SPA redirect configuration
- Updated vite.config.js for production
- Added netlify.toml with proper settings
- Added _redirects file for fallback
- Created .env.production for build vars

✅ **What to do now:**
1. Push changes to GitHub
2. Netlify auto-redeploys
3. Update `VITE_API_URL` in environment
4. Test and verify

---

If you continue to have issues, check:
1. Netlify Deploy logs
2. Browser Console (F12)
3. Network tab to see actual requests
4. Backend API is accessible and has CORS enabled
