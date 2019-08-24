import numpy as np
import math

def remove_tail(serie, tail_size):
	if tail_size>0:
		return serie[:-tail_size]
	else:
		return serie[:]

def create_lagged_series(serie,qtd,lag_size=2):
	"""
	Baseado no Takens Embedding Theorem
	:param serie: uma serie temporal
	:param lag_size: tamanho do atraso, também conhecido como tau
	:param qtd: número de séries 
	:returns: uma lista de séries atrasadas 
	"""
	series=[]
	tail_size=(qtd-1)*lag_size
	
	for i in range(qtd):
		series.append(remove_tail(np.roll(serie, -i*lag_size),tail_size))

	# import ipdb;ipdb.set_trace()
	return series


def heaviside_step(v):
	ret=0
	if v>0 :
		ret=1

	return ret

def norm(a,b):

	s=0
	for i in range(len(a)):
		s+=(a[i]-b[i])**2

	return math.sqrt(s)




def correlation(series, r,n):
	
	s=len(series)
	somatorio=0
	for i in range(n):
		for j in range(n):
			ti=[]
			tj=[]
			for k in range(s):
				ti.append(series[k][i])
				tj.append(series[k][j])
			# print("ti",ti)
			# print("tj",tj)
				
			somatorio+=heaviside_step(r-norm(ti,tj))

	c=(2/float((n*(n-1))))+somatorio
	return c;



def is_like(a,b,limiar=0.5):
	k=abs(a-b)
	# print("k",k)
	# print("limiar",limiar)
	 
	return k<=abs(limiar)

def find_saturation(m_list,v_list):

	v_list_len=len(v_list)
	m_list_len=len(m_list)

	if v_list_len!=m_list_len:
		raise ValueError("listas de tamanhos diferentes")

	if v_list_len<2:
		raise ValueError("lista menor menor que 2 ")

	# print("m_list",m_list)
	# print("v_list",v_list)

	m=None
	v_old=v_list[0]

	for i,v in enumerate(v_list[1:]):
		
		if is_like(v,v_old,v/100.0):
			m=m_list[max(0,i-1)]
			
			break
		v_old=v_list[i]

	return m

def calc_attractor_dimension(serie,tau,dim_min=1,dim_max=20):
	"""
	Baseado no Grassberger-Procaccia Algorithm
	:param serie: uma serie temporal
	:returns: um float com a dimensão encontrada. Ou "-1" caso não encontre 
	"""
	m=dim_min
	limiar=0.5
	alpha=1
	is_attractor=False
	n=10
	v_list=[]
	m_list=list(range(1,dim_max+1))
	r=np.std(serie[:n])

	# print("r",r)
	for m in m_list:
		lagged_series=create_lagged_series(serie,m,lag_size=tau)

		c=correlation(lagged_series, r,n)

		v_list.append(math.log10(c)/math.log10(r))


	# print("v",v)
	# print("m",m_list)
	

	return find_saturation(m_list,v_list), m_list, v_list 





def find_lag(serie,max_tau=3000,limiar=0.05,delta_t=0.01):
	
	'''encontra o atraso baseado na função do correlação. O atraso escolhido
	é o primeiro zero encontrado para função de correlação.
	:param serie: serie temporal
	:param max: maximo de iterações
	'''
	cf_min=1
	tau_cf_min=0
	tau=1
	cf_list=[1.0]
	while tau<=max_tau:
		
		size=len(serie)-tau
		t=0
		a=0
		
		while t<size:
			a+=(serie[t]*serie[t+tau])
			t+=1
		
		a=a/float(size)
		t=0
		b=0

		while t<size:
			b+=serie[t]**2
			t+=1

		b=b/float(size)
		cf=(a/float(b))
		cf_list.append(cf)
		

		if cf_min>cf:
			cf_min=cf
			tau_cf_min=tau

		if cf<limiar or cf>cf_min+limiar:
			break;


		tau+=1


	return tau_cf_min*delta_t,cf_list