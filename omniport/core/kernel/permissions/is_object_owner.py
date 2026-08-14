from rest_framework.permissions import BasePermission


def _resolve(obj, dotted_path):
    """
    Safely walk a dotted attribute path from ``obj`` using getattr, returning
    None if any segment along the way is missing or None.
    :param obj: the object to start traversal from
    :param dotted_path: the dotted attribute path to resolve
    :return: the resolved value, or None if it cannot be resolved
    """

    current = obj
    for segment in dotted_path.split('.'):
        if current is None:
            return None
        current = getattr(current, segment, None)
    return current


class IsObjectOwner(BasePermission):
    """
    Object-level permission that grants access only when the requesting person
    owns the object.

    Ownership is resolved by comparing ``request.person`` against the first
    matching attribute in a list of candidate dotted paths on the object. A view
    may override the candidates by setting ``object_owner_fields`` on itself,
    e.g. ``object_owner_fields = ('student.person',)``.

    This closes broken-object-level-authorization (BOLA / CWE-639) on detail
    actions (retrieve/update/destroy), which invoke ``has_object_permission``
    via ``get_object()``. It must be combined with ``IsAuthenticated`` so that
    list/create actions - which do not call ``has_object_permission`` - remain
    gated too.
    """

    default_owner_fields = (
        'person',
        'student.person',
        'faculty_member.person',
        'user.person',
        'owner',
    )

    def has_object_permission(self, request, view, obj):
        request_person = getattr(request, 'person', None)
        if request_person is None:
            return False

        owner_fields = getattr(
            view, 'object_owner_fields', self.default_owner_fields
        )
        for field in owner_fields:
            owner = _resolve(obj, field)
            if owner is not None and owner == request_person:
                return True
        return False
