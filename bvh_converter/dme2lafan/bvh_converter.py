import numpy as np
import re, os, ntpath

channelmap = {"Xrotation": "x", "Yrotation": "y", "Zrotation": "z"}

class Anim(object):
    """
    A very basic animation object
    """

    def __init__(self, rotation, pos, offsets, parents, bones, meta_data):
        """
        :param rotation: local angular coordinate
        :param pos: local positions tensor
        :param offsets: local joint offsets
        :param parents: bone hierarchy
        :param bones: bone names
        """
        self.rotation = rotation
        self.pos = pos
        self.offsets = offsets
        self.parents = parents
        self.bones = bones
        self.meta_data = meta_data

    def save(self):
        indents = {-1: -1}
        for i, parent in enumerate(self.parents):
            indents[i] = indents[parent] + 1
        
        
        data = []
        prev_indent = 0
        for idx, bone in enumerate(self.bones):
            if bone == "Hips":
                data += [
                    "HIERARCHY", 
                    "ROOT Hips", 
                    "{",
                    "    OFFSET 0.000000 0.000000 0.000000",
                    "    CHANNELS 6 Xposition Yposition Zposition Zrotation Yrotation Xrotation"
                ]
            else:
                indent = indents[idx]
                if prev_indent > indent:
                    data += [
						(prev_indent+1) * "    " + "End Site",
						(prev_indent+1) * "    " + "{",
						(prev_indent+1) * "    " + "	OFFSET 0.000000 0.000000 0.000000",
						(prev_indent+1) * "    " + "}"
                    ]
                    for i in range(prev_indent, indent-1, -1):
                        data += [i * "    " + "}"]

                data += [
                    indent * "    " + f"JOINT {bone}",
                    indent * "    " + "{",
                    indent * "    " + "    OFFSET " + " ".join([str(i) for i in self.offsets[idx]]),
                    indent * "    " + "    CHANNELS 3 Zrotation Yrotation Xrotation"
                ]
                prev_indent = indent
        
        data += [
            (prev_indent+1) * "    " + "End Site",
            (prev_indent+1) * "    " + "{",
            (prev_indent+1) * "    " + "	OFFSET 0.000000 0.000000 0.000000",
            (prev_indent+1) * "    " + "}"
        ]
        for i in range(prev_indent, -1, -1):
            data += [i * "    " + "}"]

        data += ["MOTION"]
        data += self.meta_data
        
        length = self.rotation.shape[0]
        rotation = self.rotation.reshape(length, -1)
        root_pos = self.pos.reshape(length, -1)[:, :3]


        for i in range(length):
            data += ["    ".join([str(j) for j in root_pos[i]]) + "    " +
                     "    ".join([str(j) for j in rotation[i]])]
        
        for i in range(len(data)):
            if data[i][-1] != "\n":
                data[i] += "\n"
            
        with open('test.bvh', 'w') as f:
            f.writelines(data)
                    
    def 


def read_bvh(filename, start=None, end=None, order=None):
    """
    Reads a BVH file and extracts animation information.

    :param filename: BVh filename
    :param start: start frame
    :param end: end frame
    :param order: order of euler rotations
    :return: A simple Anim object conatining the extracted information.
    """

    f = open(filename, "r")

    i = 0
    active = -1
    end_site = False

    names = []
    orients = np.array([]).reshape((0, 4))
    offsets = np.array([]).reshape((0, 3))
    parents = np.array([], dtype=int)
    meta_data = []

    # Parse the  file, line by line
    for line in f:

        if "HIERARCHY" in line:
            continue
        if "MOTION" in line:
            continue

        rmatch = re.match(r"ROOT (\w+)", line)
        if rmatch:
            names.append(rmatch.group(1))
            offsets = np.append(offsets, np.array([[0, 0, 0]]), axis=0)
            orients = np.append(orients, np.array([[1, 0, 0, 0]]), axis=0)
            parents = np.append(parents, active)
            active = len(parents) - 1
            continue

        if "{" in line:
            continue

        if "}" in line:
            if end_site:
                end_site = False
            else:
                active = parents[active]
            continue

        offmatch = re.match(
            r"\s*OFFSET\s+([\-\d\.e]+)\s+([\-\d\.e]+)\s+([\-\d\.e]+)", line
        )
        if offmatch:
            if not end_site:
                offsets[active] = np.array([list(map(float, offmatch.groups()))])
            continue

        chanmatch = re.match(r"\s*CHANNELS\s+(\d+)", line)
        if chanmatch:
            channels = int(chanmatch.group(1))
            if order is None:
                channelis = 0 if channels == 3 else 3
                channelie = 3 if channels == 3 else 6
                parts = line.split()[2 + channelis : 2 + channelie]
                if any([p not in channelmap for p in parts]):
                    continue
                order = "".join([channelmap[p] for p in parts])
            continue

        jmatch = re.match("\s*JOINT\s+(\w+)", line)
        if jmatch:
            names.append(jmatch.group(1))
            offsets = np.append(offsets, np.array([[0, 0, 0]]), axis=0)
            orients = np.append(orients, np.array([[1, 0, 0, 0]]), axis=0)
            parents = np.append(parents, active)
            active = len(parents) - 1
            continue

        if "End Site" in line:
            end_site = True
            continue

        fmatch = re.match("\s*Frames:\s+(\d+)", line)
        if fmatch:
            meta_data += [line]
            if start and end:
                fnum = (end - start) - 1
            else:
                fnum = int(fmatch.group(1))
            positions = offsets[np.newaxis].repeat(fnum, axis=0)
            rotations = np.zeros((fnum, len(orients), 3))
            continue

        fmatch = re.match("\s*Frame Time:\s+([\d\.]+)", line)
        if fmatch:
            meta_data += [line]
            frametime = float(fmatch.group(1))
            continue

        if (start and end) and (i < start or i >= end - 1):
            i += 1
            continue

        for j in range(8,0,-1):
            if re.search(j * " ", line):
                break
        dmatch = line.strip().split(j * " ")

        if dmatch:
            data_block = np.array(list(map(float, dmatch)))
            N = len(parents)
            fi = i - start if start else i
            if channels == 3:
                positions[fi, 0:1] = data_block[0:3]
                rotations[fi, :] = data_block[3:].reshape(N, 3)
            elif channels == 6:
                data_block = data_block.reshape(N, 6)
                positions[fi, :] = data_block[:, 0:3]
                rotations[fi, :] = data_block[:, 3:6]
            elif channels == 9:
                positions[fi, 0] = data_block[0:3]
                data_block = data_block[3:].reshape(N - 1, 9)
                rotations[fi, 1:] = data_block[:, 3:6]
                positions[fi, 1:] += data_block[:, 0:3] * data_block[:, 6:9]
            else:
                raise Exception("Too many channels! %i" % channels)

            i += 1

    f.close()

    # rotations = utils.euler_to_quat(np.radians(rotations), order=order)
    # rotations = utils.remove_quat_discontinuities(rotations)

    return Anim(rotations, positions, offsets, parents, names, meta_data)

data = read_bvh("jump_n_parsed.bvh")

data.save()


