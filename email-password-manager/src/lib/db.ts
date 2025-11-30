import { Pool, QueryResult, types } from 'pg';

// Parse numeric as integer to avoid string type issues
types.setTypeParser(types.builtins.NUMERIC, parseFloat);

let pool: Pool | undefined;

export async function openDb() {
  if (!process.env.DATABASE_URL) {
    throw new Error('DATABASE_URL is not set');
  }

  if (!pool) {
    pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: {
        rejectUnauthorized: false
      }
    });
  }

  // Return a wrapper object that mimics the sqlite methods
  return {
    get: async <T = any>(sql: string, params: any[] = []): Promise<T | undefined> => {
      const { rows } = await pool!.query(sql, params);
      return rows[0] as T | undefined;
    },
    all: async <T = any>(sql: string, params: any[] = []): Promise<T[]> => {
      const { rows } = await pool!.query(sql, params);
      return rows as T[];
    },
    run: async (sql: string, params: any[] = []): Promise<QueryResult> => {
      return await pool!.query(sql, params);
    },
    exec: async (sql: string): Promise<void> => {
      await pool!.query(sql);
    },
    close: async () => {
      // Don't close the pool in serverless environment
      // if (pool) {
      //   await pool.end();
      //   pool = undefined;
      // }
    },
  };
}

// This type will be used to ensure API routes are compatible
export type Db = Awaited<ReturnType<typeof openDb>>;