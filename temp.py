-- Create the table
CREATE TABLE feature_usage (
    user_id VARCHAR(50),
    feature_name VARCHAR(100),
    usage_date DATE
);

-- Insert data into the table
INSERT INTO feature_usage (user_id, feature_name, usage_date) VALUES
('U1', 'Smart Templates', '2024-06-01'),
('U1', 'Smart Templates', '2024-06-02'),
('U2', 'Smart Templates', '2024-06-01'),
('U3', 'Smart Templates', '2024-06-06'),
('U3', 'Smart Templates', '2024-06-08'),
('U4', 'Smart Templates', '2024-06-11'),
('U5', 'Smart Templates', '2024-06-15');


