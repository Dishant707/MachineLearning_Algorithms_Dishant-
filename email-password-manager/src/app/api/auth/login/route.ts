
import { NextRequest, NextResponse } from 'next/server';
import { compare } from 'bcrypt';
import { openDb } from '@/lib/db';
import { getSession } from '@/lib/session';

export async function POST(req: NextRequest) {
  const db = await openDb();
  const session = await getSession();
  const { email, password } = await req.json();

  if (!email || !password) {
    return NextResponse.json({ error: 'Email and password are required' }, { status: 400 });
  }

  try {
    const user = await db.get('SELECT * FROM users WHERE email = $1', [email]);
    if (!user) {
      return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 });
    }

    const passwordMatch = await compare(password, user.password);
    if (!passwordMatch) {
      return NextResponse.json({ error: 'Invalid credentials' }, { status: 401 });
    }

    session.user = {
      id: user.id,
      email: user.email,
    };
    await session.save();

    return NextResponse.json({ message: 'Logged in successfully' }, { status: 200 });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  } finally {
    await db.close();
  }
}
