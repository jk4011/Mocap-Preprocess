# 여러 csv 파일들을 합쳐주는 코드입니다.
# 비어있는 부분을 채워주고 (description_map 참고)
# style에 맞게 tag 를 채워주거나 description을 변경해 줍니다. (def add_tag, add_discription)

# todo : csv_creater.py 다시 짜고, 이 코드 정리하기
import csv

l = []
f_names = ['motion index', 'bvh file', 'rgb file', 'actor', 'description', 'tag', 'extra description', 'style', '']
styles = ['H', "EH", "N", "S", "ES"]

def add_discription(st, actor):
  if actor == "1":
    st = st.replace("He", "A man")

  elif actor == "2":
    st = st.replace("He", "A woman")
    st = st.replace("his", "her")
    st = st.replace("himself", "herself")

  return st


def add_tag(tag, style):
  if style == 'EH' : 
    return tag + ", happy, pleasure, delight, glad, exaggeration"
  
  elif style == "H"  : 
    return tag + ", happy, pleasure, delight, glad"
  
  elif style == "ES" : 
    return tag + ", sorrow, sadness, exaggeration"
  
  elif style == "S" : 
    return tag + ", sorrow, sadness" 
  else: # 'N'
    return tag
  
csv_files = ["2021-08-05.csv", 
            "2021-08-06.csv",  
            "2021-08-09.csv",  
            "2021-08-10.csv",  
            "2021-08-11.csv",  
            "2021-08-12.csv",  
            "2021-08-13.csv",  
            "2021-08-17.csv",  
            "2021-08-18.csv",  
            "2021-08-19.csv",  
            "2021-08-20.csv",  
            "2021-08-23.csv",  
            "2021-08-24.csv",  
            "2021-08-24.csv",  
            "2021-08-25.csv",  
            "2021-08-26.csv"]

with open('merged.csv', 'w', newline='') as wfile:
  writer = csv.DictWriter(wfile, fieldnames=f_names)
  writer.writerow(dict(zip(f_names, f_names)))

  for csv_file in csv_files:
    with open(csv_file, newline='') as csvfile:
    
      d = {}
      reader = csv.DictReader(csvfile)
      for row in reader:
        if row["tag"] == '' or row["description"] == '':
          continue
        d[row["motion index"]] = row

    with open(csv_file, newline='') as csvfile:
      
      reader = csv.DictReader(csvfile)

      for row in reader:
        idx = row["motion index"]
        if idx == '':
          continue
        data = d[idx]

        row['style'] = styles[(int(idx)-1) % 5]
        try: 
          row['extra description'] = data['']
          del row['']
        except:
          pass

        row['description'] = add_discription(data['description'], row['actor'])
        if row['tag'] == "":
          row['tag'] = data['tag'] 
        row['tag'] = add_tag(row['tag'], row['style'])

        writer.writerow(row)






