drop table feedback;
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    is_spam BOOLEAN NOT NULL,
    user_feedback TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



