
import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/session';

export async function GET(req: NextRequest) {
  const session = await getSession();
  session.destroy();
  // Redirect to login page
  return NextResponse.redirect(new URL('/login', req.url));
}
