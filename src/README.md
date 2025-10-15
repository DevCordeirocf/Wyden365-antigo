Formas de executar o script database.sql
Executar o script no Supabase

Existem algumas formas:

Usando o painel do Supabase

Vá para SQL Editor.

Copie e cole seu init_db.sql.

Clique em Run.

Usando a CLI do Supabase

Instale a CLI:

npm install -g supabase


Faça login:

supabase login


Rode o script:

supabase db query < init_db.sql


Usando um cliente SQL (pgAdmin, DBeaver, DataGrip)

Conecte no banco usando os dados do Supabase.

Execute o script diretamente.
