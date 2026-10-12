# SSAFY AI Challenge — 이미지 객관식 VQA

이미지와 질문, 네 개의 선지를 입력받아 답안을 생성하는 Colab 실험 모음입니다.
최종 순위와 대표 제출 모델은 아직 확정하지 않았습니다. 공개 폴더의 노트북은 **추론용**입니다.

## 실행 파일

| 노트북 | 용도 |
| --- | --- |
| [gemma4_31b_dinov3.ipynb](notebooks/gemma4_31b_dinov3.ipynb) | Gemma 4 31B + DINOv3 크롭 + 선지 TTA + 선택적 Thinking |
| [qwen38_27b_dinov3.ipynb](notebooks/qwen38_27b_dinov3.ipynb) | Qwen 3.8 27B + DINOv3 비교 실험 |
| [qwen38_27b_dinov2.ipynb](notebooks/qwen38_27b_dinov2.ipynb) | DINOv2 크롭 비교 실험 |
| [qwen38_27b_simple.ipynb](notebooks/qwen38_27b_simple.ipynb) | Qwen 단순 추론 |
| [exaone45_33b_simple.ipynb](notebooks/exaone45_33b_simple.ipynb) | EXAONE 단순 추론 |

순위가 나온 후 이 표에서 대표 제출을 표시하고 나머지를 비교 실험으로 남길 예정입니다.
파일명에 적힌 모델 및 파라미터 수는 각 노트북 설정을 기준으로 합니다.

## Colab 실행

1. 원하는 노트북을 Colab에 업로드하고 해당 모델을 수용할 GPU 런타임을 선택합니다.
2. 데이터 압축을 풀어 다음 구조를 준비합니다. 데이터는 저장소에 포함하지 않습니다.

```text
/content/drive/MyDrive/ssafy-16-2-ai/
├── test.csv
├── sample_submission.csv
├── test/test_0001.jpg ...
├── train.csv
└── train/ ...
```

3. `DATA_DIR_OVERRIDE`를 실제 CSV·이미지 폴더로 맞춥니다. 폴더가 한 번 더 중첩되어 있으면 안쪽 경로를 사용합니다.
4. 위에서부터 실행합니다. 패키지 변경으로 재시작을 요구하면 세션을 재시작하고 `INSTALL_PACKAGES=False`로 다시 실행합니다. 새 런타임에서는 설치가 필요합니다.
5. DINOv3는 승인받은 Hugging Face 계정으로 로그인합니다. Google 계정과 같을 필요는 없습니다. 토큰은 노트북에 적지 않습니다.
6. 완료 후 출력되는 `submission.csv` 경로를 확인합니다. 결과는 데이터 폴더 아래 `gemma_results` 또는 `qwen_results` 등에 저장됩니다.

TTA/Thinking은 문항을 여러 번 추론하므로 단순 추론보다 느립니다. DINO는 확대할 영역을 고르는 보조 모델이며 성능 개선을 보장하지 않습니다.
`validation` 모드는 train.csv의 정답으로 비교하며 학습을 수행하지 않습니다.

## 의존성

공통 목록: [requirements/colab-inference.txt](requirements/colab-inference.txt).
Colab 기본 PyTorch/CUDA를 사용하고 pandas는 Colab 호환을 위해 2.2.3으로 유지합니다.
노트북 하나만 업로드해도 실행할 수 있도록 설치 셀도 유지합니다. 환경별 전체 `pip freeze`나 패키지 wheel을 공개 저장소에 넣지 않습니다.
버전 범위는 기존 실험 설정이며 완전히 고정된 재현 환경은 아닙니다. 실행별 `run_config.json`에는 실제 설치 버전이 기록됩니다.

## 기존 실행 이어가기

[scripts/gemma4_speed_resume.py](scripts/gemma4_speed_resume.py)는 **이미 실행 중인 기존 Gemma 런타임 전용** 패치입니다.
8번 실행만 중지하고 동일 런타임에서 패치를 실행한 다음 8번만 재개합니다. 새 실행에서 먼저 실행하는 파일이 아닙니다.
기존 체크포인트를 보존하고 설정 변경 이력을 기록합니다. CPU/GPU 차이로 미세한 결과 차이는 생길 수 있습니다.

## 저장소 정리와 검증

- [정리 내역](docs/cleanup.md): 삭제 내역, 중요 자료 위치와 미확정 실험.
- [실험 메모](docs/experiment_notes.md): 사용자가 기록한 실험 과정.
- `python tools/validate_repository.py`: 노트북 문법·출력·자격 증명 패턴 검사.

데이터, 모델 가중치, 실행 로그, 제출 CSV, 발표자료, 배포 가이드, 참고 자료는 `.gitignore`로 제외합니다.
저장소: https://github.com/rladntlr/ssafy-recycling-vqa-v2
정리 과정에서 대형 모델 추론은 다시 실행하지 않았습니다.

로컬 자료: `data/`는 중복 제거 후 남긴 데이터 한 벌, `results/`는 실행 결과, `reference/`는 발표자료·가이드·고유 실험입니다. ZIP 배포본과 중복 백업은 삭제했습니다.
