from rest_framework import permissions


class AuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """ Создаем и настраиваем пермишены для сериализаторов """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin')


class AdminOrReadOnly(permissions.BasePermission):
    """ Создаем и настраиваем пермишены для сериализаторов """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin')


class AdminOrSuperUser(permissions.BasePermission):
    """ Создаем и настраиваем пермишены для сериализаторов """

    def has_permission(self, request, view):
        user = request.user
        return (
            (user.is_authenticated and user.role == 'admin')
            or (user.is_authenticated and user.is_staff is True)
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            (user.is_authenticated and user.role == 'admin')
            or (user.is_authenticated and user.is_staff is True)
        )


class AdminOrSuperUserOrModerator(permissions.BasePermission):
    """ Создаем и настраиваем пермишены для сериализаторов """

    def has_permission(self, request, view):
        user = request.user
        return (
            (user.is_authenticated and user.role == 'admin')
            or (user.is_authenticated and user.is_staff is True)
            or (user.is_authenticated and user.role == 'moderator')
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            (user.is_authenticated and user.role == 'admin')
            or (user.is_authenticated and user.is_staff is True)
            or (user.is_authenticated and user.role == 'moderator')
        )


class AdminOrAuthUser(permissions.BasePermission):
    """ Создаем и настраиваем пермишены для сериализаторов """

    def has_object_permission(self, request, view, obj):
        user = request.user

        return (
            (user.is_authenticated and user.role == 'admin')
            or (user.is_authenticated and user.is_staff is True)
            or user.is_authenticated
        )
