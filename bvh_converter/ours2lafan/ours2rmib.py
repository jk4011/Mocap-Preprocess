import os
from scipy.spatial.transform import Rotation as R
import re
import numpy as np
from tqdm import tqdm


def insert_spine(data):

    # spine1 의 y 값을 절반으로 바꾸어 줍니다.
    float_expr = "[-]?[0-9]+[\.][0-9]+"
    half_y = float(re.findall(float_expr, data[11])[1]) / 2
    target = "{float_expr} {float_expr} {float_expr}".format(float_expr=float_expr)
    content = "-0.000000 %f 0.000000" % half_y
    data[11] = re.sub(target, content, data[11])

    # spine2 를 추가합니다.
    data.insert(13, "        JOINT Spine2\n")
    data.insert(14, "        {\n")
    data.insert(15, "            OFFSET -0.000000 %f 0.000000\n" % half_y)
    data.insert(16, "            CHANNELS 3 Zrotation Yrotation Xrotation\n")
    data.insert(80, "        }\n")

    for i in range(data.index("MOTION\n") + 3, len(data)):
        l = data[i].split('    ')
        l.insert(9, "0.000000    0.000000    0.000000")
        data[i] = '    '.join(l)

    return data


def change_joint_order(data):

    # HIERARCHY 순서 변경
    indice = np.arange(5)                  # [0:4] -> [0:4]
    indice = np.append(indice, np.arange(82, 106))   # [82:106] -> [5:29]
    indice = np.append(indice, np.arange(106, 130))  # [106:130] -> [29:53]
    indice = np.append(indice, np.arange(5, 82))     # [5:82] -> [53:130]

    hierachy_data = np.array(data[:130])
    hierachy_data = hierachy_data[indice]
    data[:130] = hierachy_data.tolist()

    # MOTION 순서 변경
    tmp = list(range(2))
    tmp = tmp + list(range(15, 19))
    tmp = tmp + list(range(19, 23))
    tmp = tmp + list(range(2, 15))

    indice = np.arange(0)
    for i in tmp:
        indice = np.append(indice, [3*i, 3*i+1, 3*i+2])
    
    for i in range(data.index("MOTION\n") + 3, len(data)):
        l = np.array(data[i].split('    ')[:-1])
        l = l[indice].tolist()
        data[i] = '    '.join(l) + '    \n'

    return data


def change_rotation_ZXY_to_ZYX(data):
    
    # HIERARCHY 변환 (ZXY->ZYX)
    for i in range(0, data.index("MOTION\n")):
        # Zrotation Xrotation Yrotation -> Zrotation Yrotation Xrotation
        if re.search("Zrotation Xrotation Yrotation", data[i]):
            data[i] = re.sub("Zrotation Xrotation Yrotation", "Zrotation Yrotation Xrotation", data[i])
        
        # At "End Site", -14.752577 0.000000 0.000000 -> 0.000000 0.000000 0.000000
        if re.search("End Site", data[i]):
            float_expr = "[-]?[0-9]+[\.][0-9]+"
            data[i+2] = re.sub("{float_expr} {float_expr} {float_expr}".format(float_expr=float_expr), 
                                "0.000000 0.000000 0.000000", data[i+2])
    
    
    # MOTION 변환 (ZXY->ZYX)
    frame = []

    for j in range(data.index("MOTION\n") + 3, len(data)):
        frame.append(data[j].split('    ')[:-1])

    for i in range(len(frame)):
        for j in range(3, len(frame[0]), 3):
            zxy = [float(frame[i][j]), float(frame[i][j + 1]), float(frame[i][j + 2])]
            r = R.from_euler('zyx', zxy, degrees=True)
            zyx = r.as_euler('zxy', degrees=True)
            frame[i][j], frame[i][j + 1], frame[i][j + 2] = [str(i) for i in zyx]

        temp = ''
        for k in range(len(frame[i])):
            if k == len(frame[i]) - 1:
                temp += frame[i][k] + '\n'
            else:
                temp += frame[i][k] + '    '

        data[data.index("MOTION\n") + i + 3] = temp
        
    return data




try:
    os.mkdir('converted')
except:
    pass

file_names = os.listdir()

for filename in tqdm(file_names):
    # ex) 001_0716001_001.vbh
    if re.match("\d+_\d+_\d+\.bvh", filename):  
        with open(filename) as f:
            data = list(f.readlines())
    else:
        continue  # if not bvh file -> pass

    
    # 함수 순서 바꾸면 안 됩니다.
    data = insert_spine(data)
    data = change_joint_order(data)
    data = change_rotation_ZXY_to_ZYX(data)
    

    # 지정된 경로(default: /converted)에 변환된 파일 저장
    with open('converted/' + filename[:-4] + '_converted.bvh', 'w') as f:
        f.writelines(data)

    print('converted: {}'.format(filename))
