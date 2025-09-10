from cloudinary.uploader import upload

def handle_file_upload(request, pathname='image', folder='marcus_uploads'):
    data = request.data.dict()

    if isinstance(data.get(pathname), str):
        return request.data

    elif request.FILES.get(pathname, None):
        res = upload(request.FILES[pathname], folder=folder)
        return { **data, pathname: res['secure_url'] }

    else:
        return request.data
