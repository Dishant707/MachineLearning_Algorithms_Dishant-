
import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/session';
import { openDb } from '@/lib/db';

export async function DELETE(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getSession();
  const user = session.user;

  if (!user) {
    return NextResponse.json({ error: 'Not authenticated' }, { status: 401 });
  }

  const db = await openDb();
  try {
    const credential = await db.get('SELECT * FROM credentials WHERE id = $1 AND userId = $2', [id, user.id]);
    if (!credential) {
      return NextResponse.json({ error: 'Credential not found' }, { status: 404 });
    }

    await db.run('DELETE FROM credentials WHERE id = $1', [id]);
    return NextResponse.json({ message: 'Credential deleted successfully' });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  } finally {
    await db.close();
  }
}
