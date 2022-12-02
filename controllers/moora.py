import json
import pandas as pd
import numpy as np
import math
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
      A = np.transpose(A)

      # convert data type to float
      data = []
      for i in range(A.shape[0]) :
          temp = []
          for j in range(A[i].shape[0]) :
              temp.append(float(A[i][j]))

          data.append(temp)
      
      # replace value variable A
      A = np.array(data)
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
    
    norm = normalizationMoora(A)
    optimalization = optimalizationAttributeValue(norm, W)
    Yi = calculateYiValue(optimalization, L)
    result = appendCandidateToResult(K, Yi)
    final_result = sorting(result, 'desc')

    return jsonify({"data": final_result})

def normalizationMoora(matrix) :
  result = []

  for i in range(matrix.shape[0]) :
    val = []
    sum_row = sum([pow(x, 2) for x in matrix[i]])

    for j in range(matrix[i].shape[0]) : 
      temp = float(matrix[i][j]) / math.sqrt(sum_row)
      val.append(temp)

    result.append(val)

  result = np.asarray(result)
  return result.transpose()

def optimalizationAttributeValue(matrix, W) :
  result = []

  for i in range(matrix.shape[0]) :
    val = []

    for j in range(matrix[i].shape[0]) :
      temp = float(matrix[i][j]) * float(W[j])
      val.append(temp)
    
    result.append(val)

  result = np.asarray(result)
  return result 

def calculateYiValue(matrix, L) :
  result = []

  for i in range(matrix.shape[0]) :
    max = []
    min = []

    for j in range(matrix[i].shape[0]) :
      if L[j] == 'benefit' :
        max.append(matrix[i][j])
      else :
        min.append(matrix[i][j])

    result.append(sum(max) - sum(min))
  
  return np.asarray(result)

def appendCandidateToResult(candidate, data) :
  if not candidate.shape[0] == data.shape[0] :
    print('Input kandidat tidak valid!')
    return

  result = []
  for i in range(candidate.shape[0]) :
    temp = []
    temp.append(candidate[i])
    temp.append(data[i])
    result.append(temp)

  return result

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