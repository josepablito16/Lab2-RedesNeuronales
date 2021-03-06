from scipy.optimize import minimize
import numpy as np
import mnist_reader
from redNeuronal import *
import pickle



#Constantes
'''
Factor por el que se divide para
que no baje tan rapido la sigmoide
'''
NORMALIZAR=1000.0

#Cantidad de neuronas en la
#Capa oculta
NEURONAS_OCULTAS=130

#Neuronas en la capa salida
NEURONAS_SALIDA=10


#Lectura de datos
print("Lectura de datos...")
X_train, y_train = mnist_reader.load_mnist ( './data/fashion' , kind = 'train' )
X_test, y_test = mnist_reader.load_mnist ( './data/fashion' , kind = 't10k' )


#Proceso de datos
print("Proceso de datos...")
'''
Se leen los datos y se dividen por 
NORMALIZAR
'''
# X es la data de 28x28
# Info de cada pixel
X=X_train/NORMALIZAR

m,n=X.shape

#Y son las labels de cada imagen
y=y_train.reshape(m,1)

Y=(y==np.array(range(10))).astype(int)

print("Se construye el modelo...")
#Se construye el modelo
theta_shapes=np.array([
	[NEURONAS_OCULTAS,n+1],
	[NEURONAS_SALIDA,NEURONAS_OCULTAS+1]
	])

#Thetas iniciales
flat_thetas=flatten_list_of_arrays([
	np.random.rand(*theta_shape)/100
	for theta_shape in theta_shapes
	])

print("Se entrena el modelo...")
#Optimizando
result=minimize(
	fun=cost_function,
	x0=flat_thetas,
	args=(theta_shapes,X,Y),
	method='L-BFGS-B',
	jac=back_propagation,
	options={'disp':True,'maxiter':1000}

	)

print("Modelo entrenado! ")
modelo=open('modeloFinal','wb')
pickle.dump(result.x,modelo)

modelo.close()

