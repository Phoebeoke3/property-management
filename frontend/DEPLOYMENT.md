# Deploying to Netlify

This guide will help you deploy your Property Management frontend to Netlify using Git.

## Prerequisites

1. A GitHub, GitLab, or Bitbucket account with your code
2. A Netlify account (free at [netlify.com](https://netlify.com))
3. Your backend API deployed and accessible

## Step 1: Prepare Your Repository

1. Make sure your frontend code is committed and pushed to your Git repository
2. Ensure your backend is deployed and accessible via HTTPS

## Step 2: Deploy to Netlify

### Option A: Deploy via Netlify UI (Recommended for first deployment)

1. **Sign in to Netlify**
   - Go to [netlify.com](https://netlify.com) and sign in
   - Click "New site from Git"

2. **Connect your repository**
   - Choose your Git provider (GitHub, GitLab, or Bitbucket)
   - Authorize Netlify to access your repositories
   - Select your property management repository

3. **Configure build settings**
   - **Base directory**: `frontend` (since your frontend is in a subdirectory)
   - **Build command**: `npm run build`
   - **Publish directory**: `build`
   - Click "Deploy site"

4. **Set environment variables**
   - Go to Site settings > Environment variables
   - Add: `REACT_APP_API_URL` = `https://your-backend-domain.com/api/v1`
   - Replace with your actual backend URL

### Option B: Deploy via Netlify CLI

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**
   ```bash
   netlify login
   ```

3. **Navigate to frontend directory and deploy**
   ```bash
   cd frontend
   netlify deploy --prod --dir=build
   ```

## Step 3: Configure Custom Domain (Optional)

1. In Netlify dashboard, go to Site settings > Domain management
2. Click "Add custom domain"
3. Follow the DNS configuration instructions

## Step 4: Update Backend CORS (Important!)

Make sure your backend allows requests from your Netlify domain:

```python
# In your FastAPI backend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-netlify-site.netlify.app",
        "https://your-custom-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Step 5: Test Your Deployment

1. Visit your Netlify site
2. Test all functionality (login, property management, etc.)
3. Check browser console for any errors
4. Verify API calls are working

## Troubleshooting

### Build Errors
- Check that all dependencies are in `package.json`
- Ensure Node.js version compatibility (Netlify uses Node 18 by default)

### API Connection Issues
- Verify `REACT_APP_API_URL` environment variable is set correctly
- Check backend CORS configuration
- Ensure backend is accessible from the internet

### Routing Issues
- The `netlify.toml` file includes SPA redirects for React Router
- If you have custom routes, update the redirects accordingly

## Continuous Deployment

Once deployed, Netlify will automatically rebuild and deploy your site whenever you push changes to your main branch.

## Support

- [Netlify Documentation](https://docs.netlify.com/)
- [React Deployment Guide](https://create-react-app.dev/docs/deployment/) 