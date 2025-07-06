# AI Journey Orchestrator

A comprehensive AI-powered marketing automation platform that tracks customer behavior, provides personalized recommendations, and sends automated SMS notifications for abandoned cart recovery.

## Features

### 🔐 Authentication System
- Secure user registration and login
- Password hashing with bcrypt
- Session management
- User profile management

### 🛒 E-commerce Functionality
- Product catalog with categories
- Shopping cart system
- Product detail pages
- Responsive product cards with hover effects

### 🤖 AI-Powered Features
- GPT-4/Gemini integration for chatbot
- Personalized product recommendations
- AI-generated marketing messages
- Intelligent customer journey mapping

### 📊 Behavior Tracking
- Real-time user behavior monitoring
- Page views, clicks, and scroll tracking
- Time spent on pages
- Product interaction analytics

### 📱 SMS Marketing
- Twilio integration for SMS notifications
- Abandoned cart recovery messages
- Purchase confirmation messages
- Personalized marketing campaigns

### 💬 Chatbot Assistant
- Floating chatbot interface
- AI-powered customer support
- Product recommendations
- Order assistance

### 📈 Admin Dashboard
- User behavior analytics
- Marketing message tracking
- User management
- Performance metrics

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-journey-orchestrator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   SECRET_KEY=your_secret_key_here
   ```

4. **Initialize the database**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## API Keys Setup

### OpenAI API Key
1. Go to [OpenAI API](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to your `.env` file

### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### Twilio Setup
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token from the dashboard
3. Purchase a phone number for SMS sending
4. Add credentials to your `.env` file

## Usage

### User Registration
1. Click "Register" in the navigation
2. Fill in username, email, phone number, and password
3. Phone number is required for SMS notifications

### Shopping Experience
1. Browse products on the homepage
2. Add items to cart
3. View cart and proceed to checkout
4. Receive SMS notifications for abandoned carts

### AI Chatbot
1. Click the floating chat icon
2. Ask questions about products
3. Get personalized recommendations
4. Receive order assistance

### Admin Features
1. Login as an admin user
2. Access the dashboard via the user menu
3. Monitor user behavior and analytics
4. Track marketing message performance

## Project Structure

```
ai-journey-orchestrator/
├── app.py                 # Main Flask application
├── journey_engine.py      # Customer journey logic
├── gpt_generator.py       # AI response generation
├── sms_sender.py          # SMS notification service
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── cart.html
│   ├── product_detail.html
│   └── admin.html
├── static/                # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── chatbot.js
│       └── tracking.js
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # Project documentation
```

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Session
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite
- **AI Services**: OpenAI GPT-4, Google Gemini
- **SMS Service**: Twilio
- **Styling**: Bootstrap 5, Font Awesome
- **Real-time Features**: JavaScript fetch API

## Features in Detail

### Behavior Tracking
- Tracks user interactions across the site
- Monitors product views, cart additions, and purchases
- Records time spent on pages and scroll behavior
- Captures click patterns and navigation paths

### AI Journey Engine
- Analyzes user behavior patterns
- Determines customer journey stages
- Triggers appropriate marketing actions
- Generates personalized messages

### Abandoned Cart Recovery
- Detects when users add items but don't purchase
- Sends personalized SMS reminders after 5 minutes
- Uses AI to generate compelling recovery messages
- Tracks recovery campaign effectiveness

### Responsive Design
- Mobile-first approach
- Optimized for all device sizes
- Touch-friendly interface
- Fast loading times

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Adding New Features
1. Update the appropriate Python modules
2. Add new templates if needed
3. Update CSS and JavaScript files
4. Test thoroughly before deployment

### Database Schema
The application uses SQLAlchemy with these main models:
- `User`: User accounts and authentication
- `Product`: Product catalog
- `UserBehavior`: Behavior tracking data
- `MarketingMessage`: SMS and notification log

## Security Considerations

- Passwords are hashed using bcrypt
- Session management with secure cookies
- Input validation on all forms
- SQL injection prevention with SQLAlchemy
- CSRF protection considerations

## Deployment

For production deployment:
1. Use a production WSGI server (e.g., Gunicorn)
2. Set up a reverse proxy (e.g., Nginx)
3. Use environment variables for all secrets
4. Enable HTTPS/SSL
5. Set up proper logging and monitoring

## Support

For issues or questions:
1. Check the console for error messages
2. Verify all API keys are correctly set
3. Ensure all dependencies are installed
4. Check the Flask logs for detailed error information

## License

This project is licensed under the MIT License - see the LICENSE file for details.