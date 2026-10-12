# 2026-10-01 최종 정리

사용자의 삭제 요청에 따라 단순 보관 중심 구성을 변경했습니다.

## 남긴 파일

- `notebooks/`, `scripts/`, `requirements/`, `tools/`: 공개용 코드와 검증 도구.
- `data/`: 원본 이미지와 CSV 한 벌.
- `results/gemma_results/`: 기존 Gemma 체크포인트·설정·결과. `ssafy-16-2-ai/gemma_results/`에서 이동했습니다.
- `reference/`: 발표 PPT와 배포 가이드 PDF.
- `reference/experiments/`: 서로 다른 Qwen 학습 실험, Gemma 실행본, 고유 초안.
- `reference/baselines/`: 제공된 baseline·오프라인 다운로드 노트북.
- `reference/unique_sources/`: 공개본과 동일하다고 확정하지 못한 소수의 고유 원본.
- `analysis/`: 분석 보고서·집계·재생성용 코드.
- `baseline/`, `downloads/`: 설치된 로컬 환경과 모델·오프라인 패키지. 현재 환경을 유지하기 위해 제거하지 않았습니다.

## 삭제

- 배포·Drive 다운로드 ZIP 3개.
- SHA-256 비교로 동일함을 확인한 데이터 복사본 16,115개. `data/`의 대응 파일은 유지했습니다.
- 공개본과 코드가 같은 노트북, 동일 패치 복사본, 빈 노트북.
- 과거 일회성 노트북 생성기와 당시 배치 전용 모의 테스트.
- 다시 만들 수 있는 분석 이미지 모음.

아카이브 전체 삭제는 하지 않았습니다. 파일별로 분류하고 고유 파일은 옮긴 뒤 빈 폴더만 제거했습니다.
삭제·이동 집계는 `prune_summary.json`에 기록했습니다. 설치 패키지 내부 테스트 자산은 삭제 대상 ZIP에서 제외했습니다.

공개 제외: `reference/`, `results/`, `data/`, `analysis/`, `baseline/`, `downloads/`. 발표자료는 GitHub에 올라가지 않습니다.
로컬 결과 경로가 바뀌었으므로 옛 분석 스크립트에서 절대 경로를 사용하는 경우 수정이 필요합니다. Colab Drive 경로와 원격 실행에는 영향을 주지 않습니다.
최종 모델·점수·공식 순위는 제출 기록 확인 후 README에 추가합니다.
