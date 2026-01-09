# 🚀 Running the App Locally

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
./setup_local.sh
```

### Option 2: Manual Setup

#### 1. Install Python Dependencies
```bash
# Install python3-venv if not installed
sudo apt install python3-venv python3-pip

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2. Set Up Environment Variables
```bash
# Copy the template
cp .env.local .env

# Edit .env with your settings:
# - Update DATABASE_PASSWORD with your MySQL root password
# - Update PESAPAL credentials if you have them (optional for basic testing)
```

#### 3. Set Up MySQL Database
```bash
# Start MySQL (if not running)
sudo systemctl start mysql

# Create database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS grocery_db;"

# Or if no password:
mysql -u root -e "CREATE DATABASE IF NOT EXISTS grocery_db;"
```

#### 4. Run Database Migrations
```bash
# Activate virtual environment (if using)
source venv/bin/activate

# Run migrations
flask db upgrade
```

#### 5. Run the Application
```bash
# Activate virtual environment (if using)
source venv/bin/activate

# Run the app
python3 app.py
```

The app will be available at:
- **Main app:** http://127.0.0.1:5000
- **Admin panel:** http://127.0.0.1:5000/admin/login

## Default Admin Credentials
- **Email:** admin@denncathy.com
- **Password:** Admin123!

## Troubleshooting

### Issue: "python3-venv not found"
```bash
sudo apt install python3-venv python3-pip
```

### Issue: "DATABASE_PASSWORD environment variable is required"
- Make sure `.env` file exists
- Check that `DATABASE_PASSWORD` is set in `.env`

### Issue: "Can't connect to MySQL"
- Check MySQL is running: `sudo systemctl status mysql`
- Verify database credentials in `.env`
- Test connection: `mysql -u root -p`

### Issue: "No module named 'flask'"
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### Issue: Migration errors
```bash
# Check current migration status
flask db current

# If needed, stamp to latest
flask db stamp head

# Then upgrade
flask db upgrade
```

## Environment Variables Reference

Required:
- `SECRET_KEY` - Flask secret key (any random string for dev)
- `DATABASE_PASSWORD` - MySQL root password
- `DATABASE_NAME` - Database name (default: grocery_db)

Optional (for payment testing):
- `PESAPAL_CONSUMER_KEY` - Pesapal API key
- `PESAPAL_CONSUMER_SECRET` - Pesapal API secret
- `PESAPAL_IPN_ID` - IPN ID (get from setup_ipn.py)

## Development Tips

1. **Hot Reload:** The app runs in debug mode by default, so changes auto-reload
2. **Database Changes:** After model changes, create a new migration:
   ```bash
   flask db migrate -m "Description of changes"
   flask db upgrade
   ```
3. **View Logs:** Check console output for errors and debug info
4. **Reset Database:** (⚠️ Deletes all data)
   ```bash
   flask db downgrade base
   flask db upgrade
   ```
