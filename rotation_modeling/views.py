from django.http import JsonResponse
from django.shortcuts import render
from .math_model import *
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
        return render(request, 'rotation_modeling/test.html', {'mas': zip(t,w), 'mas2': zip(o,w)} )
    return render(request,'rotation_modeling/test.html',{'mas': zip([0,0], [0,0])})

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
    return "{'mas':'1'}";