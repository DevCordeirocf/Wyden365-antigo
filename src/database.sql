-- ======================================
-- Tabelas
-- ======================================

-- Tabela users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    favoriteteam VARCHAR(100),
    isAdmin BOOLEAN DEFAULT FALSE
);

-- Tabela team
CREATE TABLE IF NOT EXISTS team (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    sport VARCHAR(50) NOT NULL
);

-- Tabela event
CREATE TABLE IF NOT EXISTS event (
    id SERIAL PRIMARY KEY,
    sport VARCHAR(50) NOT NULL,
    team1 VARCHAR(100) NOT NULL,
    team2 VARCHAR(100) NOT NULL,
    date TIMESTAMP NOT NULL
);

-- Tabela wallet
CREATE TABLE IF NOT EXISTS wallet (
    id SERIAL PRIMARY KEY,
    userid INT REFERENCES users(id) ON DELETE CASCADE,
    balance FLOAT DEFAULT 0
);

-- Tabela bet
CREATE TABLE IF NOT EXISTS bet (
    id SERIAL PRIMARY KEY,
    userid INT REFERENCES users(id) ON DELETE CASCADE,
    teamid INT REFERENCES team(id),
    eventid INT REFERENCES event(id),
    amount FLOAT NOT NULL
);

-- Tabela prize
CREATE TABLE IF NOT EXISTS prize (
    id SERIAL PRIMARY KEY,
    betid INT REFERENCES bet(id) ON DELETE CASCADE,
    amount FLOAT NOT NULL,
    odds FLOAT NOT NULL
);

-- ======================================
-- Dados iniciais
-- ======================================

-- Usuário administrador
INSERT INTO users (name, email, password, isAdmin)
VALUES ('Admin', 'admin@teste.com', 'admin123', TRUE)
ON CONFLICT DO NOTHING;

-- Exemplo de times
INSERT INTO team (name, sport)
VALUES 
('Team A', 'Football'),
('Team B', 'Football')
ON CONFLICT DO NOTHING;

-- Exemplo de evento
INSERT INTO event (sport, team1, team2, date)
VALUES ('Football', 'Team A', 'Team B', NOW())
ON CONFLICT DO NOTHING;
