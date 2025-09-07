#!/bin/bash

# Property Management Frontend Deployment Script
echo "🚀 Starting deployment process..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the frontend directory."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the project
echo "🔨 Building the project..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful! The 'build' directory is ready for deployment."
    echo ""
    echo "📋 Next steps:"
    echo "1. Push your code to Git repository"
    echo "2. Go to Netlify and create a new site from Git"
    echo "3. Set base directory to: frontend"
    echo "4. Set build command to: npm run build"
    echo "5. Set publish directory to: build"
    echo "6. Add environment variable: REACT_APP_API_URL = your-backend-url"
    echo ""
    echo "🌐 Your site will be available at: https://your-site-name.netlify.app"
else
    echo "❌ Build failed. Please check the error messages above."
    exit 1
fi 