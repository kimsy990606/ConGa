# 🚀 5분 안에 시작하기

## 👋 **처음 사용하시나요?**

걱정 마세요! 아주 쉽습니다. 

---

## 📥 **Step 1: 파일 다운로드**

1. ZIP 파일 다운로드
2. 원하는 폴더에 압축 해제
3. `contract-analyzer` 폴더 열기

---

## 🐍 **Step 2: Python 설치 (없으면)**

### **이미 Python이 있는지 확인:**

**Windows:**
- `cmd` 열고 `python --version` 입력
- Python 3.8 이상이 나오면 OK!

**Mac:**
- 터미널 열고 `python3 --version` 입력
- Python 3.8 이상이 나오면 OK!

### **없으면 설치:**

1. https://www.python.org/downloads/ 접속
2. "Download Python" 버튼 클릭
3. 설치 파일 실행
4. **중요:** "Add Python to PATH" 체크!

---

## 💻 **Step 3: 터미널 열기**

### **Windows:**

1. `contract-analyzer` 폴더 열기
2. 주소창에 `cmd` 입력하고 엔터
3. 검은 창이 열림!

### **Mac:**

1. `contract-analyzer` 폴더 우클릭
2. "폴더에서 새로운 터미널" 선택
3. 터미널이 열림!

---

## 📦 **Step 4: 라이브러리 설치 (처음 한 번만)**

터미널에 다음 명령어 입력:

**Windows:**
```
pip install -r requirements.txt
```

**Mac:**
```
pip3 install -r requirements.txt
```

**엔터 누르고 기다리기** (1-2분 소요)

이런 메시지 나오면 성공:
```
Successfully installed streamlit-1.28.0 PyPDF2-3.0.0 ...
```

---

## 🚀 **Step 5: 실행!**

터미널에 다음 명령어 입력:

**Windows:**
```
streamlit run app.py
```

**Mac:**
```
streamlit run app.py
```

**엔터!**

---

## 🎉 **Step 6: 브라우저에서 확인**

- 자동으로 브라우저가 열립니다
- 주소: `http://localhost:8501`
- 안 열리면 위 주소를 직접 입력하세요

---

## ✅ **Step 7: 사용하기**

1. **사이드바에서 체크리스트 확인**
   - 여러 변호사 상담했나요?
   - 담당 변호사 직접 만났나요?

2. **계약서 PDF 업로드**
   - "파일 선택" 버튼 클릭
   - PDF 파일 선택

3. **분석 결과 확인**
   - 점수 확인
   - 위험 조항 확인
   - Double Check 질문 확인

4. **리포트 다운로드**
   - "상세 리포트 다운로드" 클릭
   - "개선 요청서 다운로드" 클릭

---

## 🛑 **문제 해결**

### **"python을 찾을 수 없습니다"**

→ Python을 설치하지 않았거나 PATH에 추가 안 됨
→ Python 재설치 (Add to PATH 체크!)

### **"streamlit을 찾을 수 없습니다"**

→ 라이브러리 설치 안 됨
→ `pip install streamlit` 실행

### **"포트 8501이 이미 사용중"**

→ 이미 Streamlit이 실행 중
→ 터미널에서 `Ctrl + C` 눌러서 종료

### **PDF를 읽을 수 없습니다**

→ PDF가 손상되었거나 암호화됨
→ 다른 PDF로 시도

---

## 💡 **꿀팁**

### **터미널 없이 실행하려면?**

**Windows:**
1. 메모장 열기
2. 다음 내용 입력:
   ```
   @echo off
   pip install -r requirements.txt
   streamlit run app.py
   pause
   ```
3. `start.bat` 로 저장
4. 앞으로는 `start.bat` 더블클릭!

**Mac:**
1. 텍스트 편집기 열기
2. 다음 내용 입력:
   ```bash
   #!/bin/bash
   pip3 install -r requirements.txt
   streamlit run app.py
   ```
3. `start.command` 로 저장
4. 터미널에서 `chmod +x start.command` 실행
5. 앞으로는 `start.command` 더블클릭!

---

## 🌐 **온라인 버전 사용하기**

터미널이 싫다면?

→ 온라인 버전 사용! (배포 후 링크 추가)
→ 설치 없이 브라우저에서 바로 사용 가능

---

## 📞 **도움이 필요하면?**

1. README.md 파일 확인
2. GitHub Issues에 질문
3. [이메일 주소]로 문의

---

## 🎓 **다음 단계**

웹앱이 잘 실행되나요?

축하합니다! 이제:

1. **샘플 계약서로 테스트** (samples/ 폴더)
2. **실제 계약서 분석**
3. **친구에게 공유**
4. **피드백 남기기**

---

**Made with ❤️ for better legal contracts**

처음이라 어려우셨나요? 
괜찮습니다. 천천히 따라하다 보면 금방 익숙해집니다!
