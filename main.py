import streamlit as st
import sklearn.datasets as sk
import pandas as pd
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

def methodofkeys(dict, search_iter):
    for iter1, iter2 in dict.items():
        if iter2 == search_iter:
            return iter1
def model_making(train_data,train_value,nooflayers,length,activation_function,c_r,optimizers,loss_function,metrics,epoch):
    model=keras.Sequential()
    model.add(tf.keras.Input(shape=(len(train_data[0]),)))
    for i in range(nooflayers):
        model.add(tf.keras.layers.Dense(length[i],activation=activation_function[i]))
    if(c_r=='c'):
        model.add(tf.keras.layers.Dense(len(train_value.value_counts())))
    elif(c_r=='r'):
        model.add(tf.keras.layers.Dense(1))
    
    model.compile(optimizer=optimizers,loss=loss_function,metrics=metrics)
    history=model.fit(train_data,train_value,epochs=epoch)
    return model,history

st.set_page_config(page_title='Neural Network Playground', page_icon='🏛️')
st.title("Neural Network Playground")
st.subheader('')
with st.expander('Dataset'):
    
    data_file=st.file_uploader("Upload A Dataset",accept_multiple_files=True)
    st.write("OR")
   
    datasets=dict({'None':None,'Boston Housing Dataset':sk.load_boston(),'Iris dataset':sk.load_iris(),'Diabetes datset':sk.load_diabetes(),'Wine Dataset':sk.load_wine(),'Linnerud Datset':sk.load_linnerud()})
    option=st.selectbox("Choose the preconceived datatset",datasets.keys())
    c_or_r=dict({'Classification':'c','Regression':'r'})
    c_r=st.radio('Type of dataset: ',c_or_r.keys())
    c_r=c_or_r[c_r]
    if  option=='None':
        st.error('No dataset detected')
    elif  option!='None':
        actual_data=datasets[option].data[:int(0.7*len(datasets[option].data)),:]
        actual_values=datasets[option].target[:int(0.7*len(datasets[option].data))]
    
nooflayers=st.number_input("No.of hidden layers",min_value=1)
length=[]
list_of_af=['elu','exponential','gelu','hard_sigmoid','linear','relu','selu','sigmoid','softmax','softplus','softsign','swish','tanh']
activation_function=[]
for i in range(nooflayers):
    with st.expander('Layer '+ str(i+1)):
        length.append(st.number_input("No of nodes of layer " +str(i+1),min_value=1))
        activation_function.append(st.selectbox('Activation Function of layer '+str(i+1),list_of_af))

list_of_optimizers=['SGD','Adadelta','Adam','Adagrad','Adamax','Ftrl','Nadam','RMSprop']
list_of_loss_func=dict({'mse': ' mse : Computes the mean squared error between labels and predictions.',
'binary_crossentropy': ' binary_crossentropy : Computes the binary crossentropy loss.',
'categorical_crossentropy': 'categorical_crossentropy : Computes the categorical crossentropy loss.',
'categorical_hinge': ' categorical_hinge : Computes the categorical hinge loss between y_true and y_pred.',
'cosine_similarity': 'cosine_similarity : Computes the cosine similarity between labels and predictions.',
'hinge': ' hinge : Computes the hinge loss between y_true and y_pred.',
'huber': ' huber : Computes Huber loss value.',
'kld': ' kld : Computes Kullback-Leibler divergence loss between y_true and y_pred.',
'log_cosh': ' log_cosh : Logarithm of the hyperbolic cosine of the prediction error.',
'mae': ' mae : Computes the mean absolute error between labels and predictions.',
'mape': ' mape : Computes the mean absolute percentage error between y_true and y_pred.',
'msle': ' msle : Computes the mean squared logarithmic error between y_true and y_pred.',
'poisson': ' poisson : Computes the Poisson loss between y_true and y_pred.',
'sparse_categorical_crossentropy': ' sparse_categorical_crossentropy : Computes the sparse categorical crossentropy loss.',
'squared_hinge': ' squared_hinge : Computes the squared hinge loss between y_true and y_pred'})
list_of_metrics_func=list_of_loss_func.copy()
list_of_metrics_func['top_k_categorical_accuracy']='top_k_categorical_accuracy : Computes how often targets are in the top K predictions.'
list_of_metrics_func['sparse_categorical_accuracy']='sparse_categorical_accuracy : Calculates how often predictions equal labels.'
list_of_metrics_func['sparse_top_k_categorical_accuracy']='sparse_top_k_categorical_accuracy :  Computes how often integer targets are in the top K predictions.'
list_of_metrics_func['categorical_accuracy']='categorical_accuracy(...): Calculates how often predictions match one-hot labels.'
Optimizers=st.selectbox('Optimizers',list_of_optimizers)
Loss_func=methodofkeys(list_of_loss_func,st.selectbox('Loss Function',list_of_loss_func.values()))
list_of_metrics_function=st.multiselect('Metrics for the model',list_of_metrics_func.values())
keys_of_metric_function=[methodofkeys(list_of_metrics_func,i) for i in list_of_metrics_function]
epoch=st.number_input("No. of Epoch",min_value=1)
if st.button('Run the given model'):
    k,history=model_making(actual_data,actual_values,nooflayers,length,activation_function,c_r,Optimizers,Loss_func,keys_of_metric_function,epoch)
    history = pd.DataFrame.from_dict(history.history)
    st.dataframe(history)
    val=k.evaluate(datasets[option].data[:int(0.2*len(datasets[option].data)),:],datasets[option].target[:int(0.2*len(datasets[option].data))],verbose=2)
    st.write(val)


    





