from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from ChromoGraph.chrofig import *
import os.path


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = os.path.join("ChromoGraph", "index.html")

    def get(self, request):
        form = self.form_class
        filename = request.session.get('filenames', '')
        url = request.COOKIES['sessionid']
        if filename:
            del request.session['filenames']
            return render(request, os.path.join("ChromoGraph", "index.html"),
                          {'form': form, 'filename': filename})

        return render(request, os.path.join("ChromoGraph", "index.html"), {'form': form})

    def post(self, request, *args, **kwargs):
        if not os.path.exists(os.path.join('ChromoGraph', 'static',  request.COOKIES['sessionid'])):
            os.mkdir(os.path.join('ChromoGraph', 'static',  'media', request.COOKIES['sessionid']))
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        resp = request.POST
        if form.is_valid():
            for file in files:

                figure = ChromoFigure()
                figure.title = resp['title'] if resp['title'] and len(files) == 1 else file
                figure.min_time, figure.max_time = float(resp['min_time']), float(resp['max_time'])
                fig, ax = figure.export(file)

                filename = os.path.join('media', request.COOKIES['sessionid'],
                                        (str(figure.title) + '_').replace('. ', '-'))
                filename += '.' + resp["format"]
                list_names = request.session.get('filenames', '')
                request.session['filenames'] = (list_names + [filename]) if list_names else [filename]
                fig.savefig(os.path.join('ChromoGraph', 'static', filename), format=resp['format'])
            return redirect(request.path)
        # else:
        #     return render(request, os.path.join("ChromoGraph", "index.html"), {'form': form})
