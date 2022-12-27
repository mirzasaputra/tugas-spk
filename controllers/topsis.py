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
      A = np.array(df.iloc[0:,1:(len(W) + 1)].values)

      # set value K
      kriteria = df.iloc[0:,:1].values
      K = []
      for d in kriteria :
        K.append(d[0])

      K = np.array(K)
      A = np.transpose(A)
    
    Rij = calculateRij(A)
    R = normalisasiR(A, Rij)
    Y = normalisasiY(R, W)
    APositive = calculateAPositive(Y, L)
    ANegative = calculateANegative(Y, L)
    DAPositive = distanceAPositive(Y, APositive)
    DANegative = distanceANegative(Y, ANegative)
    finalResult = finalPreferensi(DAPositive, DANegative)
    finalResult = appendCandidateToResult(K, finalResult)
    finalResult = sorting(finalResult, 'desc')

    return jsonify({"data": finalResult})

def calculateRij(matriks) :
  result = []

  for i in range(matriks.shape[0]) :
    temp = 0

    for j in range(matriks[i].shape[0]) :
      temp += math.pow(float(matriks[i][j]), 2)

    result.append(math.sqrt(temp))
  
  return np.asarray(result)

def normalisasiR(matriks, Rij) :
  result = []
  matriks = matriks.transpose()

  for i in range(matriks.shape[0]) :
    val = []

    for j in range(matriks[i].shape[0]) :
      val.append(float(matriks[i][j]) / float(Rij[j]))

    result.append(val)

  return np.asarray(result)

def normalisasiY(matriks, weight) :
  result = []

  for i in range(matriks.shape[0]) :
    val = []

    for j in range(matriks[i].shape[0]) :
      val.append(float(matriks[i][j]) * float(weight[j]))

    result.append(val)
  
  return np.asarray(result)

def calculateAPositive(matriks, label) :
  matriks = matriks.transpose()
  
  if not matriks.shape[0] == label.shape[0] :
    print('Jumlah index array tidak sesuai')
    return

  result = []

  for i in range(matriks.shape[0]) :
    if label[i] == 'cost' :
      result.append(min(matriks[i]))
    else :
      result.append(max(matriks[i]))
    
  return np.asarray(result)

def calculateANegative(matriks, label) :
  matriks = matriks.transpose()
  
  if not matriks.shape[0] == label.shape[0] :
    print('Jumlah index array tidak sesuai')
    return

  result = []

  for i in range(matriks.shape[0]) :
    if label[i] == 'cost' :
      result.append(max(matriks[i]))
    else :
      result.append(min(matriks[i]))
    
  return np.asarray(result)

def distanceAPositive(matriks, APositive) :
  matriks = matriks.transpose()

  if not matriks.shape[0] == APositive.shape[0] :
    print('Jumlah index array tidak sesuai')
    return

  matriks = matriks.transpose()
  result = []
  
  for i in range(matriks.shape[0]) :
    temp = 0

    for j in range(matriks[i].shape[0]) :
      temp += math.pow(matriks[i][j] - APositive[j], 2)
    
    result.append(math.sqrt(temp))
  
  return np.asarray(result)

def distanceANegative(matriks, ANegative) :
  matriks = matriks.transpose()

  if not matriks.shape[0] == ANegative.shape[0] :
    print('Jumlah index array tidak sesuai')
    return

  matriks = matriks.transpose()
  result = []
  
  for i in range(matriks.shape[0]) :
    temp = 0

    for j in range(matriks[i].shape[0]) :
      temp += math.pow(ANegative[j] - matriks[i][j], 2)
    
    result.append(math.sqrt(temp))
  
  return np.asarray(result)

def finalPreferensi(DAPositive, DANegative) :
  if not DAPositive.shape[0] == DANegative.shape[0] :
    print('Jumlah index array tidak sesuai')
    return
  
  result = []

  for i in range(DANegative.shape[0]) :
    a = DANegative[i] + DAPositive[i]
    result.append(DANegative[i] / a)

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