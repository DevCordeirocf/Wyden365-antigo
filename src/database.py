from supabase import create_client, Client
import os
import bcrypt
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Cria cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================
# FUNÇÃO PARA OBTER O CLIENTE
# ==========================
def get_supabase_client():
    """Retorna o cliente Supabase"""
    return supabase

# ==========================
# FUNÇÃO PARA HASH DE SENHA
# ==========================
def hash_password(password: str) -> str:
    """Cria hash bcrypt da senha"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# ==========================
# FUNÇÃO PARA TESTAR CONEXÃO
# ==========================
def test_connection():
    """Testa se a conexão com Supabase está funcionando"""
    try:
        # Tenta buscar dados de uma tabela
        response = supabase.table("users").select("*").limit(1).execute()
        print("✅ Conexão com Supabase OK!")
        print(f"📊 Tabela 'users' acessível: {len(response.data)} registros encontrados")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False

# ==========================
# FUNÇÃO PARA CRIAR USUÁRIO ADMIN
# ==========================
def create_admin_user():
    """Cria usuário administrador inicial"""
    try:
        # Verifica se já existe admin
        result = supabase.table("users").select("*").eq("email", "admin@wyden365.com").execute()
        
        if len(result.data) > 0:
            print("⚠️  Usuário admin já existe!")
            return
        
        # Cria senha com hash
        hashed_password = hash_password("Admin@123")
        
        # Insere admin
        admin_data = {
            "name": "Administrador",
            "email": "admin@wyden365.com",
            "password": hashed_password,
            "favoriteteam": None,
            "isAdmin": True  # ⭐ CORRIGIDO para minúsculo
        }
        
        response = supabase.table("users").insert(admin_data).execute()
        
        # Cria carteira para o admin
        admin_id = response.data[0]["id"]
        supabase.table("wallet").insert({
            "userid": admin_id,
            "balance": 0.0
        }).execute()
        
        print("✅ Usuário admin criado com sucesso!")
        print("📧 Email: admin@wyden365.com")
        print("🔑 Senha: Admin@123")
        
    except Exception as e:
        print(f"❌ Erro ao criar admin: {str(e)}")

# ==========================
# FUNÇÃO PARA POPULAR DADOS DE TESTE
# ==========================
def populate_test_data():
    """Popula o banco com dados de teste"""
    try:
        # Verificar se já existem dados
        events = supabase.table("event").select("*").execute()
        if len(events.data) > 0:
            print("⚠️  Dados de teste já existem!")
            return
        
        # Criar usuário de teste
        test_password = hash_password("teste123")
        test_user = supabase.table("users").insert({
            "name": "João Silva",
            "email": "joao@teste.com",
            "password": test_password,
            "favoriteteam": "Atlética WYDEN",
            "isAdmin": False
        }).execute()
        
        # Criar carteira para usuário teste
        supabase.table("wallet").insert({
            "userid": test_user.data[0]["id"],
            "balance": 100.0  # Saldo inicial de R$ 100
        }).execute()
        
        print("✅ Dados de teste criados com sucesso!")
        print("📧 Usuário teste: joao@teste.com")
        print("🔑 Senha: teste123")
        print("💰 Saldo inicial: R$ 100,00")
        
    except Exception as e:
        print(f"❌ Erro ao popular dados: {str(e)}")

# ==========================
# FUNÇÃO PARA INICIALIZAR BANCO
# ==========================
def initialize_database():
    """Inicializa o banco de dados com dados necessários"""
    print("🚀 Inicializando banco de dados...")
    print("-" * 50)
    
    # 1. Testar conexão
    if not test_connection():
        print("\n❌ Falha na conexão. Verifique suas credenciais no .env")
        return False
    
    print("-" * 50)
    
    # 2. Criar admin
    create_admin_user()
    
    print("-" * 50)
    
    # 3. Popular dados de teste
    populate_test_data()
    
    print("-" * 50)
    print("✅ Inicialização concluída!")
    return True

# ==========================
# EXECUÇÃO DIRETA
# ==========================
if __name__ == "__main__":
    initialize_database()