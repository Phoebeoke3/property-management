# Property Management System

A comprehensive property management application for landlords and administrators to manage properties, tenants, and rental agreements. Now with enhanced dashboard features and external deployment capabilities!

##  Features

- **Enhanced Dashboard**: Add properties, add locations, filter by location
- **Property Management**: Create and manage individual property profiles
- **Tenant Management**: Store tenant details and contact information
- **Document Management**: Upload and store tenancy agreements and other documents
- **Rent Tracking**: Monitor rent payments and due dates
- **Alert System**: Get notifications when rent agreements are expiring
- **Multi-platform**: Web and mobile applications (PWA ready)
- **Scalable Architecture**: Built for future integrations and growth
- **External Deployment**: Ready for cloud hosting and mobile installation

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (or SQLite for development)

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\Activate.ps1`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables (see `.env.example`)
6. Run database migrations: `python -m alembic upgrade head`
7. Start the server: 
   - **Windows**: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
   - **Mac/Linux**: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
   - **Important**: Must run from the `backend` directory to avoid import errors

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`
   - **Important**: Must run from the `frontend` directory to avoid npm ENOENT errors

##  External Deployment

### Deploy to Netlify (Recommended - Free)
1. Build the frontend: `npm run build`
2. Go to [netlify.com](https://netlify.com)
3. Drag & drop the `build` folder
4. Your app is live instantly!

### Deploy to Vercel
1. Install Vercel CLI: `npm install -g vercel`
2. Deploy: `npx vercel`
3. Follow the prompts

### Mobile Installation
Your app is a Progressive Web App (PWA):
- **Android**: Chrome → Menu → "Add to Home screen"
- **iPhone**: Safari → Share → "Add to Home Screen"

##  Dashboard Features

### Enhanced Dashboard
- **Add Property Button**: Opens modal to add new properties
- **Add Location Button**: Opens modal to add new locations
- **Location Filter**: Dropdown to filter properties by location
- **Property Cards**: Display location, type, rent, and status
- **Statistics Cards**: Show key metrics (total properties, tenants, revenue)

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server for running FastAPI applications
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migrations
- **JWT**: Authentication and authorization (python-jose)
- **Pydantic**: Data validation and settings management
- **Passlib**: Password hashing (bcrypt)
- **Python-multipart**: File upload support
- **SQLite**: Development database (PostgreSQL for production)

### Frontend
- **React**: Web application with TypeScript
- **React Router**: Navigation and routing
- **CSS3**: Modern styling with gradients and animations
- **PWA**: Progressive Web App capabilities

### Infrastructure
- **Docker**: Containerization (optional)
- **Netlify/Vercel**: Frontend hosting
- **Railway/Heroku**: Backend hosting
- **Cloud Storage**: Document storage (AWS S3)

## Project Structure

```
property-management/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── utils/          # Utility functions
│   ├── alembic/            # Database migrations
│   └── requirements.txt    # Python dependencies
├── frontend/               # React web application
│   ├── public/             # Static files and PWA manifest
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── package.json
│   └── vercel.json         # Vercel deployment config
├── docker-compose.yml      # Docker configuration
├── DEPLOYMENT.md           # Detailed deployment guide
└── README.md
```

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

##  UI Features

- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Interactive Elements**: Hover effects, smooth transitions
- **Color Scheme**: Purple gradient theme
- **Card-based Layout**: Easy-to-scan information display
- **Status Indicators**: Visual status badges for properties

## 🔧 Development

### Running Locally
```bash
# Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python -m alembic upgrade head
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm start
```

**Important Windows Notes:**
- Always run uvicorn from the `backend` directory
- Don't use `| cat` in PowerShell (Unix/Linux only)
- If you get import errors, ensure you're in the backend directory

### Building for Production
```bash
cd frontend
npm run build
```

##  Mobile Features

- **PWA Ready**: Install on mobile devices
- **Responsive Design**: Optimized for all screen sizes
- **Touch-friendly**: Large buttons and touch targets
- **Offline Capable**: Basic offline functionality

##  Deployment Options

### Free Tier (Recommended)
- **Frontend**: Netlify/Vercel (Free)
- **Backend**: Railway (Free)
- **Database**: Railway PostgreSQL (Free)
- **Total Cost**: $0/month

### Production Tier
- **Frontend**: Vercel Pro ($20/month)
- **Backend**: Railway ($5/month)
- **Database**: Railway PostgreSQL ($5/month)
- **Total Cost**: ~$30/month

##  Security

- **HTTPS**: All deployments use HTTPS
- **Environment Variables**: Secure configuration management
- **CORS**: Proper cross-origin resource sharing
- **Input Validation**: Pydantic schemas for data validation

##  Future Enhancements

- [ ] User authentication and authorization
- [ ] Real-time notifications
- [ ] Payment processing integration
- [ ] Advanced reporting and analytics
- [ ] Mobile app (React Native)
- [ ] Email/SMS notifications
- [ ] Document upload and management
- [ ] Maintenance request system

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

##  License

This project is licensed under the MIT License.

##  Support

- Check the [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions
- Review the API documentation at `http://localhost:8000/docs`
- Check the troubleshooting section in the deployment guide

##  Troubleshooting

### Common Issues

**Import Error: "No module named 'app'"**
- **Solution**: Always run uvicorn from the `backend` directory
- **Command**: `cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

**npm Error: ENOENT - Could not read package.json**
- **Cause**: Running npm from the wrong directory
- **Solution**: Always run npm commands from the `frontend` directory
- **Command**: `cd frontend && npm install`

**PowerShell "cat" Error**
- **Cause**: `| cat` is Unix/Linux syntax, not Windows PowerShell
- **Solution**: Remove `| cat` from the command
- **Correct**: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

**Server Won't Start**
- Ensure virtual environment is activated: `.\venv\Scripts\Activate.ps1`
- Check you're in the backend directory: `pwd` should show `...\backend`
- Verify dependencies are installed: `pip list | findstr fastapi`

**Working Directory Requirements**
- **Backend**: Must run from `backend/` directory for Python imports to work
- **Frontend**: Must run from `frontend/` directory for npm to find package.json
- **Alternative**: Use `--prefix` flag: `npm --prefix ./frontend install`

---

**Your Property Management System is ready for production deployment!** 🎉 