import os
from scipy.spatial.transform import Rotation as R
import re
import numpy as np

# HIERACHY

delete_line_list = [6, 7, 8, 9, 34,             # LHipJoint
                    35, 36, 37, 38, 63,         # RHipJoint
                    64, 65, 66, 67, 183,        # LowerBack
                    # Neck
                    76, 77, 78, 79, 94] + \
                    list(range(111, 129)) + [133] + \
                    list(range(154, 172)) + [176]
                    # LeftFingerBase, LeftHandIndex1, LThumb
                    # RightFingerBase, RightHandIndex1, RThumb
delete_line_list = (np.array(delete_line_list) - 1).tolist()


def delete_joint_hierachy(data, line_list):
    """HIERARCHY 부분의 불필요한 joint 삭제"""
    
    line_list.sort(reverse=True)
    for i in line_list:
        data.pop(i)

    return data

# MOTION

tmp = (np.array([3, 8, 13, 16]) - 1) * 3
pass_coord_list = np.append(tmp, np.append(tmp + 1, tmp + 2)).tolist()


def pass_coord(data, joint_idx_list):
    """삭제된 joint의 Euler coordinate를 뒤에 넘겨 더해 줌
        단, 끝에 있는 joint는 안 넘겨도 됨. """
    
    frame = []
    for j in range(data.index("MOTION\n") + 3, len(data)):
        frame.append(data[j].split(' ')[:-1])

    for i in range(len(frame)):
        for j in joint_idx_list:
            frame[i][j+3] = str(float(frame[i][j+3]) + float(frame[i][j]))
            
        temp = ''
        for k in range(len(frame[i])):
            if k == len(frame[i]) - 1:
                temp += frame[i][k] + '\n'
            else:
                temp += frame[i][k] + ' '

        data[data.index("MOTION\n") + i + 3] = temp
        

    return data


tmp = (np.array([3, 8, 13, 16, 23, 24, 25, 30, 31, 32]) - 1) * 3
delete_joint_list = np.append(tmp, np.append(tmp + 1, tmp + 2)).tolist()
print(delete_joint_list)

def delete_joint(data, joint_idx_list):
    """coodinate를 뒤에 넘긴 후, 
    MOTION 부분의 불필요한 joint를 삭제"""
    
    joint_idx_list.sort(reverse=True)
    
    frame = []
    for j in range(data.index("MOTION\n") + 3, len(data)):
        frame.append(data[j].split(' '))

    for i in range(len(frame)):
        for j in joint_idx_list:
            try:
                frame[i].pop(j)
            except:
                print("error!")
                print(len(frame[i]), j)
                exit(1)
            
        temp = ''
        for k in range(len(frame[i])):
            if k == len(frame[i]) - 1:
                temp += frame[i][k] + '\n'
            else:
                temp += frame[i][k] + ' '

        data[data.index("MOTION\n") + i + 3] = temp
        
    return data



def insert_spine(data):

    # spine1 의 y 값을 절반으로 바꾸어 줍니다.
    float_expr = "[-]?[0-9]+[\.][0-9]+"
    half_y = float(re.findall(float_expr, data[55])[1]) / 2
    target = "{float_expr} {float_expr} {float_expr}".format(float_expr=float_expr)
    content = "-0.000000 %f 0.000000" % half_y
    data[55] = re.sub(target, content, data[55])

    # spine2 를 추가합니다.
    data.insert(61, "            JOINT Spine2\n")
    data.insert(62, "            {\n")
    data.insert(63, "                OFFSET -0.000000 %f 0.000000\n" % half_y)
    data.insert(64, "                CHANNELS 3 Zrotation Yrotation Xrotation\n")
    data.insert(128, "            }\n")

    for i in range(data.index("MOTION\n") + 3, len(data)):
        l = data[i].split(' ')
        l.insert(30, "0.000000    0.000000    0.000000")
        data[i] = '    '.join(l)

    return data


try:
    os.mkdir('parsed')
except:
    pass

for filename in os.listdir():
    # ex) 001_0716001_001.vbh
    if re.match("\w+.bvh", filename):
        with open(filename) as f:
            data = list(f.readlines())
    else:
        continue  # if not bvh file -> pass


    # 함수 순서 바꾸면 안 됩니다.
    data = delete_joint_hierachy(data, delete_line_list)
    data = pass_coord(data, pass_coord_list)
    data = delete_joint(data, delete_joint_list)
    data = insert_spine(data)


    # 지정된 경로(default: /parsed)에 변환된 파일 저장
    with open('parsed/' + filename[:-4] + '_parsed.bvh', 'w') as f:
        f.writelines(data)

print('parsed')