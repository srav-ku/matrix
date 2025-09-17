export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;
    
    if (!file) {
      return Response.json({ error: 'No file provided' }, { status: 400 });
    }

    const backendFormData = new FormData();
    backendFormData.append('file', file);
    
    const response = await fetch('http://localhost:8000/admin/movies/upload-csv', {
      method: 'POST',
      body: backendFormData
    });
    
    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    return Response.json({ error: 'Upload failed' }, { status: 500 });
  }
}