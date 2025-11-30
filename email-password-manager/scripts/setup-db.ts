
import { openDb } from '../src/lib/db';

async function setup() {
  const db = await openDb();
  await db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      email TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL
    );
  `);

  await db.exec(`
    CREATE TABLE IF NOT EXISTS credentials (
      id SERIAL PRIMARY KEY,
      userId INTEGER NOT NULL,
      service TEXT NOT NULL,
      username TEXT NOT NULL,
      password TEXT NOT NULL,
      FOREIGN KEY (userId) REFERENCES users (id) ON DELETE CASCADE
    );
  `);

  console.log('Database setup complete.');
  await db.close(); // Explicitly close the pool connection for a script
}

setup();
