# ⚖️ 변호사 계약서 품질 검증 서비스

## 📋 프로젝트 소개

변호사-의뢰인 계약 분쟁을 줄이기 위한 **비영리 프로젝트**입니다.

### ✅ 주요 기능

- **19개 필수 조항** 자동 체크
- **17개 위험 패턴** 감지
- **구체성 검증** (모호한 표현 감지)
- **실무 노하우** 반영 (실제 분쟁 사례 기반)
- **개선 요청서** 자동 생성

### 🎯 특징

- ✅ 100% 무료
- ✅ 오픈소스
- ✅ 개인정보 수집 안 함
- ✅ 분석 후 파일 즉시 삭제

---

## 🚀 로컬 실행 방법

### 1. Python 설치 확인

Python 3.8 이상이 필요합니다.

```bash
python --version
# 또는
python3 --version
```

### 2. 파일 다운로드

이 저장소를 다운로드하거나 클론합니다:

```bash
git clone [repository-url]
cd contract-analyzer
```

### 3. 필요한 라이브러리 설치

**Windows:**
```bash
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
pip3 install -r requirements.txt
```

### 4. 실행

**Windows:**
```bash
streamlit run app.py
```

**Mac/Linux:**
```bash
streamlit run app.py
```

브라우저가 자동으로 열리면서 `http://localhost:8501` 에서 실행됩니다!

---

## 📁 파일 구조

```
contract-analyzer/
├── app.py                          # Streamlit 웹 인터페이스
├── contract_analyzer.py            # 분석 엔진 (v4.0)
├── requirements.txt                # 필요한 라이브러리
├── README.md                       # 이 파일
└── samples/                        # 샘플 계약서 (선택사항)
    ├── good_contract.pdf
    └── bad_contract.pdf
```

---

## 🌐 온라인 버전

로컬 설치 없이 바로 사용하고 싶다면:

👉 **[웹사이트 링크](https://contract-analyzer.streamlit.app)** (배포 후 추가)

---

## 🔍 사용 방법

1. **웹 앱 실행** (`streamlit run app.py`)
2. **체크리스트 확인** (사이드바)
3. **계약서 업로드** (PDF 또는 이미지)
4. **분석 결과 확인**
5. **리포트 다운로드**

---

## 📊 분석 항목

### 필수 조항 (19개)

#### 기본 정보
- 담당변호사 (이름 + 등록번호)
- 위임범위 (어디까지 해주는지)

#### 비용 관련
- 착수금 (초기 지급 금액)
- 성공보수 (승소 시 금액)
- 추가비용 (실비 항목)
- 환불조건 (언제 얼마 환불)

#### 절차 관련
- 성공기준 (무엇이 성공인지)
- 강제집행범위 (가압류/가처분 포함 여부)
- 승소범위정의 (화해도 승소인지)
- 시간차지방식 (해지 시 공제 방법)

#### 권한 및 의무
- 통지의무 (상황 보고)
- 비밀유지 (정보 보호)
- 조정화해권한 (동의 필요 여부)
- 변호사책임 (과실 시 책임)

---

### 위험 패턴 (17개)

#### 매우 높음 (🔴🔴)
- 72시간 조항 (변협 징계 대상)
- 현금 할인 제시 (탈세 위험)

#### 높음 (🔴)
- 팀제 운영 (담당 변호사 불명확)
- 환불 불가 조항
- 비용 상한 없음
- 위임 범위 좁음
- 시간차지 과다
- 추가 비용 애매
- 금액 표기 모호

#### 중간 (🟡)
- 담당 변경 가능
- 성공 기준 모호
- 시간제 조항 없음
- 잔금 기한 없음
- 조정 권한 독단
- 임의 해지
- 책임 조항 모호

#### 낮음 (🟢)
- 소통 불명확

---

## 🛠️ 기술 스택

- **Python 3.8+**
- **Streamlit** - 웹 인터페이스
- **PyPDF2** - PDF 처리
- **Pillow** - 이미지 처리
- **pytesseract** - OCR (선택사항)

---

## 🤝 기여하기

이슈, PR 환영합니다!

### 기여 방법

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 라이센스

MIT License (비영리 목적에 한함)

---

## ⚠️ 면책 조항

본 서비스는 교육 및 연구 목적의 프로젝트입니다.

1. 본 서비스는 계약서 품질 개선을 위한 **참고 자료**이며 **법적 자문이 아닙니다**.

2. 최종 계약 결정은 반드시 변호사와 직접 상담 후 하시기 바랍니다.

3. 본 서비스의 분석 결과로 인한 어떠한 손해에 대해서도 책임을 지지 않습니다.

4. 업로드된 모든 파일은 분석 후 즉시 삭제되며, 어떠한 개인정보도 수집하지 않습니다.

---

## 📞 문의

- 이슈: [GitHub Issues]
- 이메일: [이메일 주소]

---

## 📈 프로젝트 통계

- ✅ 분석 조항: 19개
- ✅ 위험 패턴: 17개
- ✅ 구체성 검증: 활성화
- ✅ 실무 사례: 반영

---

**Made with ❤️ for better legal contracts**
