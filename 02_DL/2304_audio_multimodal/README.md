# 기침소리 오디오데이터와 환자 정보 정형데이터를 이용한 코로나 감염 여부 판단 멀티모달 모델 구축
작성자 sona0817  

## Abstract
 기침소리 오디오데이터를 MFCC 변환, 수치화 하여 환자의 발열상태, 근육통, 호흡기질환 등에 대한 정형데이터와 하나의 데이터프레임으로 합치는 Multimodal Early Fusion 기술을 사용하여
환자의 코로나 감염여부를 판단하는 것을 목적으로 한다.

## 1. INTRODUCTION
 코로나19가 전세계적으로 확산되면서 작은 기침, 발열 등에도 PCR검사를 해야 하는 경우가 많아졌다.
PCR검사는 비강에 면봉을 넣어 원심분리기를 이용해 감염여부를 확인하는 방법을 사용하기 때문에 결과를 확인하기까지 오랜 시간이 걸리는데다,
자주 검사를 해야 하는 직업을 가진 경우 매번 비강검사의 불편함을 겪을 수 밖에 없었다.
이에 환자의 질환상태와 기침소리를 통해 코로나 감염 여부를 판단할 수 있다면 시간을 절약하고, 비강검사의 불편함도 해소할 수 있다.

 환자정보는 정형데이터로 환자의 나이, 성별, 호흡기질환여부(T/F), 발열 및 근육통 여부(T/F)를 수집하였고, 기침소리는 오디오데이터로 한 사람이 두 번 기침하는 소리를 녹음하였다.
이 때 환자정보는 수치형으로 모두 변환하고 기침소리는 librosa라는 패키지를 이용해 음성특징을 MFCC(Mel-Frequency Cepstral Coefficients)를 추출하여 정형데이터와 결합했다.
이는 두가지 이상의 데이터를 사용하는 멀티모달 중에서 Early Fusion 기술을 사용한 것으로 모델에 학습시키기 전 두가지 모달리티 데이터를 합치는 방법이다.

## 2. DATASET
### 2.1. Dataset Details

- Data Provider: DACON
- Train Data - Audio: .wav file 3805개
- Test DAta - Audio: .wav file 5732개
- train_data.csv & test_data.csv
  - train_data.csv shape: 3805 rows x 6 columns
  - test_data.csv shape: 5732 rows x 5 columns
  - id: 대상자 ID
  - age: 대상자 나이
  - gender: 대상자 성별
  - respiratory_condition: 대상자 호흡기 질환 여부
  - fever_or_muscle_pain: 대상자 발열 혹은 근육통 증상 여부
  - covid19: 코로나 음성/양성 여부 (0:음성, 1:양성)

### 2.2. Data Preprocessing - Label Encoding
 라벨인코딩은 범주형 데이터를 0부터 연속된 수치 데이터로 바꿔주눈 기술로 모델을 학습할 때에는 숫자형으로 데이터를 넣어야 하기 때문에 인코딩을 수행한다.
이 때, 각 숫자는 서로 관계가 없는 상황이지만 (예를들어 정상은 1, 비정상은 2로 변환되었을 때 비정상이 정상의 2배라는 의미를 가지지 않음),
라벨이 너무 많아지는 경우 학습 과정에서 가중치가 많이 들어갈 수 있기 때문에 적절히 사용해야한다.
본 프로젝트에서는 train_data.csv와 test_data.csv에 있는 'gender'컬럼인 대상자의 성별을 0:male, 1:female로 변환하였다.

## 3. Method
### 3.1. MFCC 추출
MFCC는 오디오데이터 중에서도 특히 사람의 음성에 대해 특징을 추출하는데 특화된 알고리즘으로 재부적으로 작동하는 다양한 과정들이 사람의 음성 특징을 강조한다.
입력된 소리 전체를 한번에 알고리즘에 적용하지 않고 20~40ms 사이값으로 나누어 적용한다.
MFCC 알고리즘은 해당 구간에 대해서 사람이 인지하기 좋은 Mel-scale로 스펙트럼을 분석하고, 퓨리에 변환을 통해 특징을 추출한다.
MFCC 알고리즘을 통해 변환된 특징벡터는 주파수 도메인 특징으로 간주되어 시간 도메인 특징보다 더 정확하다는 장점이 있다.
본 프로젝트에서는 librosa.feature.mfcc() 함수를 통해 MFCC 특징을 추출했다.
  
<p align='center'>
  <img width="80%" alt="image" src="https://github.com/Sona0817/study/assets/80690009/dae15fa1-0646-4b60-a597-94272f5fa8cb">
</p>
  
#### 3.1.1. Mel-scale
MFCC는 Mel-Frequency Cepstral Coefficient의 약자로 오디오데이터를 특징 벡터로 변환해주는 알고리즘이다.
Mel은 사람의 달팽이관에서 아이디어를 얻은 방법으로 사람의 달팽이관에 소리가 들어갈 때 주파수(진동수)에 따라 달팽이관에 부딪히는 위치가 달라진다.
달팽이관의 구조상 주파수 대역이 낮을 때 변화를 잘 잡아내지만 주파수 대역이 높을 때의 변화는 잘 잡아내지 못한다.
이러한 달팽이관의 특성에 맞춰 오디오데이터의 특성을 추출하는 것을 Mel-scale이라고 한다.

#### 3.1.2. Pre-emphasis
몸 구조상 사람의 소리는 고주파 성분이 상당히 줄어들어서 발성하게 되고, 이런 특징은 모음을 발음할 때 두드러진다.
고주파 성분을 강화하고 저주파 성분을 양화시키는 high pass filter를 적용하여 음성 신호가 전체 주파수 영역대에서 고르게 분포될 수 있도록 한다.

<p align='center'>
  <img width="40%" alt="image" src="https://github.com/Sona0817/study/assets/80690009/64819311-ff82-4af0-bb01-1a28ab610431">
</p>
  
#### 3.1.3. 음소단위변환
사람의 음성의 경우 같은 단어를 말하더라도 어떤 사람은 1초만에 말하기도 하고 어떤 사람은 5초동안 말할 수도 있다.
따라서 오디오데이터에서 Mel-scale을 뽑기 전에 오디오데이터를 음소단위로 변환한다.
음소란 사람이 현재 내고 있는 발음을 의마하며, 사람의 목소리는 통상적으로 20~40ms 시간 내에 음소가 변하지 않는다고 한다.
따라서 오디오데이터를 20~40ms 사이의 단위로 쪼개어 변환한다.

librosa.feature.mfcc() 함수에서는 일정한 시간간격(25ms)동안 존재하는 오디오신호를 하나의 프레임으로 간주한다.
프레임 분할 시 프레임 초반과 후반에 손실되는 정보를 보존하기 위해 인접한 프레임들을 50%정도 겹쳐 데이터를 공유하도록 한다.
프레임이 겹치는 것을 고려하여 전체 음성데이터에 대해 일정한 시간간격으로 프레임을 분할하여 시퀀스로 반환한다.
이 때 반환된 시퀀스는 MFCC계수로 음성신호의 시간적 특성을 보존하면서 주파수 정보를 추출한다.

#### 3.1.4. Windowing
프레임 단위로 분할된 음성 신호에 윈도우 함수를 적용하여 프레임의 경계를 부드럽게 만들어주는 단계다.
일반적으로 해밍(Hamming) 함수가 사용되고 수식은 아래와 같다.

<p align='center'>
  <img width="40%" alt="image" src="https://github.com/Sona0817/study/assets/80690009/97e5d4f9-c986-4cd5-9e2a-c032d032dc6d">
</p>

해밍 윈도우 함수는 프레임의 시작과 끝에서 값이 0이 되고, 중심에서 최대값을 갖는 형태로 프레임 경계 부분에서 발생하는 오차를 줄인다.

#### 3.1.5. Fast Fourier Transform
윈도우가 적용된 프레임을 FFT 알고리즘을 사용하여 주파수 영역으로 변환한다. FFT는 시간 영역의 신호를 주파수 영역으로 변환하는 알고리즘으로 주파수 성분의 세기 정보를 얻을 수 있다.

<p align='center'>
  <img width="40%" alt="image" src="https://github.com/Sona0817/study/assets/80690009/5bc09fca-f573-4c42-b30b-1f6e79d44e00">
</p>

FFT를 얻은 주파수 스펙트럼은 복소수 형태로 표현되며 크기, 세기, 에너지 등의 정보를 포함하고 있다. 이를 통해 해당 신호(소리)의 주요 특징을 분석하며 MFCC 계산의 중간 결과로 사용한다.

#### 3.1.6. Mel-Filter Bank
FFT 결과를 Mel-scale로 변환된 주파수 영역으로 매핑한다.
이 과정은 인간의 청각 특을 모델링하고, 음성 신호의 중요한 주파수 대역을 강조하기 위해 사용된다.
일반적으로 FFT 알고리즘을 통해 받은 주파수 스펙트럼에 삼각형 모양의 필터를 곱해 각 필터의 주파수 응답을 계산한다.

<p align='center'>
  <img width="80%" alt="image" src="https://github.com/Sona0817/study/assets/80690009/7775df07-28aa-45b9-b6f5-fc3e793b09ae">
</p>

왼쪽 그림의 첫번째는 낮응ㄴ 주파수 영역에서 작은 삼각형을 보이고 두번째, 세번재로 갈수록 높은 주파수 영역으로 이동하면서 삼각형이 넓어지는 모습을 볼 수 있다.
이런 Mel-Filter를 모든 주파수 범위에 적용하면 오른쪽 그림과 같이 나타난다.
FFT 주파수 스펙트럼에 Mel-Filter Bank를 적용하면 Mel-Spectrogram을 구할 수 있다.

Mel-Spectrogram은 음성신호를 주파수로 변경하여 그 주파수의 콘텐츠를 표시하는 방법 중 하나로, 주파수와 시간을 X축, Y축으로 한 시각화 표현이다.
Mel-Spectrogram에서 나타나는 색상은 각 셀의 에너지 값을 표현한 것으로 음성신호를 시각적으로 비교해 볼 수 있다는 장점이 있다.
Mel-Spectrogram 역시 MFCC와 마찬가지로 음성 및 오디오 신호 분석에 사용되는 방법이지만 차이가 있다.
MFCC는 음성신호의 특성을 추출하는 것에 목적이 있고, 주파수 스펙트럼의 에너지나 특성을 포착하는 것을 중점으로 두어 각 성분의 상관관계 등으로 표현한다.
Mel-Spectrogram은 주파수 콘텐츠를 시간에 따라 시각화 하는 것에 목적이 있다.

#### 3.1.7. Log
멜 필터 뱅크의 결과에 로그를 취하여 선형 척도에서 로그 척도로 변환한다.
인간의청각 특성을 모델링하기 위한 것으로 다음단계에 DCT(Discrete Cosine Transform) 또는 IFFT(Inverse Fast Fourier Transform)을 잘 적용하기 위해 log를 취한다.

#### 3.1.8. Discrete Cosice Transform (DCT; 이산 코사인 변환)
MFCC를 추출할 때 일반적으로 CDT가 쓰이고, 로그화 된 Mel-spectrum을 차원축소하여 특징을 얻는 방법 중 하나다.
DCT의 주요 목적은 스펙트럼의 정보를 보존하면서 차원을 줄이는 것이다.
실수 입력에 대한 변환으로, 대부분의 실제 MFCC 계수 추출에서 사용된다.
DCT를 사용하면 변환된 계수의 첫번째 몇개만 사용되며, 이를 통해 중요한 주파수 대역을 표현할 수 있다.
librosa.feature.mfcc() 함수에서는 n_mfcc 파라미터를 통해 사용할 계수의 개수를 설정할 수 있다.

### 3.2. SMOTE
SMOTE는 Synthetic Minority Over-sampling Technique의 약자로, 대표적인 오버 샘플링 기법이다.
데이터세트의 균형을 맞추기 위해 사용하며, 소수 클래스에 대한 합성 샘플을 생성한다.

SMOTE는 소수클래스 데이터를 무작위로 선택하는 것으로 시작하여 데이터에 대한 k-근접이웃 알고리즘을 설정한다.
이후 선택된 랜덤 데이터와 무작위로 선택된 k-근접이웃 데이터 사이에 합성 데이터가 생성된다.
SMOTE는 소수클래스의 합성 데이터를 생성하는 동안 인접한 다수 클래스 데이터의 위치를 고려하지 않기 때문에 클래스가 겹치거나 노이즈가 발생할 수 있다.
따라서 고차원 데이터를 분류하는데는 비효율적이지만 오디도데이터와 정형데이터 같은 1차원, 2차원 데이터에 대해서는 효과적이다.

<p align='center'>
 <img width="60%" alt="image" src="https://github.com/Sona0817/study/assets/80690009/d75b819e-03fe-4b9f-a513-e8bec76ced96">
</p>


### 3.3. Multimodal Early Fusion
멀티모달 심층학습 모델에서 CNN과 FC레이어로 구형되는 특징 추출기와 분류기 이전에 두 입력 요소의 결합이 수행되면 Early Fusion(전단융합)이라 한다.
오디오데이터의 MFCC를 추출하여 수치화 하였기 때문에 기존의 다른 정형데이터와 함쳐 하나의 데이터프레임으로 만드는 것이 어렵지 않고,
데이터의 초기 단계에서 모달리티 간의 상호작용과 유용한 특징의 결합이 가능하기 때문에 Early Fusion을 선택했다.

<p align='center'>
 <img width="80%" alt="image" src="https://github.com/Sona0817/study/assets/80690009/770c6c24-2e58-4762-8fac-49017c9b20a0">
</p>

## 4. Conclusion
본 프로젝트는 오디오데이터와 정형데이터를 이용해 코로나 감염여부를 판단하는 모델을 만드는 것이 목표다.
3085개의 오디오데이터와 정형데이터로 학습했다.
오디오데이터는 MFCC 특성을 추출하였고, 정형데이터는 학습에 용이하도록 int형으로 변환했다.
MFCC를 추출할 때 sample_rate 파라미터는 사람 목소리와 비슷한 16000으로 설정, n_mfcc는 30으로 설정했다.
Early Fusion을 통해 오디오데이터와 정형데이터를 합친 후 클래스 불균형(0:3499, 1:306)을 해결하기 위해 SMOTE 알고리즘을 통해 학습 데이터셋(0:3499, 1:3499)을 구축했다.
학습데이터셋을 8대 2로 나누어 5598개의 train data와 1400개의 valid data를 구축하였고,
train data를 3가지 모델 Random Forest Classifier, MLP Classifier, Deep Linear Model에 학습시켰다.
valid data를 통해 3가지 모델을 평가한 결과는 아래와 같다.

<p align='center'>
 <img width="80%" alt="image" src="https://github.com/Sona0817/study/assets/80690009/a0007d23-8fe7-4794-97e8-2f464fc59754">
</p>

Random Forest와 Deep Linear Model은 0.9를 넘는 Accuracy를 보여 성능이 좋은편이고,
MLP의 경우 0.84 정도의 Accuracy로 약간 아쉬운 성능을 보였다.
3가지 모델이 전체적으로 높은 Accuracy를 모이기 때문에 오디오데이터와 정형데이터의 Early Fusion 멀티모달 학습이 대체적으로 잘 이루어졌다고 할 수 있다.

모델의 성능을 향상시키기 위해서 대상자의 호흡기질환, 발열여부 외에 산소포화도, 심박수 등의 정보나 X-ray 사진 등 추가적인 정보 수집을 할 수 있다.
또한, 본 프로젝트에서는 비교적 간단한 모델을 사용하여 멀티모달 데이터를 처리했는데 CNN이나 LSTM 등 다양한 모델 아키텍처를 이용하여 좀 더 좋은 성능의 모델을 구축할 수 있다.

## Reference
- 음성신호를 이용한 양방향 LSTM 기반 우울증 진단, 조아현, Journal of KIIT, Vol.20, No.1, 31 Jan 2022
- 전단 융합 기반 멀티모달 심층학습을 이용한 손동작 분류, 김익진, The Transaction of the Korean Insitute of Electrical Engineers, KIEE Vol.70, No.11, 27 Oct 2021
- An Efficient SMOTE-Based Deep Learning Model for Voice Pathology Detection, Ji-Na Lee, article belongs to the Special Issu AI, Machine Learning and Deep Learning in Signal Processing, 10 Mar 2023
- On the Benefits of Early Fusion in Multimodal Representation Learning, George Barnum, 14 Nov 2020



