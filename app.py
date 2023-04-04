import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response

from uvicorn import run

app = FastAPI()


@app.get('/assets/{path}')
def assets(path):
    """Route for assets
    
        The defualt app.mount will return the content-type as plaintext while serving
        a javascript file, leading to the page nothing but blank.

        This route will return the correct content-type for javascript.
    """
    print('Assets')
    if not os.path.exists(f'frontend/dist/assets/{path}'):
        return {'error': 'Not Found'}

    with open(f'frontend/dist/assets/{path}', 'rb') as f:
        content = f.read()

    header = {'Content-Type': 'text/plain'}

    if path.endswith('.js'):
        header = {'Content-Type': 'application/javascript'}
    elif path.endswith('.css'):
        header = {'Content-Type': 'text/css'}
    elif path.endswith('.svg'):
        header = {'Content-Type': 'image/svg+xml'}
    else:
        # other file types if needed
        ...

    return Response(content=content, status_code=200, headers=header)


# Mount the static files that vite produces
# Make sure that following line is placed after the route for assets, in prevent of being overrided

# Make /dist as the root path, and reponse the index.html by default
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="dist")

if __name__ == "__main__":
    run('app:app', host='127.0.0.1', port=8888, reload=True)
