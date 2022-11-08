import json
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
    # set value A
    A = np.array(data['A'])
    A = np.transpose(A)
    # set value K
    K = np.array(data['K'])

    # convert data type to float
    data = []
    for i in range(A.shape[0]) :
        temp = []
        for j in range(A[i].shape[0]) :
            temp.append(float(A[i][j]))

        data.append(temp)
    
    # replace value variable A
    A = np.array(data)

    norm_result = validationPriority(L, A)
    result = calculateSaw(norm_result, W)
    remap_result = appendCandidateToResult(K, result)
    final_result = sorting(remap_result, 'desc')

    return jsonify({"data": final_result})

def validationPriority(label, data) :
  if not label.shape[0] == data.shape[0] :
    print('Input yang dimasukkan tidak valid!')
    return 

  val = []
  result = []

  for i in range(data.shape[0]) :
    if label[i] == 'benefit' :
      for j in range(data[i].shape[0]) :
        temp = float(data[i][j]) / np.max(data[i])
        val.append(temp)
    elif label[i] == 'cost' :
      for j in range(data[i].shape[0]) :
        temp =  np.min(data[i]) / float(data[i][j])
        val.append(temp)
      
    result.append(val)
    val = []
  
  return np.array(result)

def calculateSaw(data, weight) :
  if not weight.shape[0] == data.shape[0] :
    print('Input yang dimasukkan tidak valid!')
    return

  temp_array = []
  val = []
  result = []

  data = np.transpose(data)

  for i in range(data.shape[0]) :
    for j in range(data[i].shape[0]) :
      temp = float(data[i][j]) * float(weight[j])
      temp_array.append(temp)

    val.append(temp_array)
    temp_array = []

    saw = np.sum(val)
    result.append(saw)
    val = []

  return np.array(result)

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