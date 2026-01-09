#!/bin/bash
# Local Development Setup Script

echo "🚀 Setting up local development environment..."

# Check if python3-venv is installed
if ! python3 -m venv --help &>/dev/null; then
    echo "❌ python3-venv is not installed"
    echo "📦 Installing python3-venv..."
    echo "   Run: sudo apt install python3-venv python3-pip"
    echo ""
    read -p "Do you want to continue without venv? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    USE_VENV=false
else
    USE_VENV=true
fi

# Create virtual environment if possible
if [ "$USE_VENV" = true ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created"
fi

# Install dependencies
echo "📥 Installing dependencies..."
if [ "$USE_VENV" = true ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    pip3 install --user --upgrade pip
    pip3 install --user -r requirements.txt
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
# Local Development Environment Configuration
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=root
DATABASE_NAME=grocery_db
FLASK_ENV=development
FLASK_DEBUG=True
PESAPAL_CONSUMER_KEY=your_consumer_key_here
PESAPAL_CONSUMER_SECRET=your_consumer_secret_here
PESAPAL_IPN_ID=
PESAPAL_BASE_URL=https://cybqa.pesapal.com/pesapalv3
PESAPAL_CALLBACK_URL=http://localhost:5000/payment/callback
PESAPAL_NOTIFICATION_URL=http://localhost:5000/payment/ipn
EOF
    echo "✅ .env file created"
    echo "⚠️  Please update .env with your database credentials"
fi

# Check MySQL connection
echo ""
echo "🔍 Checking MySQL connection..."
if command -v mysql &> /dev/null; then
    echo "✅ MySQL client found"
else
    echo "⚠️  MySQL client not found. Install with: sudo apt install mysql-client"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update .env with your database credentials"
echo "2. Ensure MySQL is running: sudo systemctl status mysql"
echo "3. Create database: mysql -u root -p -e 'CREATE DATABASE IF NOT EXISTS grocery_db;'"
echo "4. Run migrations: flask db upgrade"
echo "5. Start the app: python3 app.py"
echo ""
