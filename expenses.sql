-- Create the database
CREATE DATABASE expenses_db;

-- Connect to the database
\c expenses_db;

-- Create the table
CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    expense_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO expenses (description, category, amount, expense_date) VALUES
('Grocery shopping at Walmart', 'Groceries', 82.75, '2025-04-03'),
('Monthly Spotify subscription', 'Entertainment', 9.99, '2025-04-01'),
('Uber ride to airport', 'Transport', 35.50, '2025-04-02')
ON CONFLICT DO NOTHING;
