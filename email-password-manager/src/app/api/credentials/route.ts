
import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/session';
import { openDb } from '@/lib/db';

export async function GET(req: NextRequest) {
  const session = await getSession();
  const user = session.user;

  if (!user) {
    return NextResponse.json({ error: 'Not authenticated' }, { status: 401 });
  }

  const db = await openDb();
  try {
    const credentials = await db.all('SELECT * FROM credentials WHERE userId = $1', [user.id]);
    return NextResponse.json(credentials);
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  } finally {
    await db.close();
  }
}

export async function POST(req: NextRequest) {
  const session = await getSession();
  const user = session.user;

  if (!user) {
    return NextResponse.json({ error: 'Not authenticated' }, { status: 401 });
  }

  const { service, username, password } = await req.json();

  if (!service || !username || !password) {
    return NextResponse.json({ error: 'Service, username, and password are required' }, { status: 400 });
  }

  const db = await openDb();
  try {
    // For a real app, password should be encrypted here before saving
    await db.run('INSERT INTO credentials (userId, service, username, password) VALUES ($1, $2, $3, $4)', [user.id, service, username, password]);
    return NextResponse.json({ message: 'Credential saved successfully' }, { status: 201 });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  } finally {
    await db.close();
  }
}
