# Market-Ready Features Roadmap for Denncathy Fresh Basket

## Phase 1: Order Management (Immediate - 2-3 days)

### 1.1 Order Status & Recovery
- **Resume/Edit Payment-Initiated Orders**
  - Allow customers to resume checkout if browser closes mid-payment
  - Show pending orders on customer dashboard
  - "Retry Payment" button for failed orders
  - Allow order cancellation if payment not completed within 30 mins
  
- **Admin Order Management**
  - View all orders (filter by status: pending, payment_initiated, completed, failed, cancelled)
  - Edit order details (customer info, delivery address) before fulfillment
  - Manually mark orders as: completed, shipped, delivered, refunded
  - Bulk actions (mark multiple as shipped, export CSV)
  - Search orders by reference, customer email, phone

### 1.2 Order Lifecycle
- **Statuses**: pending → payment_initiated → completed → shipped → delivered
- **Guest Orders**: Accessible via order reference link (no login required)
- **Cancellation Policy**: Cancel if payment fails or within 24hrs of order (admin approval)

---

## Phase 2: Email Notifications (2-3 days)

### 2.1 Transactional Emails
**Admin Notifications (you@denncathy.co.ke)**
- New order received (name, items, total, delivery address)
- Payment confirmed (order ref, tracking ID, amount)
- Order cancelled
- Customer requested refund

**Customer Notifications (buyer@example.com)**
- Order confirmation (order ref, items, total, estimated delivery)
- Payment received confirmation
- Order shipped (tracking link if available)
- Delivery reminder (24hrs before expected delivery)
- Order delivered confirmation
- Payment failed (retry link)

### 2.2 Email Setup
- Use SendGrid / Mailgun (free tier available)
- Email templates in `templates/emails/` using Jinja2
- Background task queue (Celery + Redis) for async sending
- Email logs stored in database for audit trail

---

## Phase 3: Order Tracking (3-4 days)

### 3.1 Customer-Facing Tracking
- **Order Status Page**
  - Real-time status updates
  - Estimated delivery date (calculated from order date + delivery window)
  - Item breakdown with individual tracking
  - Delivery address confirmation
  - Customer can update delivery notes before delivery
  
- **Tracking Link**
  - Unique link per order (no login required): `/order/track/<order_ref>`
  - SMS notification with tracking link (optional, requires Twilio)

### 3.2 Admin Tracking Dashboard
- Map view of pending deliveries (Google Maps API)
- Delivery driver assignment
- Status timeline per order (when status changed, by whom)
- Photos on delivery (driver uploads proof of delivery)

---

## Phase 4: Payment & Refunds (2-3 days)

### 4.1 Refund Management
- **Admin Refund Portal**
  - Initiate refund (full or partial)
  - Refund reason tracking (customer requested, out of stock, payment error, etc.)
  - Refund status: pending, processing, completed
  - PesaPal refund API integration

- **Customer Refund Requests**
  - Self-service refund request form (within 7 days of delivery)
  - Reason dropdown (product damaged, not as described, duplicate charge, etc.)
  - Automatic approval for certain categories, manual review for others

### 4.2 Payment Analytics
- Revenue dashboard (daily, weekly, monthly)
- Payment success rate
- Failed payment recovery rate
- Most common failure reasons

---

## Phase 5: Inventory & Product Management (3-4 days)

### 5.1 Stock Management
- **Real-time Inventory**
  - Track stock per product
  - Auto-reduce stock on order completion
  - Low stock alerts (alert admin when < 5 units)
  - Reorder points per product
  - Mark products as "out of stock" (hide from catalog)

- **Inventory History**
  - Log all stock movements (added, sold, adjusted, wasted)
  - Supplier management (reorder from supplier)
  - Expiry date tracking for perishables

### 5.2 Product Recommendations
- "You might also like" (customers who bought X also bought Y)
- Seasonal products carousel
- Best sellers section
- Trending products (most viewed this week)

---

## Phase 6: Customer Management (2-3 days)

### 6.1 Customer Dashboard
- Order history (filter, search, export)
- Favorite/saved items
- Review and rating history
- Address book (saved delivery addresses)
- Wishlist
- Loyalty points / rewards program

### 6.2 Reviews & Ratings
- Post-delivery review request (email 3 days after delivery)
- 5-star rating system with comments
- Photo uploads with reviews
- Helpful/unhelpful voting on reviews
- Admin moderation (flag inappropriate reviews)

---

## Phase 7: Analytics & Reporting (3-4 days)

### 7.1 Business Metrics Dashboard
- **Sales Analytics**
  - Daily/weekly/monthly revenue
  - Average order value
  - Customer lifetime value
  - Repeat customer rate
  
- **Product Analytics**
  - Top selling products
  - Product profit margins
  - Inventory turnover rate
  - Return rate per product

- **Customer Analytics**
  - Total customers, new vs returning
  - Customer acquisition cost
  - Churn rate
  - Geographic distribution

### 7.2 Reports & Exports
- Generate PDF reports (daily, weekly, monthly)
- CSV exports (orders, customers, products)
- Tax report (sales, GST if applicable)
- Profit & loss statement

---

## Phase 8: Marketing & Engagement (2-3 days)

### 8.1 Email Marketing
- Newsletter signup form
- Automated campaigns:
  - Welcome email series (3 emails over 7 days)
  - Abandoned cart recovery (email after 24hrs)
  - Win-back campaign (for inactive customers)
- Segmentation (high-value customers, inactive, new customers)

### 8.2 Promotional Tools
- Discount codes (flat, percentage, product-specific)
- Bulk discounts (buy 5+ items = 10% off)
- Seasonal promotions (flash sales, limited-time offers)
- Referral program (give discount for referring friend)

---

## Phase 9: Security & Compliance (Ongoing)

### 9.1 Data Security
- GDPR compliance (consent, data export, deletion)
- PCI compliance (never store CC, use PesaPal tokenization)
- Two-factor authentication for admin
- Audit logs (who accessed what, when)

### 9.2 Fraud Prevention
- IP blocking for repeated failed payments
- Duplicate order detection
- Unusual activity alerts
- Rate limiting on API endpoints

---

## Phase 10: Mobile & UX (3-5 days)

### 10.1 Mobile Optimization
- Responsive checkout (already done)
- Mobile app (Flutter/React Native) for future
- One-click reorder (for frequent customers)

### 10.2 UX Improvements
- Live chat support (Intercom, Drift)
- FAQ chatbot (AI-powered)
- Order notifications (push, SMS)
- Order delay alerts (if delivery is delayed, auto-notify)

---

## Implementation Priority Matrix

| Feature | Effort | Impact | Priority |
|---------|--------|--------|----------|
| Order Status & Recovery | 2 days | High | 🔴 **NOW** |
| Email Notifications | 3 days | High | 🔴 **NOW** |
| Refund Management | 2 days | Medium | 🟠 Week 1 |
| Order Tracking | 3 days | High | 🟠 Week 1 |
| Inventory Management | 3 days | High | 🟠 Week 1 |
| Customer Dashboard | 2 days | Medium | 🟠 Week 1 |
| Analytics Dashboard | 3 days | Medium | 🟡 Week 2 |
| Reviews & Ratings | 2 days | Medium | 🟡 Week 2 |
| Email Marketing | 2 days | Medium | 🟡 Week 2 |
| Live Chat | 1 day | Medium | 🟡 Week 3 |

---

## Quick Wins (Can do today)

1. **Add "Order Status" page** (route: `/order/<order_id>`)
   - Show current status, items, total, delivery address
   - Button to resend confirmation email
   - Cancel button (with refund if applicable)

2. **Send basic emails** (using Flask-Mail + SMTP)
   - Order confirmation to customer
   - New order alert to admin
   - Payment received confirmation

3. **Add Inventory Check** 
   - Before checkout, verify all items in stock
   - Show out-of-stock items as unavailable

4. **Add Order Timeline**
   - Show when order was placed, payment received, shipped, delivered
   - Admin can update status from dashboard

---

## Tech Stack Recommendations

- **Email**: SendGrid (15k free emails/month) or Mailgun
- **Task Queue**: Celery + Redis (for async email sending)
- **SMS**: Twilio (optional, for SMS notifications)
- **Maps**: Google Maps API (for delivery tracking)
- **Analytics**: Plausible (privacy-friendly alternative to GA)
- **Live Chat**: Intercom or Drift
- **Hosting**: Keep Host Africa, add CDN for images (Cloudflare)

---

## Database Schema Additions

```sql
-- Order Status History (audit trail)
CREATE TABLE order_status_history (
    id INT PRIMARY KEY,
    order_id INT,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_by INT,  -- admin_id
    reason TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Refund Requests
CREATE TABLE refund_requests (
    id INT PRIMARY KEY,
    order_id INT,
    amount DECIMAL,
    reason VARCHAR(255),
    status VARCHAR(50),  -- pending, approved, completed, rejected
    created_at TIMESTAMP,
    approved_by INT,  -- admin_id
    approved_at TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Inventory Tracking
CREATE TABLE inventory_log (
    id INT PRIMARY KEY,
    product_id INT,
    quantity_change INT,
    reason VARCHAR(100),  -- "sold", "restock", "adjustment", "waste"
    created_at TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Email Logs
CREATE TABLE email_logs (
    id INT PRIMARY KEY,
    recipient VARCHAR(255),
    subject VARCHAR(255),
    email_type VARCHAR(100),  -- "order_confirmation", "payment_received", etc
    status VARCHAR(50),  -- "sent", "failed", "bounced"
    sent_at TIMESTAMP,
    order_id INT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Reviews
CREATE TABLE product_reviews (
    id INT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    rating INT,  -- 1-5
    comment TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (customer_id) REFERENCES users(id)
);
```

