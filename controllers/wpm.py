import json
import pandas as pd
import numpy as np
from flask import jsonify

# create main function
def main() :
    # read data.json
    file = open('data.json', 'r')
    data = json.load(file)
    
    # set value L
    L = np.array(data['L'])
    # set value W
    W = np.array(data['W'])
    if data['file'] == "" :
      # set value A
      A = np.array(data['A'])

      # set value K
      K = np.array(data['K'])
    else :
      # set value A
      path = data['file']
      df = pd.read_csv(path)
      A = np.array(df.iloc[:7,1:(len(W) + 1)].values)

      # set value K
      kriteria = df.iloc[:7,:1].values
      K = []
      for d in kriteria :
        K.append(d[0])

      K = np.array(K)

    A = np.transpose(A)

    # calling all function to execute
    W = validationPriority(L, W)
    normA = countWithWeight(A, W)
    S = calculateVectorS(normA)
    V = calculateVectorV(S)
    result = appendLabel(K, V)
    result = sorting(result, data['sorting'])

    return jsonify({"data": result})



# create validationPriority function
def validationPriority(label, weight) :
  if not label.shape[0] == weight.shape[0] :
    print('Input yang dimasukkan tidak sesuai')
    return
  
  result = []
  count = 0

  for i in range(weight.shape[0]) :
    count += float(weight[i])

  for i in range(weight.shape[0]) :
    if label[i] == 'benefit' :
      result.append(float(weight[i]) / count)
    elif label[i] == 'cost' :
      result.append((float(weight[i]) / count)* -1)
    
  return np.array(result)

# create countWithWeight function
def countWithWeight(data, weight) :
  if not data.shape[0] == weight.shape[0] :
    print('Input yang dimasukkan tidak sessuai')
    return

  data = np.transpose(data)
  result = []
  val = []

  for i in range(data.shape[0]) :
    for j in range(data[i].shape[0]) :
      val.append(pow(float(data[i][j]), float(weight[j])))

    result.append(val)
    val = []

  return np.array(result)

# create calculateVectorS function
def calculateVectorS(data) :
  result = []

  for i in range(data.shape[0]) :
    temp = 0
    for j in range(data[i].shape[0]) :
      if temp == 0 :
        temp += float(data[i][j])
      else :
        temp *= float(data[i][j])
    
    result.append(temp)
  
  return np.array(result)

# create calculateVectorV function
def calculateVectorV(data) :
  result = []

  for i in range(data.shape[0]) :
    temp = 0
    for j in range(data.shape[0]) :
      temp += float(data[j])
    
    result.append(float(data[i]) / temp)

  return np.array(result)

# create appendLabel function
def appendLabel(K, data) :
  result = []

  for i in range(data.shape[0]) :
    result.append([K[i], data[i]])
  
  return result

# create sorting function
def sorting(data, dir) :
  for i in range(len(data)) :
    for j in range(len(data) - i - 1) :
      if dir == 'asc' :
        if data[j][1] > data[j +  1][1] :
          data[j], data[j + 1] = data[j + 1], data[j]
      elif dir == 'desc' :
        if data[j][1] < data[j +  1][1] :
          data[j], data[j + 1] = data[j + 1], data[j]
      

  return data