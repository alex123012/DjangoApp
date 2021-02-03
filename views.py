from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from ChromoGraph.chrofig import *
import os.path
import zipfile


class FileFieldView(FormView):
    form_class = FileFieldForm  # Upload from from forms.py for template
    template_name = os.path.join("ChromoGraph", "index.html")  # Basic template

    def get(self, request):
        if not request.COOKIES.get('sessionid', ''):  # set session cookie
            request.session.session_key()
        form = self.form_class  # Set variable for form for template
        filename = request.session.get('filenames', '')  # Import file name if exists (after POST)
        if filename:
            zipper = False
            if len(filename) > 1:
                zipper = zipgraph(request.COOKIES['sessionid'])  # Create zip archive with more than 1 graphs
            return render(request, os.path.join("ChromoGraph", "index.html"),
                          {'form': form, 'filename': filename, 'zip': zipper})

        return render(request, os.path.join("ChromoGraph", "index.html"), {'form': form})

    def post(self, request, *args, **kwargs):
        if not os.path.exists(os.path.join('ChromoGraph', 'static',  'media')):  # Create new folders for storing graphs
            os.mkdir(os.path.join('ChromoGraph', 'static',  'media'))
        if not os.path.exists(os.path.join('ChromoGraph', 'static', 'media',  request.COOKIES['sessionid'])):
            os.mkdir(os.path.join('ChromoGraph', 'static',  'media', request.COOKIES['sessionid']))

        form_class = self.get_form_class()
        form = self.get_form(form_class)  # Getting form for template
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
                filename += '.' + resp["format"]  # Creating unique path and filename in static/media/

                list_names = request.session.get('filenames', '')
                request.session['filenames'] = (list_names + [filename]) if list_names else [filename]
                fig.savefig(os.path.join('ChromoGraph', 'static', filename), format=resp['format'])  # Saving graph
            return redirect(request.path)
        else:
            return render(request, os.path.join("ChromoGraph", "index.html"), {'form': form})


def zipgraph(ide):
    cwd = os.getcwd()
    path = os.path.join('ChromoGraph', 'static', 'media')
    os.chdir(path)  # Changing cwd
    with zipfile.ZipFile(os.path.join(f'{ide}.zip'), 'w') as myzip:
        for root, _, files in os.walk(os.path.join(ide)):
            for file in files:
                myzip.write(os.path.join(root, file))
    os.chdir(cwd)
    return os.path.join('media', f'{ide}.zip')
