-- ======================================
-- SCHEMA CORRIGIDO - WYDEN365
-- Execute este SQL no SQL Editor do Supabase
-- ======================================

-- Dropar tabelas existentes (se quiser resetar)
-- DROP TABLE IF EXISTS prize CASCADE;
-- DROP TABLE IF EXISTS bet CASCADE;
-- DROP TABLE IF EXISTS event CASCADE;
-- DROP TABLE IF EXISTS wallet CASCADE;
-- DROP TABLE IF EXISTS team CASCADE;
-- DROP TABLE IF EXISTS users CASCADE;

-- ======================================
-- Tabela users
-- ======================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    favorite_team VARCHAR(100),

    is_admin BOOLEAN DEFAULT FALSE,  -- ⭐ MUDADO PARA MINÚSCULO
    created_at TIMESTAMP DEFAULT NOW()
);

-- ======================================
-- Tabela team
-- ======================================
CREATE TABLE IF NOT EXISTS team (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    sport VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ======================================
-- Tabela event (CORRIGIDA)
-- ======================================
CREATE TABLE IF NOT EXISTS event (
    id SERIAL PRIMARY KEY,
    sport VARCHAR(50) NOT NULL,
    team1 VARCHAR(100) NOT NULL,
    team2 VARCHAR(100) NOT NULL,
    odds_team1 FLOAT NOT NULL DEFAULT 2.0,  -- ⭐ ADICIONADO
    odds_team2 FLOAT NOT NULL DEFAULT 2.0,  -- ⭐ ADICIONADO
    date TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'aberto',    -- ⭐ ADICIONADO (aberto/fechado/finalizado)
    winner VARCHAR(100),                     -- ⭐ ADICIONADO (team1/team2/empate/null)
    created_at TIMESTAMP DEFAULT NOW()
);

-- ======================================
-- Tabela wallet
-- ======================================
CREATE TABLE IF NOT EXISTS wallet (
    id SERIAL PRIMARY KEY,
    userid INT REFERENCES users(id) ON DELETE CASCADE,
    balance FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ======================================
-- Tabela bet (CORRIGIDA)
-- ======================================
CREATE TABLE IF NOT EXISTS bet (
    id SERIAL PRIMARY KEY,
    userid INT REFERENCES users(id) ON DELETE CASCADE,
    eventid INT REFERENCES event(id) ON DELETE CASCADE,
    selected_team VARCHAR(100) NOT NULL,     -- ⭐ MUDADO (nome do time escolhido)
    amount FLOAT NOT NULL CHECK (amount >= 5.0), -- ⭐ Aposta mínima R$ 5,00
    odds FLOAT NOT NULL,                     -- ⭐ ADICIONADO (odds no momento da aposta)
    potential_prize FLOAT NOT NULL,          -- ⭐ ADICIONADO (amount * odds)
    status VARCHAR(20) DEFAULT 'ativa',      -- ⭐ ADICIONADO (ativa/ganha/perdida/cancelada)
    created_at TIMESTAMP DEFAULT NOW()
);

-- ======================================
-- Tabela prize (OPCIONAL - pode ser removida)
-- Como o prêmio é calculado automaticamente, 
-- podemos usar apenas a tabela bet
-- ======================================
-- Se preferir manter:
CREATE TABLE IF NOT EXISTS prize (
    id SERIAL PRIMARY KEY,
    betid INT REFERENCES bet(id) ON DELETE CASCADE,
    amount FLOAT NOT NULL,
    odds FLOAT NOT NULL,
    paid_at TIMESTAMP DEFAULT NOW()
);

-- ======================================
-- Índices para melhorar performance
-- ======================================
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_wallet_userid ON wallet(userid);
CREATE INDEX IF NOT EXISTS idx_bet_userid ON bet(userid);
CREATE INDEX IF NOT EXISTS idx_bet_eventid ON bet(eventid);
CREATE INDEX IF NOT EXISTS idx_bet_status ON bet(status);
CREATE INDEX IF NOT EXISTS idx_event_status ON event(status);

-- ======================================
-- Dados iniciais (SEM SENHA EM TEXTO PLANO)
-- A senha será inserida via Python com bcrypt
-- ======================================

-- Exemplo de times
INSERT INTO team (name, sport)
VALUES
    ('Atlética WYDEN', 'Futebol'),
    ('Atlética UNIFOR', 'Futebol'),
    ('Atlética UFC', 'Futebol'),
    ('Atlética UECE', 'Futebol'),
    ('Atlética WYDEN', 'Basquete'),
    ('Atlética UNIFOR', 'Basquete')
ON CONFLICT DO NOTHING;

-- Exemplo de evento
INSERT INTO event (sport, team1, team2, odds_team1, odds_team2, date, status)
VALUES 
    ('Futebol', 'Atlética WYDEN', 'Atlética UNIFOR', 1.85, 2.10, NOW() + INTERVAL '3 days', 'aberto'),
    ('Basquete', 'Atlética UFC', 'Atlética UECE', 1.90, 1.95, NOW() + INTERVAL '5 days', 'aberto')
ON CONFLICT DO NOTHING;