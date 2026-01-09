# ⚡ Quick Start - Run App Locally

## Current Status
✅ MySQL is running
✅ .env file created
❌ Python dependencies need to be installed

## Steps to Run the App

### 1. Install Python Dependencies (Required)
```bash
# Install pip and venv
sudo apt install python3-pip python3-venv

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Update .env File
Edit `.env` and update:
- `DATABASE_PASSWORD` - Your MySQL root password (or leave as "root" if that's your password)

### 3. Create Database
```bash
# Create the database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS grocery_db;"
# Enter your MySQL password when prompted
```

### 4. Run Migrations
```bash
# Activate venv (if not already)
source venv/bin/activate

# Run database migrations
flask db upgrade
```

### 5. Start the App
```bash
# Activate venv (if not already)
source venv/bin/activate

# Run the app
python3 app.py
```

## Access the App
- **Homepage:** http://127.0.0.1:5000
- **Admin Panel:** http://127.0.0.1:5000/admin/login
  - Email: `admin@denncathy.com`
  - Password: `Admin123!`

## One-Line Setup (After installing pip)
```bash
sudo apt install python3-pip python3-venv && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS grocery_db;" && flask db upgrade && python3 app.py
```

## Need Help?
See `RUN_LOCALLY.md` for detailed troubleshooting.
