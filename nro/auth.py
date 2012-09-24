import decorator
from flask import g, abort

@decorator.decorator
def require_inspect(f, *args, **kwargs):
	if not g.user.can_inspect():
		abort(403)

	return f(*args, **kwargs)

@decorator.decorator
def require_curate(f, *args, **kwargs):
	if not g.user.can_curate():
		abort(403)
	return f(*args, **kwargs)

@decorator.decorator
def require_merge(f, *args, **kwargs):
	if not g.user.can_merge():
		abort(403)
	return f(*args, **kwargs)

@decorator.decorator
def require_delete(f, *args, **kwargs):
	if not g.user.can_delete():
		abort(403)
	return f(*args, **kwargs)
