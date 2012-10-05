from flask import render_template
from flask.views import View

class BaseIndexView(View):

    def __init__(self):
        self.class_name = self.__class__.__name__

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

class IndexView(BaseIndexView):

    def get_template_name(self):
        return 'home.html'
