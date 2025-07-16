# Property Management System Setup Guide

## Quick Start with Docker

The easiest way to get started is using Docker Compose:

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd property-management

# Start all services
docker-compose up -d

# The application will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Documentation: http://localhost:8000/docs
```

## Manual Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL
- Redis (optional, for notifications)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database:**
   ```bash
   # Create PostgreSQL database
   createdb property_management
   
   # Run migrations
   alembic upgrade head
   ```

6. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

## Database Schema

The system includes the following main entities:

### Users
- Authentication and authorization
- Role-based access (Admin, Landlord, Tenant)
- Profile management

### Properties
- Property details (address, type, features)
- Financial information (rent, deposit)
- Status tracking (available, occupied)

### Tenants
- Personal information
- Emergency contacts
- Employment details

### Rental Agreements
- Lease terms and conditions
- Start/end dates
- Status tracking (draft, active, expired)

### Documents
- File upload and storage
- Document categorization
- Access control

### Notifications
- Alert system for rent expiry
- Email/SMS notifications
- Status tracking

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login

### Properties
- `GET /api/v1/properties` - List properties
- `POST /api/v1/properties` - Create property
- `GET /api/v1/properties/{id}` - Get property details
- `PUT /api/v1/properties/{id}` - Update property
- `DELETE /api/v1/properties/{id}` - Delete property

### Tenants
- `GET /api/v1/tenants` - List tenants
- `POST /api/v1/tenants` - Create tenant
- `GET /api/v1/tenants/{id}` - Get tenant details
- `PUT /api/v1/tenants/{id}` - Update tenant
- `DELETE /api/v1/tenants/{id}` - Delete tenant

### Rental Agreements
- `GET /api/v1/rental-agreements` - List agreements
- `POST /api/v1/rental-agreements` - Create agreement
- `GET /api/v1/rental-agreements/{id}` - Get agreement details
- `PUT /api/v1/rental-agreements/{id}` - Update agreement
- `POST /api/v1/rental-agreements/{id}/sign` - Sign agreement
- `GET /api/v1/rental-agreements/expiring-soon` - Get expiring agreements

### Documents
- `GET /api/v1/documents` - List documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete document

### Notifications
- `GET /api/v1/notifications` - List notifications
- `GET /api/v1/notifications/unread` - Get unread count
- `POST /api/v1/notifications/{id}/read` - Mark as read
- `POST /api/v1/notifications/mark-all-read` - Mark all as read
- `DELETE /api/v1/notifications/{id}` - Delete notification

## Features

### Core Features
- ✅ Property management with detailed profiles
- ✅ Tenant management with contact information
- ✅ Rental agreement creation and tracking
- ✅ Document upload and storage
- ✅ Rent expiry notifications
- ✅ Role-based access control
- ✅ RESTful API with comprehensive endpoints

### Advanced Features
- 🔄 Email/SMS notifications (configurable)
- 🔄 Cloud storage integration (AWS S3)
- 🔄 Background task processing (Celery)
- 🔄 Mobile app support (React Native ready)
- 🔄 Real-time notifications (WebSocket ready)

## Security

- JWT-based authentication
- Password hashing with bcrypt
- Role-based authorization
- CORS configuration
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy

## Scalability

The system is designed for scalability:

- **Database**: PostgreSQL with connection pooling
- **Caching**: Redis for session and data caching
- **File Storage**: Configurable (local or cloud)
- **Background Tasks**: Celery for async processing
- **API**: FastAPI with async support
- **Frontend**: React with component-based architecture

## Future Integrations

The system is prepared for:

- Payment processing (Stripe, PayPal)
- Maintenance request tracking
- Financial reporting and analytics
- Property inspection scheduling
- Tenant screening services
- Insurance management
- Tax reporting tools

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Verify database exists

2. **CORS Errors**
   - Check BACKEND_CORS_ORIGINS in .env
   - Ensure frontend URL is included

3. **File Upload Issues**
   - Check uploads directory permissions
   - Verify file size limits
   - Check allowed file types

4. **Authentication Issues**
   - Verify SECRET_KEY is set
   - Check token expiration settings
   - Ensure proper Authorization headers

### Logs

- Backend logs: Check uvicorn output
- Frontend logs: Check browser console
- Database logs: Check PostgreSQL logs

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs for error messages
3. Verify environment configuration
4. Test individual components

## License

This project is licensed under the MIT License. 