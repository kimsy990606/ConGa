"""
⚖️ 변호사 계약서 품질 검증 서비스
- 비영리 프로젝트
- 100% 무료
- 개인정보 수집 안 함
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

from contract_analyzer import ContractAnalyzer
import PyPDF2
from PIL import Image
import io

# 결과 자동 소멸 시간 (분)
RESULT_EXPIRY_MINUTES = 5

# 개선 요청서 생성 함수 (사용 전에 정의되어야 함)
def generate_improvement_request(results):
    """변호사에게 보낼 개선 요청서 생성"""

    lines = []
    lines.append("=" * 60)
    lines.append("계약서 개선 요청서")
    lines.append("=" * 60)
    lines.append("")
    lines.append("변호사님께,")
    lines.append("")
    lines.append("계약서를 검토한 결과 다음 사항에 대해 명확히 해주시면 감사하겠습니다:")
    lines.append("")

    # 위험 조항
    if results['risk_patterns']:
        lines.append("=" * 60)
        lines.append("1. 위험 조항 개선 요청")
        lines.append("=" * 60)
        lines.append("")

        for i, risk in enumerate(results['risk_patterns'], 1):
            lines.append(f"[{i}] {risk['data']['description']}")
            lines.append(f"    → 개선 요청: {risk['data']['suggestion']}")
            lines.append("")

    # 구체성 문제
    if results.get('specificity_issues'):
        lines.append("=" * 60)
        lines.append("2. 구체성 개선 요청")
        lines.append("=" * 60)
        lines.append("")

        for i, issue in enumerate(results['specificity_issues'], 1):
            lines.append(f"[{i}] {issue['clause']}")
            lines.append(f"    → {issue['info']['suggestion']}")
            lines.append("")

    # 누락 조항
    missing_required = [name for name, info in results['required_check'].items()
                       if not info['found'] and info['data']['importance'] == '필수']

    if missing_required:
        lines.append("=" * 60)
        lines.append("3. 누락된 필수 조항")
        lines.append("=" * 60)
        lines.append("")

        for clause_name in missing_required:
            lines.append(f"- {clause_name}: {results['required_check'][clause_name]['data']['description']}")
        lines.append("")

    # Double Check 질문
    lines.append("=" * 60)
    lines.append("4. 추가 확인 질문")
    lines.append("=" * 60)
    lines.append("")
    lines.append("□ 가압류/가처분도 위임 범위에 포함되나요?")
    lines.append("□ 시간당 차지 금액이 얼마인가요?")
    lines.append("□ 화해로 끝나도 성과보수를 내야 하나요?")
    lines.append("□ 일부 승소 시 비율 계산은 어떻게 하나요?")
    lines.append("□ 계약 해지 시 환불 금액은 어떻게 계산하나요?")
    lines.append("")
    lines.append("=" * 60)
    lines.append("")
    lines.append("위 사항들에 대해 명확한 답변 부탁드립니다.")
    lines.append("감사합니다.")
    lines.append("")
    lines.append("의뢰인 올림")

    return "\n".join(lines)

# 페이지 설정
st.set_page_config(
    page_title="변호사 계약서 검증",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
if 'checklist_step' not in st.session_state:
    st.session_state.checklist_step = 1  # 1: 체크리스트, 2: 이런 변호사는 피하세요, 3: 메인

# 분석 결과 만료 체크 및 자동 삭제
def check_and_clear_expired_results():
    """만료된 분석 결과 자동 삭제"""
    if 'analysis_expiry' in st.session_state:
        if datetime.now() > st.session_state.analysis_expiry:
            # 만료됨 - 모든 분석 데이터 삭제
            keys_to_delete = ['analysis_results', 'analysis_expiry', 'analyzed_text']
            for key in keys_to_delete:
                if key in st.session_state:
                    del st.session_state[key]
            return True  # 만료됨
    return False  # 유효함

def get_remaining_time():
    """남은 시간 계산 (초 단위)"""
    if 'analysis_expiry' in st.session_state:
        remaining = st.session_state.analysis_expiry - datetime.now()
        return max(0, int(remaining.total_seconds()))
    return 0

def clear_analysis_data():
    """분석 데이터 즉시 삭제"""
    keys_to_delete = ['analysis_results', 'analysis_expiry', 'analyzed_text']
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]

# 페이지 로드 시 만료 체크
check_and_clear_expired_results()

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown('<div class="main-header">⚖️ 변호사 계약서 품질 검증</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">변호사 계약 전, 이 한 번만 확인하세요!</div>', unsafe_allow_html=True)

# 프로젝트 안내
with st.expander("📢 서비스 소개", expanded=False):
    st.markdown("""
    ### 🎯 이 서비스는?
    
    변호사-의뢰인 계약 분쟁을 줄이기 위한 **비영리 프로젝트**입니다.
    
    ✅ **완전 무료** - 수익화 없음  
    ✅ **개인정보 보호** - 분석 결과는 5분 후 자동 삭제, 원본 파일은 저장하지 않음
    ✅ **오픈소스** - GitHub에서 코드 확인 가능  
    
    ### 📊 분석 내용
    
    - **19개 필수 조항** 자동 체크
    - **17개 위험 패턴** 감지
    - **구체성 검증** (모호한 표현 걸러냄)
    - **실무 노하우** 반영 (실제 분쟁 사례 기반)
    
    ### ⚠️ 주의사항
    
    본 서비스는 **참고 자료**이며 법적 자문이 아닙니다.  
    최종 계약 결정은 반드시 변호사와 직접 상담 후 하시기 바랍니다.
    """)

# 모달 형식의 체크리스트 (세션 상태에 따라 표시)
if st.session_state.checklist_step == 1:
    # Step 1: 계약 전 체크리스트
    st.markdown("""
    <div style="background-color: #f8f9fa; border: 2px solid #007bff; border-radius: 10px; padding: 2rem; margin: 2rem 0;">
    """, unsafe_allow_html=True)

    st.markdown("## 📋 계약 전 체크리스트")
    st.markdown("### ✅ 계약서 검토 전 필수 확인")
    st.markdown("아래 항목들을 먼저 체크해주세요.")
    st.markdown("")

    check1 = st.checkbox("여러 변호사와 상담을 진행했다")
    check2 = st.checkbox("사건을 담당할 변호사와 직접 상담했다")
    check3 = st.checkbox("'무조건 승소한다'는 말은 과장의 위험이 있습니다.")
    check4 = st.checkbox("상담한 변호사와 필수적으로 계약을 해야하는 것은 아니니, 충분히 고민해보세요.")

    st.markdown("")
    st.markdown("---")
    st.markdown("### 🔍 변호사 등록 확인")
    st.markdown("""
    계약하려는 변호사가 실제로 등록된 변호사인지 반드시 확인하세요.

    👉 **[대한변호사협회 변호사 검색](https://www.koreanbar.or.kr/pages/search/search.asp)** (새 창에서 직접 조회)

    ⚠️ 미등록 또는 자격정지 상태의 변호사와 계약하면 법적 보호를 받을 수 없습니다.
    """)

    st.markdown("")

    if not all([check1, check2, check3, check4]):
        st.warning("⚠️ 모든 항목을 체크해주세요!")
        st.button("다음", disabled=True)
    else:
        st.success("✅ 좋습니다!")
        if st.button("다음"):
            st.session_state.checklist_step = 2
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

elif st.session_state.checklist_step == 2:
    # Step 2: 이런 변호사는 피하세요
    st.markdown("""
    <div style="background-color: #fff3cd; border: 2px solid #ffc107; border-radius: 10px; padding: 2rem; margin: 2rem 0;">
    """, unsafe_allow_html=True)

    st.markdown("## 🚨 이런 변호사는 피하세요")
    st.markdown("")
    st.markdown("""
    - 현금으로 내면 깎아준다고 함
    - 착수금만 많고 설명이 부족함
    - 착수금이 너무 적을 경우, 위탁 범위가 본인이 생각하는 범위와 다를 수 있습니다
    """)
    st.markdown("")

    if st.button("완료"):
        st.session_state.checklist_step = 3
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Step 3: 메인 컨텐츠 (체크리스트 완료 후)
st.markdown("---")

# 파일 업로드
st.markdown("## 📄 계약서 업로드")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "계약서 PDF 파일 또는 이미지를 업로드하세요",
        type=['pdf', 'jpg', 'jpeg', 'png'],
        help="PDF 파일 또는 계약서를 촬영한 이미지를 업로드하세요"
    )

with col2:
    st.info("""
    **지원 형식:**
    - PDF 파일
    - JPG, PNG 이미지

    **개인정보 보호:**
    - 이름, 주소 등은 가려도 됩니다
    - 원본 파일은 저장하지 않습니다
    - 분석 결과는 5분 후 자동 삭제됩니다
    """)

# 텍스트 직접 입력 옵션
with st.expander("📝 또는 계약서 텍스트를 직접 입력하세요"):
    text_input = st.text_area(
        "계약서 내용을 복사해서 붙여넣으세요",
        height=200,
        placeholder="예: 사건위임계약서\n\n위임인(갑): 홍길동\n수임인(을): 법무법인 OO\n\n제1조【목적】갑은 을에게..."
    )
    if st.button("텍스트 분석하기") and text_input:
        uploaded_file = "text_input"  # 플래그

# 분석 실행
if uploaded_file:
    st.markdown("---")
    st.markdown("## 🔍 분석 중...")
    
    # 프로그레스 바
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 1. 텍스트 추출
        status_text.text("📄 계약서 내용을 읽고 있습니다...")
        progress_bar.progress(20)
        
        if uploaded_file == "text_input":
            text = text_input
        elif uploaded_file.type == "application/pdf":
            # PDF 처리
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            # 이미지 처리 (OCR)
            st.warning("⚠️ 이미지 OCR 기능은 아직 구현 중입니다. PDF 파일을 사용해주세요.")
            text = ""
        
        progress_bar.progress(40)
        
        if not text or len(text) < 50:
            st.error("❌ 계약서 내용을 읽을 수 없습니다. PDF 파일이 올바른지 확인해주세요.")
        else:
            # 2. 분석 실행
            status_text.text("🔍 계약서를 꼼꼼히 분석하고 있습니다...")
            progress_bar.progress(60)
            
            analyzer = ContractAnalyzer()
            results = analyzer.analyze_contract(text)

            progress_bar.progress(80)
            status_text.text("📊 분석 결과를 정리하고 있습니다...")

            # 결과를 세션에 저장하고 만료 시간 설정
            st.session_state.analysis_results = results
            st.session_state.analysis_expiry = datetime.now() + timedelta(minutes=RESULT_EXPIRY_MINUTES)
            st.session_state.analyzed_text = None  # 원본 텍스트는 저장하지 않음 (개인정보 보호)

            # 원본 데이터 즉시 삭제
            del text

            progress_bar.progress(100)
            status_text.text("✅ 분석 완료!")

            # 3. 결과 표시
            st.markdown("---")
            st.markdown("## 📊 분석 결과")

            # 개인정보 보호 알림 및 카운트다운
            remaining_seconds = get_remaining_time()
            remaining_minutes = remaining_seconds // 60
            remaining_secs = remaining_seconds % 60

            privacy_col1, privacy_col2 = st.columns([3, 1])
            with privacy_col1:
                st.info(f"🔒 **개인정보 보호**: 분석 결과는 **{remaining_minutes}분 {remaining_secs}초** 후 자동 삭제됩니다. (새로고침 시 갱신)")
            with privacy_col2:
                if st.button("🗑️ 지금 삭제", help="분석 결과를 즉시 삭제합니다"):
                    clear_analysis_data()
                    st.success("✅ 분석 결과가 삭제되었습니다.")
                    st.rerun()

            # 종합 점수
            score = results['score']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "종합 점수",
                    f"{score}/100",
                    delta=None
                )
            
            with col2:
                risk_count = len(results['risk_patterns'])
                st.metric(
                    "위험 조항",
                    f"{risk_count}개",
                    delta=None
                )
            
            with col3:
                found_required = sum(1 for v in results['required_check'].values() 
                                    if v['found'] and v['data']['importance'] == '필수')
                total_required = sum(1 for v in results['required_check'].values() 
                                    if v['data']['importance'] == '필수')
                st.metric(
                    "필수 조항",
                    f"{found_required}/{total_required}",
                    delta=None
                )
            
            with col4:
                specificity_issues = len(results.get('specificity_issues', []))
                st.metric(
                    "구체성 문제",
                    f"{specificity_issues}개",
                    delta=None
                )
            
            # 점수별 메시지
            if score >= 80:
                st.markdown("""
                <div class="success-box">
                    <h3>✅ 우수한 계약서입니다!</h3>
                    <p>필수 조항이 잘 갖춰져 있고, 위험 요소가 적습니다.</p>
                </div>
                """, unsafe_allow_html=True)
            elif score >= 60:
                st.markdown("""
                <div class="warning-box">
                    <h3>⚠️ 보통 수준입니다</h3>
                    <p>일부 개선이 필요합니다. 아래 제안사항을 확인하세요.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="danger-box">
                    <h3>🚨 주의가 필요한 계약서입니다!</h3>
                    <p>여러 문제점이 발견되었습니다. 계약 전에 반드시 개선을 요청하세요.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # 위험 조항
            if results['risk_patterns']:
                st.markdown("### 🚨 발견된 위험 조항")
                
                for i, risk in enumerate(results['risk_patterns'], 1):
                    level = risk['data']['risk_level']
                    
                    if level == "매우높음":
                        emoji = "🔴🔴"
                        color = "#dc3545"
                    elif level == "높음":
                        emoji = "🔴"
                        color = "#ff6b6b"
                    elif level == "중간":
                        emoji = "🟡"
                        color = "#ffc107"
                    else:
                        emoji = "🟢"
                        color = "#28a745"
                    
                    with st.expander(f"{emoji} [{i}] {risk['data']['description']}", expanded=(level in ["매우높음", "높음"])):
                        st.markdown(f"**위험도:** `{level}`")
                        st.markdown(f"**❗ 왜 위험한가요?**")
                        st.info(risk['data']['why_risky'])
                        st.markdown(f"**💡 어떻게 해야 하나요?**")
                        st.success(risk['data']['suggestion'])
            else:
                st.success("✅ 위험한 조항이 발견되지 않았습니다!")
            
            st.markdown("---")
            
            # 구체성 문제
            if results.get('specificity_issues'):
                st.markdown("### 📝 구체성 문제")
                st.warning("다음 조항들이 있지만 충분히 구체적이지 않습니다:")
                
                for i, issue in enumerate(results['specificity_issues'], 1):
                    with st.expander(f"⚠️ [{i}] {issue['clause']}"):
                        st.markdown(f"**문제:** {issue['info']['description']}")
                        st.markdown(f"**💡 제안:** {issue['info']['suggestion']}")
            
            st.markdown("---")
            
            # 필수 조항 체크
            with st.expander("📋 필수 조항 상세 체크", expanded=False):
                st.markdown("### ✅ 필수 조항")
                
                for clause_name, clause_info in results['required_check'].items():
                    if clause_info['data']['importance'] == '필수':
                        if clause_info['found']:
                            st.success(f"✅ **{clause_name}**: {clause_info['data']['description']}")
                        else:
                            st.error(f"❌ **{clause_name}**: {clause_info['data']['description']}")
                            st.caption(f"⚠️ 위험: {clause_info['data']['risk_if_missing']}")
                
                st.markdown("### 📌 권장 조항")
                
                for clause_name, clause_info in results['required_check'].items():
                    if clause_info['data']['importance'] == '권장':
                        if clause_info['found']:
                            st.success(f"✅ **{clause_name}**: {clause_info['data']['description']}")
                        else:
                            st.warning(f"⭕ **{clause_name}**: {clause_info['data']['description']}")
                            st.caption(f"💡 있으면 더 좋아요: {clause_info['data']['risk_if_missing']}")
            
            # Double Check 질문
            st.markdown("---")
            st.markdown("## 🔄 Double Check!")
            st.markdown("### 계약서에는 있지만, 의뢰인에게 확인이 필요한 사항들")
            
            st.markdown("""
            <div class="info-box">
            <h4>📌 다음 사항들을 변호사에게 직접 확인하세요:</h4>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **💰 비용 관련:**
                - [ ] 가압류/가처분도 위임 범위에 포함되나요?
                - [ ] 시간당 차지 금액이 얼마인가요? (대형 로펌 기준 70~150만원)
                - [ ] 추가 비용은 대략 얼마나 예상되나요?
                """)
            
            with col2:
                st.markdown("""
                **📊 성과 관련:**
                - [ ] 화해로 끝나도 성과보수를 내야 하나요?
                - [ ] 일부 승소 시 비율 계산은 어떻게 하나요?
                - [ ] 방어 성공 기준은 무엇인가요?
                """)
            
            st.markdown("""
            **⚠️ 실무 조언:**
            > "계약서에는 명시되어 있어도, 의뢰인이 제대로 이해하지 못한 경우가 많습니다.  
            > 위 내용들을 변호사에게 직접 물어보고, 명확히 이해한 후 계약하세요."
            """)
            
            # 리포트 다운로드
            st.markdown("---")
            st.markdown("## 📥 분석 리포트 다운로드")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 텍스트 리포트 생성
                report_text = analyzer.generate_report(results)
                
                st.download_button(
                    label="📄 상세 리포트 다운로드 (TXT)",
                    data=report_text,
                    file_name="contract_analysis_report.txt",
                    mime="text/plain"
                )
            
            with col2:
                # 개선 요청서 생성
                improvement_request = generate_improvement_request(results)
                
                st.download_button(
                    label="📝 변호사 개선 요청서 다운로드 (TXT)",
                    data=improvement_request,
                    file_name="improvement_request.txt",
                    mime="text/plain"
                )
            
            # 사용 후기
            st.markdown("---")
            st.markdown("## 💬 피드백")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **이 서비스가 도움이 되셨나요?**
                
                피드백을 남겨주시면 서비스 개선에 큰 도움이 됩니다.
                """)
                
                feedback_rating = st.radio(
                    "만족도:",
                    ["⭐⭐⭐⭐⭐ 매우 만족", "⭐⭐⭐⭐ 만족", "⭐⭐⭐ 보통", "⭐⭐ 불만족", "⭐ 매우 불만족"],
                    horizontal=True
                )
            
            with col2:
                feedback_text = st.text_area(
                    "개선 의견이나 추가로 체크했으면 하는 조항이 있다면 알려주세요:",
                    height=100
                )
                
                if st.button("피드백 제출"):
                    st.success("감사합니다! 피드백이 전달되었습니다.")
                    st.balloons()
    
    except Exception as e:
        st.error(f"❌ 오류가 발생했습니다: {str(e)}")
        st.info("파일이 손상되었거나 읽을 수 없는 형식일 수 있습니다. 다른 파일을 시도해주세요.")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>⚖️ 변호사 계약서 품질 검증 서비스</p>
    <p>비영리 프로젝트 | 100% 무료 | 오픈소스</p>
    <p>본 서비스는 참고 자료이며 법적 자문이 아닙니다</p>
</div>
""", unsafe_allow_html=True)
