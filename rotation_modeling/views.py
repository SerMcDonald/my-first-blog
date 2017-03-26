from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from .models import RotationModel
from django.utils import timezone

from .math_model import *
import json
# Create your views here.

def model_main(request):
    if request.GET.get('orbit_hight'):
        H = int(request.GET["orbit_hight"])
        m1 = int(request.GET["mas1"])
        m2 = int(request.GET["mas2"])
        L = int(request.GET["cab_len"])
        F = float(request.GET["thrust"])
        α = int(request.GET["ang_a"])
        γ = int(request.Get["ang_g"])
        rmm = RotationMathModel(H, m1, m2, L, F, α, γ)
        y0 = np.array([0, 0, 0, 0, 0, 0, 0])
        res, t = rmm.runge1(rmm.f, y0, 0, 3150)
        w=res[:,1]
        o=res[:,0]
        return render(request, 'rotation_modeling/build_model.html', {'mas': zip(t, w), 'mas2': zip(o, w)})
    return render(request, 'rotation_modeling/build_model.html', {'mas': zip([0, 0], [0, 0])})

def build_model(request):
    if request.GET.get('orbit_hight'):
        H = int(request.GET["orbit_hight"])
        m1 = int(request.GET["mas1"])
        m2 = int(request.GET["mas2"])
        L = int(request.GET["cab_len"])
        F = float(request.GET["thrust"])
        α = int(request.GET["ang_a"])
        γ = int(request.GET["ang_g"])
        rmm =RotationMathModel(H,m1,m2,L,F,α,γ)
        y0 = np.array([0, 0, 0, 0, 0, 0, 0])
        res, t = rmm.runge2(rmm.f, y0, 0, 3150)
        w=res[:,1]
        o=res[:,0]
        m1=[[x,y] for x,y in zip(t,w)]
        m2=[[x,y] for x,y in zip(o,w)]
        zip(o, w, t)
        T = [ rmm.TT(op,wp,0,0,tp) for op,wp,tp in zip(o, w, t)]
        m3 =[[x,y] for x,y in zip(t, T)]
        return JsonResponse({"mas1":m1, "mas2":m2, "mas3":m3});
    return "{'mas':'1'}"

def saved_models(request):
    models = RotationModel.objects.all();
    return  render(request, "rotation_modeling/saved_models.html", {'models':models})

@csrf_protect
def save_model(request):
    c = {}
    c.update(csrf(request))
    if request.is_ajax():
        if request.method == 'POST':
            data =json.loads(request.body)
            RotationModel.objects.create(name=data['name'], time_avel_data=data['time_avel_data'],
                                         ang_vel_data = data['ang_vel_data'], time_thrust_data = data['time_thrust_data'],
                                         comment = data['comment'], orbit_hight=data['orbit_hight'], cab_len = data['cab_len'],
                                         mas1=data['mas1'], mas2 = data['mas2'], thrust = data['thrust'], published_date = timezone.now())
    return HttpResponse("OK")


def saved_model_detail(request, pk):
    model = get_object_or_404(RotationModel, pk=pk)
    return render(request, 'rotation_modeling/saved_model_detail.html', {'model': model})