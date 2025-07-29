-- Updated schema for PesaPal payment integration

-- Drop existing tables and recreate with enhanced structure
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;

-- Enhanced orders table with payment tracking
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_id TEXT UNIQUE NOT NULL,  -- Merchant reference
    pesapal_tracking_id TEXT,       -- PesaPal tracking ID
    total_amount DECIMAL(10,2) NOT NULL,
    status TEXT DEFAULT 'pending', -- pending, completed, failed, cancelled
    payment_method TEXT DEFAULT 'pesapal',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Enhanced order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,      -- References orders.id
    product_id INTEGER,             -- May be NULL if product is deleted
    product_name TEXT NOT NULL,     -- Store product name for history
    price DECIMAL(10,2) NOT NULL,   -- Store price at time of order
    quantity INTEGER NOT NULL,
    total DECIMAL(10,2) NOT NULL,   -- price * quantity
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
);

-- Payment transactions log table (optional - for detailed tracking)
CREATE TABLE IF NOT EXISTS payment_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    pesapal_tracking_id TEXT,
    transaction_id TEXT,
    amount DECIMAL(10,2) NOT NULL,
    currency TEXT DEFAULT 'KES',
    status TEXT NOT NULL,          -- pending, completed, failed
    payment_method TEXT,           -- mpesa, card, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- Update users table to include additional fields needed for payments
ALTER TABLE users ADD COLUMN phone TEXT;
ALTER TABLE users ADD COLUMN address TEXT;
ALTER TABLE users ADD COLUMN city TEXT;
ALTER TABLE users ADD COLUMN state TEXT;
ALTER TABLE users ADD COLUMN postal_code TEXT;
ALTER TABLE users ADD COLUMN zip_code TEXT;

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_pesapal_tracking ON orders(pesapal_tracking_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_payment_transactions_order_id ON payment_transactions(order_id);
