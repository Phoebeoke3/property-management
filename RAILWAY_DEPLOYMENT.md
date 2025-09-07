# Deploy Both Frontend and Backend to Railway

This guide will help you deploy your entire Property Management application (both frontend and backend) to Railway from one repository.

## Why Railway?

- **One Platform**: Deploy both services from the same repository
- **Automatic Deployments**: Deploys automatically when you push to Git
- **Easy Scaling**: Built-in scaling and monitoring
- **Free Tier**: Generous free tier for development
- **Custom Domains**: Easy custom domain setup

## Prerequisites

1. A GitHub, GitLab, or Bitbucket account with your code
2. A Railway account (free at [railway.app](https://railway.app))
3. Your code committed and pushed to Git

## Step 1: Prepare Your Repository

1. **Ensure all files are committed and pushed to Git**
2. **Verify your project structure:**
   ```
   property-management/
   ├── backend/
   │   ├── app/
   │   ├── requirements.txt
   │   └── railway.json
   ├── frontend/
   │   ├── src/
   │   ├── package.json
   │   └── railway.json
   └── railway.json
   ```

## Step 2: Deploy to Railway

### Option A: Deploy via Railway UI (Recommended)

1. **Sign in to Railway**
   - Go to [railway.app](https://railway.app) and sign in
   - Click "Start a New Project"

2. **Connect your repository**
   - Choose "Deploy from GitHub repo"
   - Select your property management repository
   - Click "Deploy Now"

3. **Configure your services**
   Railway will automatically detect your services. You'll need to configure each one:

   **Backend Service:**
   - Name: `property-management-backend`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

   **Frontend Service:**
   - Name: `property-management-frontend`
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Start Command: `npm run start`

4. **Set environment variables**
   - Go to each service's Variables tab
   - Add necessary environment variables

### Option B: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize and deploy**
   ```bash
   railway init
   railway up
   ```

## Step 3: Configure Environment Variables

### Backend Variables
```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
BACKEND_CORS_ORIGINS=https://your-frontend-domain.railway.app
```

### Frontend Variables
```
REACT_APP_API_URL=https://your-backend-domain.railway.app/api/v1
```

## Step 4: Update CORS Configuration

Update your backend CORS to allow your Railway frontend domain:

```python
# In backend/app/core/config.py
BACKEND_CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "https://*.railway.app",  # Railway domains
    "https://*.netlify.app",  # If you also want Netlify
]
```

## Step 5: Configure Domains

1. **Get your Railway domains**
   - Each service gets a `.railway.app` domain
   - You can set custom domains in Railway dashboard

2. **Update your frontend API configuration**
   - The frontend will automatically use the backend's Railway domain

## Step 6: Test Your Deployment

1. **Test Backend API**
   - Visit your backend domain + `/docs` for Swagger UI
   - Test API endpoints

2. **Test Frontend**
   - Visit your frontend domain
   - Test all functionality
   - Check browser console for errors

## Step 7: Set Up Custom Domains (Optional)

1. **In Railway dashboard**
   - Go to your service
   - Click "Settings" > "Domains"
   - Add your custom domain

2. **Update DNS**
   - Point your domain to Railway's nameservers
   - Or add CNAME records as instructed

## Continuous Deployment

Railway automatically:
- Detects changes in your Git repository
- Builds and deploys your services
- Provides deployment logs and status

## Monitoring and Scaling

- **Logs**: View real-time logs for each service
- **Metrics**: Monitor CPU, memory, and request metrics
- **Scaling**: Automatically scale based on demand
- **Alerts**: Set up alerts for errors or performance issues

## Troubleshooting

### Build Errors
- Check build commands in Railway dashboard
- Verify all dependencies are in requirements.txt/package.json
- Check Railway logs for specific error messages

### Service Communication
- Ensure CORS is properly configured
- Verify environment variables are set correctly
- Check that services can reach each other

### Database Issues
- Ensure your database is accessible from Railway
- Check DATABASE_URL format and credentials

## Cost Optimization

- **Free Tier**: 500 hours/month for each service
- **Pay-as-you-use**: Only pay for what you use
- **Auto-sleep**: Services sleep when not in use (free tier)

## Support

- [Railway Documentation](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app/)

## Alternative: Deploy Both to Netlify

If you prefer Netlify, you can also deploy both there:
- Frontend: Standard Netlify deployment
- Backend: Convert to Netlify Functions or use Netlify's serverless functions

Railway is generally easier for full-stack applications like yours! 