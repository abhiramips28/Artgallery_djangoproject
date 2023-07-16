from django.shortcuts import render, redirect, HttpResponse


def restricted_login(allowed=[]):
    def decorator(view):
        def wrapper_function(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed:
                return view(request, *args, **kwargs)
            else:
                return HttpResponse("You cannot view this page")

        return wrapper_function

    return decorator


def admin_or_user(view):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'users':
            return redirect('/for_users')

        if group == 'admin':
            return view(request, *args, **kwargs)

    return wrapper_function
