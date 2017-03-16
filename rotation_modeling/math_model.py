from math import *
import matplotlib.pyplot as plt
import numpy as np

class RotationMathModel:

    def __init__(self, H, m1, m2, L, F, α, γ):
        rounding =3 #Число знаков после запятой
        self.μ = 398600 #Гравитационный параметр Земли
        self.H =H#Высота круговой орбиты км
        self.Re = 6371.02 #Средний радиус Земли
        self.m1 = m1
        self.m2 = m2
        self.Ror = self.Re + self.H #Радиус орбиты
        self.Vor = sqrt(self.μ/self.Ror) #Скорость базового КА
        self.ωor = self.Vor / self.Ror #Угловая скорость движения базового аппарата по орбите
        self.θ0=0; self.β0=0 #Начальный угол положения троссовой системы координат относительно орбитальной
        self.ω0 = 0
        self.L0 = L #Начальная длина троса
        self.dL = 0 #Скорость развертывания троса
        self.T = (2*pi) / self.ωor #Период обращения вокруг Земли
        self.Fmax = F #Максимальная сила тяги двигателя, Н
        self.tp= (40* pi)/(self.ωor * sqrt(3))
        self.γ =0; self.α = α*pi/180 #Углы силы тяги
        self.Je = ((self.m1*self.m2)/(self.m1+self.m2))*(self.L0**2)
        self.me = self.m1*self.m2/(self.m1+self.m2)

    def F1(self,ωθ, t):
        return self.Fmax if(ωθ>=0) else 0

    def F(self,ωθ, t): #Cила тяги
        return self.F1(ωθ, t) if(t<=self.tp) else 0

    def Mθ(self,ωθ, t): #Момент силы
        return self.F(ωθ, t)*sin(self.α)*cos(self.γ)*self.L0

    def Mβ(self,ωθ, t): #Момент силы
        return self.F(ωθ, t)*self.L0*sin(self.γ)

    def FL(self, ωθ, t): #Сила пар
        return self.F(ωθ, t)*cos(self.α)*cos(self.γ)

    def dωθ(self, θ,ωθ,L, v, t):
        return -2*(self.dL/self.L0)*(ωθ+self.ωor) - 1.5*(self.ωor**2)*sin(2*θ) + (self.Mθ(ωθ, t)/self.Je)

    def dωθ_β(self, θ, ωθ, β, ωβ, t):
        return -2 * (self.dL / self.L0) * (ωθ + self.ωor*cos(β)) + 0.5*self.ωor**2*sin(2*θ)*sin(β)**2 - 0.5*ωβ**2*sin(2*θ) + 2*self.ωor*ωβ*cos(θ)*sin(β)  - 1.5 * (self.ωor ** 2) * sin(2 * θ) + (self.Mθ(ωθ, t) / self.Je)

    def dωβ(self, θ, ωθ, β, ωβ, t):
        return -2 * (self.dL / self.L0) * (ωβ + sin(β)*self.ωor*tan(θ))+2*ωβ*ωθ*tan(θ) - 2*self.ωor*ωθ*sin(β) - 2*(self.ωor**2)*sin(2*β) + self.Mβ(ωθ,t)/self.Je

    def TT(self, θ, ωθ, β, ωβ, t): #Сила натяжения троса
        return self.L0*self.me*(ωθ**2+2*ωθ*self.ωor*cos(β)-(self.ωor**2)*(cos(θ)**2)*(sin(β)**2) + (ωβ**2)*(cos(θ)**2)+ self.ωor*ωβ*sin(β)*sin(2*θ) + 3*(self.ωor**2)*(cos(θ)**2)*(cos(β)**2)) + self.FL(ωθ, t)

    def f(self, y, t): #система уравнений
        return np.array([y[1], self.dωθ(y[0],y[1],0,0,t), y[3], self.dωθ_β(y[2],y[3],y[4],y[5],t), y[5], self.dωβ(y[2],y[3],y[4],y[5],t), 0])

    def runge(f, y0, t0, tmax, n):
        h = (tmax - t0) / float(n)
        res=np.zeros((n+1, np.size(y0)))
        tr = np.zeros(n+1)
        tr[0]=t0
        y=y0
        t=t0
        for j in range(len(y)):
            res[0,j] = y[j]
        for i in range(1, n + 1):
            k1 = f(y, t)
            k2 = f(y + 0.5 * h * k1, t + 0.5 * h)
            k3 = f(y + 0.5 * h * k2, t + 0.5 * h)
            k4 = f(y + h * k3, t + h)
            y = y + (h/6)*(k1+2*k2+2*k3 +k4)
            t+=h
            tr[i] = t
            for j in range(len(y)):
                res[i][j] = y[j]
        return res, tr

    def runge1(self, f, y0, t0, n):
        h = 5
        res=np.zeros((n+1, np.size(y0)))
        tr = np.zeros(n+1)
        tr[0]=t0
        y=y0
        t=t0
        for j in range(len(y)):
            res[0,j] = y[j]
        i=1
        while i<n+1:#y[0]<pi:
            k1 = f(y, t)
            k2 = f(y + 0.5 * h * k1, t + 0.5 * h)
            k3 = f(y + 0.5 * h * k2, t + 0.5 * h)
            k4 = f(y + h * k3, t + h)
            y = y + (h/6)*(k1+2*k2+2*k3 +k4)
            t+=h
            tr[i] = t
            for j in range(len(y)):
                res[i][j] = y[j]
            i+=1
        return res, tr

    def runge2(self, f, y0, t0, n):
        h = 5
        res=[]
        tr = []
        tr.append(t0)
        y=y0
        t=t0
        res.append([])
        for j in range(len(y)):
            res[0].append(y[j])
        i=1
        while y[0]<pi:
            k1 = f(y, t)
            k2 = f(y + 0.5 * h * k1, t + 0.5 * h)
            k3 = f(y + 0.5 * h * k2, t + 0.5 * h)
            k4 = f(y + h * k3, t + h)
            y = y + (h/6)*(k1+2*k2+2*k3 +k4)
            t+=h
            tr.append(float(t))
            res.append([])
            for j in range(len(y)):
                res[i].append(y[j])
            i+=1
        return np.array(res), np.array(tr)

# y0= np.array([0,0,0,0,0,0,0])
# rmm=RotationMathModel()
# r, t= rmm.runge2(f, y0, 0, 10000, 3150)
# t=r[:,0]
# w=r[:,1]
# print(w[100])
# # plt.plot(t,w)
# # plt.grid()
# # plt.show()
# # print(tp)