# ARQUIVO: api/database.py

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
        try:
            # Conexão com RealDictCursor para retornar dicionários
            conn = psycopg2.connect(
                **self.conn_params,
                cursor_factory=RealDictCursor,
                sslmode='require'
            )
            cur = conn.cursor()
            
            cur.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = cur.fetchall()
                result_dict = [dict(row) for row in result]
                return result_dict
            else:
                conn.commit()
                if query.strip().upper().startswith('INSERT'):
                    if 'RETURNING' in query.upper():
                        result = cur.fetchone()
                        return result['id'] if result else None
                    else:
                        cur.execute("SELECT LASTVAL()")
                        return cur.fetchone()['lastval']
                return cur.rowcount
                
        except Exception as e:
            print(f"❌ Erro no banco: {e}")
            return None
        finally:
            if 'cur' in locals(): 
                cur.close()
            if 'conn' in locals(): 
                conn.close()