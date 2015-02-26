import json

import kn.fotos.entities as fEs
from kn.base.http import JsonHttpResponse
from django.core.exceptions import PermissionDenied

def view(request):
    data = json.loads(request.REQUEST.get('data', {}))
    action = data.get('action')
    handler = ACTION_HANDLER_MAP.get(action,
                    ACTION_HANDLER_MAP[None])
    return JsonHttpResponse(handler(data, request))

def no_such_action(data, request):
    return {'error': 'No such action'}

def album_json(album, user):
    if not album.may_view(user):
        raise PermissionDenied

    children = album.list(user)
    json_children = []
    for child in children:
        entry = {'type': child._type,
                 'path': child.full_path,
                 'name': child.name,
                 'title': child.title}
        if child._type == 'foto':
            entry['largeSize'] = child.get_cache_size('large')
            entry['thumbnailSize'] = child.get_cache_size('thumb')
        elif child._type == 'album':
            album_foto = child.get_random_foto_for(user)
            if album_foto is not None:
                entry['thumbnailSize'] = album_foto.get_cache_size('thumb')
                entry['thumbnailPath'] = album_foto.full_path
        json_children.append(entry)

    current_album = album
    json_parents = {}
    while current_album is not None:
        json_parents[current_album.full_path] = current_album.title
        current_album = current_album.get_parent()

    return {'children': json_children,
            'parents': json_parents}

def entity_from_request(data):
    if 'path' not in data:
        return 'Missing path attribute'
    if not isinstance(data['path'], basestring):
        return 'path should be string'
    entity = fEs.by_path(data['path'])
    if entity is None:
        return 'Object not found'
    return entity

def _list(data, request):
    album = entity_from_request(data)
    if isinstance(album, basestring):
        return {'error': album}
    user = request.user if request.user.is_authenticated() else None
    return album_json(album, user)

def _set_title(data, request):
    if 'title' not in data:
        return {'error': 'missing title attribute'}
    if not isinstance(data['title'], basestring):
        return {'error': 'title should be string'}
    title = data['title'] or None

    album = entity_from_request(data)
    if isinstance(album, basestring):
        return {'error': album}

    user = request.user if request.user.is_authenticated() else None
    if not fEs.is_admin(user):
        raise PermissionDenied

    album.set_title(title)
    return {'Ok': True}

ACTION_HANDLER_MAP = {
        'list': _list,
        'set-title': _set_title,
        None: no_such_action,
        }

# vim: et:sta:bs=2:sw=4:
