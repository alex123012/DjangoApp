from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import ExelForm
from .exchange import DataFrame
import matplotlib.pyplot as plt
from scipy import stats
import os


class FileFieldView(FormView):

    form = ExelForm()  # Upload from from forms.py for template
    template_name = os.path.join("exelchange", "index.html")  # Basic template

    def get(self, request, **kwargs):
        # home = os.getcwd()
        # path = os.path.join(home, 'exelchange', 'static', 'media', 'graph.png')
        # img = path if os.path.exists(path) else None
        # print(img)
        check()
        return render(request, os.path.join("exelchange", "index.html"), {'form': self.form, 'img': 'graph.png'})

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        if request.FILES.get('file', None) is None:
            x = list(map(float, request.POST['x_coord'].split()))
            y = list(map(float, request.POST['y_coord'].split()))
            # df = DataFrame((x, y))
        appr = stats.linregress(x, y)
        a = round(appr.slope, 4)
        b = round(appr.intercept, 4)
        y1 = [a * i + b for i in x]
        label = f'{a}*x {b}' if b < 0 else f'{a}*x + {b}'
        fig = plt.figure()

        # Дабавляю один список axes
        ax = fig.add_subplot(111)
        # fig, ax = plt.subplots(1, 1,
        #                        figsize=(15, 10),
        #                        tight_layout=True)

        ax.plot(x, y, label='initial', color='black')
        ax.plot(x, y1, label=label, color='orange')
        plt.legend()
        check()
        fig.savefig(os.path.join('exelchange', 'static', 'media', 'graph'))
        return redirect(request.path)


def check():
    path = os.path.join('exelchange', 'static')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join('exelchange', 'static', 'media')
    if not os.path.exists(path):
        os.mkdir(path)