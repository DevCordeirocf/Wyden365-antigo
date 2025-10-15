from supabase import create_client, Client
import os

# ==========================
# CONFIGURAÇÃO DO SUPABASE
# ==========================
# Substitua pelos valores do seu projeto Supabase
SUPABASE_URL = "https://<SEU-PROJETO>.supabase.co"
SUPABASE_KEY = "<SUA-CHAVE-ANON-OU-SERVICE-ROLE>"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================
# FUNÇÃO PARA CRIAR AS TABELAS
# ==========================
def create_tables():
    # Script SQL para criar tabelas
    sql = """
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
    """
    supabase.rpc("sql", {"query": sql}).execute()
    print("Tabelas criadas com sucesso!")

# ==========================
# FUNÇÃO PARA INSERIR DADOS INICIAIS
# ==========================
def insert_initial_data():
    # Inserir usuário administrador
    supabase.table("users").upsert({
        "name": "Admin",
        "email": "admin@teste.com",
        "password": "admin123",
        "isAdmin": True
    }).execute()

    # Inserir times
    supabase.table("team").upsert([
        {"name": "Team A", "sport": "Football"},
        {"name": "Team B", "sport": "Football"}
    ]).execute()

    # Inserir evento
    supabase.table("event").upsert({
        "sport": "Football",
        "team1": "Team A",
        "team2": "Team B",
        "date": "now()"
    }).execute()

    print("Dados iniciais inseridos com sucesso!")

# ==========================
# EXECUÇÃO
# ==========================
if __name__ == "__main__":
    create_tables()
    insert_initial_data()
