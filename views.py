from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.views import View
from ChromoGraph.chrofig import *
import os.path


class ChromoGraph(View):

    def get(self, request):
        form = UploadFileForm()
        filename = request.session.get('filename', 'nofile')

        if os.path.exists(os.getcwd() + '/ChromoGraph/static/' + filename):
            return render(request, "chrofig.html", {'form': form, 'filename': filename})

        return render(request, "index.html", {'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            resp = request.POST
            figure = ChromoFigure()

            figure.title = resp['title']
            figure.min_time = float(resp['min_time'])
            figure.max_time = float(resp['max_time'])
            fig, ax = figure.export(file)

            filename = (figure.title + '_' + request.COOKIES['sessionid']).replace(' ', '-')
            request.session['filename'] = f'{filename}.{resp["format"]}'
            fig.savefig(f'ChromoGraph/static/{filename}.{resp["format"]}', format=resp['format'])
            return redirect(request.path)
        else:
            form = UploadFileForm()
        return render(request, 'index.html', {'form': form})
