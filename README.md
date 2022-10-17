
# Mocap-Preprocess
* 모션캡쳐 전처리 코드를 모아둔 repository입니다.
* 자세한 내용은 [notion](https://jh11.notion.site/Mocap-48f9578a29de49b793e22bbc2c40e02d) 을 참고해 주세요.

## bvh converter
* bvh는 rigid body를 표현하는 파일형식입니다. bvh를 data로 nn을 학습실킬 때 bvh의 내부 형식이 같야 하기 때문에, 전처리 코드가 필요합니다.
* ex) `lafan2dme.py` : lafan 형식에서 dme 로 변환하는 파이썬 코드입니다.

* **파일 형식**  
  motive : LIMLAB의 모션캡쳐장비 sofware인 Motive의 bvh형식입니다.  
  [lafan](https://github.com/ubisoft/ubisoft-laforge-animation-dataset) : link 확인  
  [dme](https://github.com/DeepMotionEditing/deep-motion-editing) : link 확인  

## csv converter

* .tak 모션캡쳐 파일들로부터 csv 파일을 만들어주는 코드입니다.

## gui macro

* motive에서 공개하지 않은 API를 자동화하기 위해 만들어 놓은 gui macro입니다. 
