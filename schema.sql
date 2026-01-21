-- Table des moments (événements)
CREATE TABLE moments (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    mode VARCHAR(10) CHECK (mode IN ('auto', 'request')) DEFAULT 'auto',
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table des followers (relations entre utilisateurs)
CREATE TABLE followers (
    id BIGSERIAL PRIMARY KEY,
    follower VARCHAR(255) NOT NULL,
    following VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(follower, following)
);

-- Table des participations (qui participe à quel moment)
CREATE TABLE participations (
    id BIGSERIAL PRIMARY KEY,
    moment_id BIGINT REFERENCES moments(id) ON DELETE CASCADE,
    user_name VARCHAR(255) NOT NULL,
    status VARCHAR(10) CHECK (status IN ('approved', 'pending')) DEFAULT 'approved',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(moment_id, user_name)
);