import os, re
from bvh_converter import BvhConverter

try:
    os.mkdir('converted')
except:
    pass

for filename in os.listdir():
    if not re.match("\w+.bvh", filename):
        continue

    data = BvhConverter(filename)

    data.delete_joint("Spine2")
    data.rename_joint({"Neck": "Neck1"})

    data.insert_parent_joint("LeftUpLeg", "LHipJoint", loc="same")
    data.insert_parent_joint("RightUpLeg", "RHipJoint", loc="same")
    data.insert_parent_joint("Spine", "LowerBack", loc="same")
    data.insert_parent_joint("Neck1", "Neck", loc="same")

    data.insert_child_joint("LeftHand", "LeftFingerBase", loc="same")
    data.insert_child_joint("LeftFingerBase", "LeftHandIndex1", loc="same")
    data.insert_child_joint("LeftHand", "LThumb", idx=23, loc="same")
    data.insert_child_joint("RightHand", "RightFingerBase", loc="same")
    data.insert_child_joint("RightFingerBase", "RightHandIndex1", loc="same")
    data.insert_child_joint("RightHand", "RThumb", idx=30, loc="same")

    data.save("converted/" + filename)


