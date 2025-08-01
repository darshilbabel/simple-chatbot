# Simple Chatbot

A real-time Django-based chatbot application with OpenAI integration, supporting both text and voice chat functionality. Built with Django Channels for WebSocket communication and Celery for asynchronous task processing.

## Features

- 🤖 **AI-Powered Conversations**: Integration with OpenAI GPT models for intelligent responses
- 💬 **Real-time Chat**: WebSocket-based communication for instant messaging
- 🎤 **Voice Chat**: Speech-to-text and text-to-speech functionality
- 📱 **Responsive UI**: Clean, mobile-friendly interface built with Tailwind CSS
- ⚡ **Asynchronous Processing**: Celery-based background task handling
- 🗄️ **Database Management**: PostgreSQL with Django ORM
- 📊 **Admin Interface**: Django admin for managing bots, profiles, and conversations
- 🔧 **Configurable Bots**: Multiple LLM providers and model configurations
- 📈 **Chat History**: Persistent conversation storage and retrieval

## Tech Stack

- **Backend**: Django 5.2.4, Django Channels, Django REST Framework
- **Database**: PostgreSQL
- **Message Broker**: Redis
- **Task Queue**: Celery
- **AI Integration**: OpenAI API
- **Frontend**: HTML, JavaScript, Tailwind CSS
- **WebSockets**: Django Channels with Redis channel layer

## Prerequisites

Before running this application, ensure you have the following installed:

- Python 3.8+
- PostgreSQL
- Redis Server
- OpenAI API Key

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd simple_chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory using the provided `sample.env`:

```bash
cp sample.env .env
```

Edit the `.env` file with your configuration:

```env
DATABASE_NAME='your_database_name'
DATABASE_USER='your_database_user'
DATABASE_PASSWORD='your_database_password'
DATABASE_HOST='localhost'
DATABASE_PORT='5432'
SETTINGS_DEBUG='True'
DJANGO_SETTINGS_MODULE='simple_chatbot.settings'
DEFAULT_LOG_LEVEL='INFO'
OPENAI_API_KEY='your_openai_api_key'
```

### 5. Database Setup

Create a PostgreSQL database and run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Load Initial Data

Create initial profiles for the chatbot system:

```bash
python manage.py shell
```

```python
from chatbot.models import Profile
# Create AI profile
ai_profile = Profile.objects.create(
    first_name="AI Assistant",
    email="ai@chatbot.com",
    profile_type="MODERATOR"
)
# Create default user profile
user_profile = Profile.objects.create(
    first_name="User",
    email="user@chatbot.com",
    profile_type="USER"
)
```

## Running the Application

### 1. Start Redis Server

Make sure Redis is running on your system:

```bash
redis-server
```

### 2. Start Celery Worker

In a separate terminal:

```bash
celery -A simple_chatbot worker --loglevel=info --pool=solo
```

### 3. Start Django Development Server

```bash
python manage.py runserver 0.0.0.0:9000
```

The application will be available at `http://localhost:9000`

## Usage

### Text Chat

1. Navigate to `http://localhost:9000/chat/`
2. Enter your context/instructions in the right panel
3. Type your message and press Enter or click Send
4. The AI will respond in real-time

### Voice Chat

1. Navigate to `http://localhost:9000/voice-chat/`
2. Enter your context/instructions in the right panel
3. Click the "Speak" button and speak your message
4. The AI will respond with both text and speech

### Admin Interface

Access the Django admin at `http://localhost:9000/admin/` to:

- Manage bot configurations
- View chat histories
- Manage user profiles
- Configure LLM settings

## Project Structure

```
simple_chatbot/
├── chatbot/                    # Main application
│   ├── admin.py               # Django admin configuration
│   ├── apps.py                # App configuration
│   ├── models/                # Database models
│   │   ├── __init__.py
│   │   ├── base_models.py     # Core models (Bot, Profile, Chat)
│   │   └── enums.py           # Model choices and enums
│   ├── consumers/             # WebSocket consumers
│   │   ├── base_consumer.py   # Base WebSocket consumer
│   │   └── chat_consumers.py  # Chat-specific consumer
│   ├── celery_tasks/          # Background tasks
│   │   └── chat_tasks.py      # AI response processing
│   ├── templates/             # HTML templates
│   │   ├── base.html
│   │   └── chat/
│   │       ├── chat.html      # Text chat interface
│   │       └── voice_demo.html # Voice chat interface
│   ├── migrations/            # Database migrations
│   ├── routing.py             # WebSocket URL routing
│   ├── urls.py                # HTTP URL patterns
│   └── views.py               # Django views
├── simple_chatbot/            # Project settings
│   ├── __init__.py
│   ├── asgi.py                # ASGI configuration
│   ├── celery.py              # Celery configuration
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
└── sample.env                # Environment variables template
```

## Configuration

### Bot Configuration

The `Bot` model supports various configuration options:

- **LLM Provider**: OpenAI, Bedrock, or Bedrock Converse
- **Model Selection**: GPT-4, GPT-4o, GPT-4o-mini, etc.
- **Temperature**: Response randomness (0-1)
- **Max Tokens**: Response length limit
- **Context Management**: Pre-context, main context, and end context
- **Timeouts**: Connection and read timeout settings

### WebSocket Configuration

WebSocket connections are configured in `settings.py` with Redis as the channel layer backend.

### Celery Configuration

Background tasks are configured to use Redis as both broker and result backend.

## API Endpoints

### HTTP Endpoints

- `/chat/` - Text chat interface
- `/voice-chat/` - Voice chat interface
- `/admin/` - Django admin interface

### WebSocket Endpoints

- `ws/chat/` - WebSocket connection for real-time chat

## Models

### Bot
Configurable AI bot with LLM provider settings, context management, and response parameters.

### Profile
User profiles supporting different types (USER, MODERATOR, PROSPECT).

### Chat
Chat message storage with sender/receiver relationships and session management.

## Development

### Adding New Features

1. Create new models in `chatbot/models/`
2. Add WebSocket consumers in `chatbot/consumers/`
3. Implement background tasks in `chatbot/celery_tasks/`
4. Create templates in `chatbot/templates/`
5. Add URL patterns in `chatbot/urls.py`

### Database Migrations

After model changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Testing

Run Django tests:

```bash
python manage.py test
```

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Ensure Redis server is running
   - Check CHANNEL_LAYERS configuration in settings.py

2. **Celery Tasks Not Processing**
   - Verify Celery worker is running
   - Check Redis connection
   - Ensure OPENAI_API_KEY is set

3. **Database Connection Error**
   - Verify PostgreSQL server is running
   - Check database credentials in .env file
   - Ensure database exists

4. **OpenAI API Errors**
   - Verify API key is valid and has sufficient credits
   - Check rate limits and usage quotas

### Logs

- Django logs: Check console output
- Celery logs: Available in Celery worker terminal
- Redis logs: Check Redis server logs

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Configure proper database settings
3. Use a production ASGI server (e.g., Daphne, Uvicorn)
4. Set up Redis with proper persistence
5. Configure Celery with supervisor or systemd
6. Use environment variables for sensitive settings
7. Set up proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request