import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const payload = await request.json().catch(() => null);

  if (!payload || !payload.description || !payload.location || !payload.date) {
    return NextResponse.json({ ok: false, message: "Missing required fields." }, { status: 400 });
  }

  return NextResponse.json({ ok: true, message: "Sighting submitted to moderation queue." });
}
