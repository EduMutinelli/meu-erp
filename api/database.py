import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

print("✅ psycopg2 importado com sucesso!")

class Database:
    def __init__(self):
        self.conn_params = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'port': os.getenv('DB_PORT', 5432)
        }
    
    def get_connection(self):
        """Obtém uma nova conexão com o banco"""
        try:
            conn = psycopg2.connect(
                **self.conn_params,
                cursor_factory=RealDictCursor,
                sslmode='require'
            )
            return conn
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return None
        
    def execute_query(self, query, params=None):
        """Executa uma query e retorna o resultado"""
        conn = None
        cur = None
        try:
            # Usa a mesma conexão para tudo
            conn = self.get_connection()
            if not conn:
                return None
                
            cur = conn.cursor()
            cur.execute(query, params or ())
            
            # Para SELECT, retorna os dados
            if query.strip().upper().startswith('SELECT'):
                result = cur.fetchall()
                return [dict(row) for row in result] if result else []
            
            # Para INSERT/UPDATE/DELETE, faz commit
            conn.commit()
            
            # Para INSERT que retorna ID
            if query.strip().upper().startswith('INSERT'):
                if 'RETURNING' in query.upper():
                    result = cur.fetchone()
                    return result['id'] if result else None
                else:
                    cur.execute("SELECT LASTVAL()")
                    return cur.fetchone()['lastval']
            
            # Para UPDATE/DELETE, retorna número de linhas afetadas
            return cur.rowcount
                
        except Exception as e:
            print(f"❌ Erro no banco: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            # Fecha cursor e conexão
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    def execute_transaction(self, queries):
        """Executa múltiplas queries em uma transação"""
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            if not conn:
                return None
                
            cur = conn.cursor()
            results = []
            
            for query, params in queries:
                cur.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    results.append(cur.fetchall())
                else:
                    results.append(cur.rowcount)
            
            conn.commit()
            return results
            
        except Exception as e:
            print(f"❌ Erro na transação: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()