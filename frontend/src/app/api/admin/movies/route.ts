export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const page = searchParams.get('page') || '1';
    const limit = searchParams.get('limit') || '10';
    
    const response = await fetch(`http://localhost:8000/admin/movies?page=${page}&limit=${limit}`);
    const data = await response.json();
    
    return Response.json(data);
  } catch (error) {
    return Response.json({ error: 'Failed to fetch movies' }, { status: 500 });
  }
}