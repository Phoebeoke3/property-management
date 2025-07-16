# Deployment Guide - Property Management System

##  Quick Deploy Options

### Option 1: Vercel (Recommended - Free & Easy)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy Frontend:**
   ```bash
   cd frontend
   vercel
   ```

3. **Follow the prompts:**
   - Link to existing project: No
   - Project name: property-management-frontend
   - Directory: ./
   - Override settings: No

4. **Your app will be live at:** `https://your-project-name.vercel.app`

### Option 2: Netlify (Free & Easy)

1. **Build the app:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Netlify:**
   - Go to [netlify.com](https://netlify.com)
   - Drag & drop the `build` folder
   - Your app will be live instantly

### Option 3: Railway (Full Stack - Backend + Frontend)

1. **Deploy Backend:**
   ```bash
   cd backend
   railway login
   railway init
   railway up
   ```

2. **Deploy Frontend:**
   ```bash
   cd frontend
   railway init
   railway up
   ```

## 🌐 Backend Deployment Options

### Option A: Railway (Recommended)
- Free tier available
- Easy PostgreSQL database setup
- Automatic deployments

### Option B: Heroku
- Free tier discontinued
- Paid plans available
- Good for production apps

### Option C: DigitalOcean App Platform
- Starts at $5/month
- Very reliable
- Good for production

## 📱 Mobile Installation

Your app is now a **Progressive Web App (PWA)** which means:

### On Android:
1. Open your app in Chrome
2. Tap the menu (3 dots)
3. Select "Add to Home screen"
4. Your app will install like a native app

### On iPhone:
1. Open your app in Safari
2. Tap the share button
3. Select "Add to Home Screen"
4. Your app will appear on your home screen

## 🔧 Environment Variables

### Frontend (.env):
```env
REACT_APP_API_URL=https://your-backend-url.com
```

### Backend (.env):
```env
DATABASE_URL=your_database_connection_string
SECRET_KEY=your_secret_key
```

## 📊 Database Options

### For Production:
1. **Railway PostgreSQL** (Free tier)
2. **Supabase** (Free tier)
3. **PlanetScale** (Free tier)
4. **AWS RDS** (Paid)

### Update Backend Config:
```python
# backend/app/core/config.py
DATABASE_URL = "postgresql://user:password@host:port/database"
```

## 🚀 Complete Deployment Steps

### 1. Deploy Backend First:
```bash
cd backend
# Choose your platform (Railway, Heroku, etc.)
# Set up database
# Deploy
```

### 2. Update Frontend API URL:
```bash
cd frontend
# Update src/services/api.ts with your backend URL
```

### 3. Deploy Frontend:
```bash
cd frontend
# Choose your platform (Vercel, Netlify, etc.)
# Deploy
```

### 4. Test Everything:
- Frontend loads correctly
- API calls work
- Mobile installation works
- All features function properly

## 🔒 Security Considerations

1. **HTTPS Only** - All modern platforms provide this
2. **Environment Variables** - Never commit secrets
3. **CORS Configuration** - Update backend to allow your frontend domain
4. **Rate Limiting** - Consider adding to backend
5. **Authentication** - Implement proper user authentication

## 📈 Monitoring & Analytics

### Free Options:
- **Vercel Analytics** (if using Vercel)
- **Google Analytics**
- **Sentry** (error tracking)

## 💰 Cost Breakdown

### Free Tier (Recommended for starting):
- **Frontend:** Vercel/Netlify (Free)
- **Backend:** Railway (Free)
- **Database:** Railway PostgreSQL (Free)
- **Total:** $0/month

### Production Tier:
- **Frontend:** Vercel Pro ($20/month)
- **Backend:** Railway ($5/month)
- **Database:** Railway PostgreSQL ($5/month)
- **Total:** ~$30/month

## 🆘 Troubleshooting

### Common Issues:
1. **CORS Errors** - Update backend CORS settings
2. **API Not Found** - Check environment variables
3. **Database Connection** - Verify connection string
4. **Build Failures** - Check for missing dependencies

### Support:
- Check platform documentation
- Review error logs
- Test locally first

## 🎯 Next Steps

1. **Choose your deployment platform**
2. **Deploy backend first**
3. **Update frontend API URL**
4. **Deploy frontend**
5. **Test on mobile devices**
6. **Set up monitoring**
7. **Add custom domain (optional)**

Your property management system will be accessible from anywhere in the world! 🌍 