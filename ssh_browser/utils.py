def transform_path(path):
    components = path.split('/')
    result = []
    current_path = ''

    for component in components:
        current_path += component + '/'
        
        item = {'name': component, 'path': current_path[:-1]}
        
        result.append(item)

    return result
