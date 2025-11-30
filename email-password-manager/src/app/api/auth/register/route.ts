
import { NextRequest, NextResponse } from 'next/server';
import { hash } from 'bcrypt';
import { openDb } from '@/lib/db';

export async function POST(req: NextRequest) {
  const db = await openDb();
  const { email, password } = await req.json();

  if (!email || !password) {
    return NextResponse.json({ error: 'Email and password are required' }, { status: 400 });
  }

  try {
    const existingUser = await db.get('SELECT * FROM users WHERE email = $1', [email]);
    if (existingUser) {
      return NextResponse.json({ error: 'User already exists' }, { status: 409 });
    }

    const hashedPassword = await hash(password, 10);
    await db.run('INSERT INTO users (email, password) VALUES ($1, $2)', [email, hashedPassword]);

    return NextResponse.json({ message: 'User created successfully' }, { status: 201 });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  } finally {
    await db.close();
  }
}
