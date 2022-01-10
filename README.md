자세한 내용은 [notion link](https://jh11.notion.site/Mocap-48f9578a29de49b793e22bbc2c40e02d) 을 참고해 주세요.
# Mocap-Preprocess
* 모션캡쳐 전처리 코드를 모아둔 repository입니다.

## bvh converter
* bvh는 자유분방한 파일형식입니다. bvh 형식이 같아야 model을 학습시킬 수 있어, 이를 통일 시주는 코드들입니다.
* ex) `lafan2dme.py` : lafan 형식에서 dme 로 변환하는 파이썬 코드입니다.

* **파일 형식**
* ours : LIMLAB motive의 bvh형식입니다.
* [lafan](https://github.com/ubisoft/ubisoft-laforge-animation-dataset) 
* [dme](https://github.com/DeepMotionEditing/deep-motion-editing)

## csv converter

* .tak 모션캡쳐 파일들로부터 csv 파일을 만들어주는 코드입니다.

## gui macro

* motive 공개하지 않은 API를 자동화하기 위해 만들어 놓은 gui macro입니다. 
