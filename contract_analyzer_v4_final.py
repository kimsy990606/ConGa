"""
변호사 계약서 품질 분석 엔진
표준 계약서 기준으로 실제 계약서를 평가
"""

class ContractAnalyzer:
    def __init__(self):
        # 필수 조항 체크리스트
        self.required_clauses = {
            "담당변호사": {
                "keywords": ["담당변호사", "담당 변호사", "수임변호사"],
                "importance": "필수",
                "standard_location": "계약서 하단",
                "description": "실제로 사건을 담당할 변호사 이름",
                "risk_if_missing": "상담한 변호사와 다른 사람이 사건을 맡을 수 있음"
            },
            "변호사등록번호": {
                "keywords": ["등록번호", "변호사 번호", "변호사등록번호"],
                "importance": "권장",
                "standard_location": "계약서 하단",
                "description": "변호사 자격 확인",
                "risk_if_missing": "가짜 변호사일 가능성 확인 불가"
            },
            "위임범위": {
                "keywords": ["위임한계", "심급", "당해 심급"],
                "importance": "필수",
                "standard_location": "제2조",
                "description": "어디까지 해주는지 명시",
                "risk_if_missing": "추가 비용 발생할 업무가 불명확"
            },
            "착수금": {
                "keywords": ["착수보수", "착수금", "선급금"],
                "importance": "필수",
                "standard_location": "제4조 또는 제6조",
                "description": "초기 지급 금액",
                "risk_if_missing": "비용이 명시되지 않음"
            },
            "환불조건": {
                "keywords": ["반환", "환불", "지급의무"],
                "importance": "필수",
                "standard_location": "제4조 또는 제6조",
                "description": "언제 얼마를 돌려받을 수 있는지",
                "risk_if_missing": "일 안 해도 돈 못 받을 수 있음"
            },
            "성공보수": {
                "keywords": ["성과보수", "성공보수"],
                "importance": "필수",
                "standard_location": "제5조 또는 제7조",
                "description": "승소 시 지급 금액",
                "risk_if_missing": "나중에 추가 청구 가능"
            },
            "성공기준": {
                "keywords": ["전부 승소", "일부 승소", "승소 비율", "승소로 보는"],
                "importance": "필수",
                "standard_location": "제5조 또는 제7조",
                "description": "어떤 경우에 성공으로 보는지",
                "risk_if_missing": "성공 여부로 분쟁 발생 가능"
            },
            "추가비용": {
                "keywords": ["인지대", "송달료", "감정료", "실비"],
                "importance": "필수",
                "standard_location": "제6조 또는 제8조",
                "description": "추가로 발생하는 비용 항목",
                "risk_if_missing": "예상 못한 비용 청구 가능"
            },
            "예치금액": {
                "keywords": ["예치", "충당하기 위하여"],
                "importance": "권장",
                "standard_location": "제6조 또는 제8조",
                "description": "추가 비용 예치금 금액",
                "risk_if_missing": "얼마를 미리 내야 하는지 모름"
            },
            "출장비기준": {
                "keywords": ["출장 일당", "1일 금"],
                "importance": "권장",
                "standard_location": "제6조 또는 제8조",
                "description": "출장 시 1일당 금액",
                "risk_if_missing": "출장비가 무제한으로 청구될 수 있음"
            },
            "통지의무": {
                "keywords": ["통지", "보고", "알려야"],
                "importance": "권장",
                "standard_location": "제8조 또는 제10조",
                "description": "처리 상황을 알려주는 의무",
                "risk_if_missing": "연락이 안 될 수 있음"
            },
            "자료보관기간": {
                "keywords": ["3개월", "보관", "폐기"],
                "importance": "권장",
                "standard_location": "제10조~제12조",
                "description": "서류를 언제까지 보관하는지",
                "risk_if_missing": "중요 서류가 바로 폐기될 수 있음"
            },
            "비밀유지": {
                "keywords": ["비밀", "비밀유지"],
                "importance": "권장",
                "standard_location": "제13조~제15조",
                "description": "정보 보호 의무",
                "risk_if_missing": "정보가 유출될 수 있음"
            },
            "조정화해권한": {
                "keywords": ["조정", "화해", "동의", "승낙"],
                "importance": "권장",
                "standard_location": "특약사항",
                "description": "조정이나 화해 시 의뢰인 동의 필요 여부",
                "risk_if_missing": "의뢰인 동의 없이 조정/화해될 수 있음"
            },
            "시간당요율": {
                "keywords": ["시간당", "보수율", "time charge"],
                "importance": "필수_시간제",
                "standard_location": "별첨",
                "description": "시간제 계약 시 시간당 요율",
                "risk_if_missing": "시간당 얼마인지 모름"
            },
            "변호사책임": {
                "keywords": ["손해배상", "배상", "책임", "변호사.*책임"],
                "importance": "권장",
                "standard_location": "특약사항 또는 본문",
                "description": "변호사의 잘못으로 손해 발생 시 책임",
                "risk_if_missing": "변호사가 잘못해도 책임 안 질 수 있음",
                "requires_specificity": True,
                "specificity_keywords": ["원", "만원", "억", "배상", "이자", "지연"],
                "vague_keywords": ["적절한", "상당한", "합리적인", "책임진다", "배상한다"]
            },
            "강제집행범위": {
                "keywords": ["가압류", "가처분", "강제집행", "보전처분"],
                "importance": "권장",
                "standard_location": "위임범위 조항",
                "description": "본안 소송 외 추가 절차 포함 여부",
                "risk_if_missing": "가압류/가처분 진행 시 추가 비용 청구될 수 있음"
            },
            "승소범위정의": {
                "keywords": ["승소", "성공", "화해", "조정", "승소 기준"],
                "importance": "권장",
                "standard_location": "성공보수 조항",
                "description": "화해/조정도 승소로 보는지 여부",
                "risk_if_missing": "화해로 끝났는데 성과보수 청구될 수 있음",
                "requires_specificity": True,
                "specificity_keywords": ["전부 승소", "일부 승소", "비율", "판결"],
                "vague_keywords": ["성공 시", "승소 시", "유리하게"]
            },
            "시간차지방식": {
                "keywords": ["시간당", "time charge", "시간제", "공제"],
                "importance": "권장",
                "standard_location": "환불조건 조항",
                "description": "계약 해지 시 시간당 비용 공제 방식",
                "risk_if_missing": "환불 시 예상보다 많이 공제될 수 있음",
                "requires_specificity": True,
                "specificity_keywords": ["만원", "원", "시간당"],
                "vague_keywords": ["합리적", "적정", "통상적"]
            }
        }
        
        # 위험 패턴
        self.risk_patterns = {
            "팀제운영": {
                "keywords": ["팀제", "팀으로", "공동으로", "협업"],
                "risk_level": "높음",
                "description": "실제 담당 변호사가 명시되지 않음",
                "suggestion": "담당 변호사 이름과 변호사 등록번호를 명시해달라고 요청하세요",
                "why_risky": "상담한 변호사가 아닌 다른 변호사(특히 경험이 적은 변호사)가 실제로 사건을 처리할 수 있습니다."
            },
            "환불불가": {
                "keywords": ["일절 환불", "환불 불가", "환불되지 않", "반환하지 않"],
                "risk_level": "높음",
                "description": "변호사가 일을 착수하지 않아도 환불 불가",
                "suggestion": "착수 전 100% 환불, 소장 제출 전 50% 환불 등 단계별 환불 규정을 추가해달라고 요청하세요",
                "why_risky": "변호사가 업무를 제대로 수행하지 않아도 돈을 돌려받을 수 없습니다."
            },
            "72시간조항": {
                "keywords": ["72시간", "3일", "계약 후.*시간"],
                "risk_level": "매우높음",
                "description": "계약 후 72시간 경과 시 무조건 환불 불가",
                "suggestion": "이 조항은 변협에서 중징계 대상으로 본 악질 조항입니다. 계약하지 마세요",
                "why_risky": "변협이 '72시간 약관'을 사용한 법무법인에 정직 6개월 중징계를 검토한 바 있습니다. 구조적으로 환불을 차단하는 조항입니다."
            },
            "추가비용애매": {
                "keywords": ["추가 비용 발생", "별도 청구", "실비 청구"],
                "anti_keywords": ["인지대", "송달료", "감정료"],  # 구체적 항목이 없으면 위험
                "risk_level": "높음",
                "description": "추가 비용 항목 및 금액이 불명확",
                "suggestion": "예상되는 추가 비용 항목(인지대, 송달료 등)과 대략적인 금액을 명시해달라고 요청하세요",
                "why_risky": "나중에 예상하지 못한 금액이 청구될 수 있습니다."
            },
            "비용상한없음": {
                "keywords": ["무제한", "상한 없", "제한 없"],
                "risk_level": "높음",
                "description": "추가 비용이나 성과보수에 상한이 없음",
                "suggestion": "총 비용 한도액 또는 성과보수 상한을 명시해달라고 요청하세요",
                "why_risky": "예상보다 훨씬 많은 금액이 청구될 수 있습니다."
            },
            "담당변경가능": {
                "keywords": ["담당 변경", "변경할 수 있", "교체할 수"],
                "anti_keywords": ["동의", "승인", "사전 협의"],
                "risk_level": "중간",
                "description": "의뢰인 동의 없이 담당 변호사 변경 가능",
                "suggestion": "담당 변호사 변경 시 사전 동의 조항을 추가해달라고 요청하세요",
                "why_risky": "내가 선택한 변호사가 아닌 다른 사람이 갑자기 사건을 맡을 수 있습니다."
            },
            "소통불명확": {
                "keywords": ["중요한.*통지", "필요한.*보고"],
                "anti_keywords": ["주 1회", "월 1회", "분기별", "정기적"],
                "risk_level": "낮음",
                "description": "연락 빈도가 불명확",
                "suggestion": "주 1회 또는 월 1회 등 정기 보고 조항을 추가해달라고 요청하세요",
                "why_risky": "연락이 잘 안 되거나, 중요한 정보를 늦게 알 수 있습니다."
            },
            "조정권한독단": {
                "keywords": ["조정.*할 수 있", "화해.*할 수 있"],
                "anti_keywords": ["동의", "승낙", "사전 협의"],
                "risk_level": "중간",
                "description": "의뢰인 동의 없이 조정/화해 가능",
                "suggestion": "조정이나 화해 시 반드시 의뢰인 사전 동의를 받는다는 조항을 추가해달라고 요청하세요",
                "why_risky": "원하지 않는 조건으로 조정되거나 화해될 수 있습니다."
            },
            "성공기준모호": {
                "keywords": ["성공 시", "승소 시"],
                "anti_keywords": ["전부 승소", "일부 승소", "승소 비율"],
                "risk_level": "중간",
                "description": "성공 기준이 구체적이지 않음",
                "suggestion": "전부 승소/일부 승소 시 각각 얼마인지, 승소 비율 계산 방법을 명시해달라고 요청하세요",
                "why_risky": "나중에 성공 여부로 분쟁이 발생할 수 있습니다."
            },
            "시간제조항없음": {
                "keywords": ["시간제", "time charge", "타임차지"],
                "anti_keywords": ["시간당", "원/시간", "보수율"],
                "risk_level": "높음",
                "description": "시간제 계약인데 시간당 요율이 없음",
                "suggestion": "시간당 요율을 명확히 명시해달라고 요청하세요",
                "why_risky": "시간당 얼마인지 모른 채 무제한으로 청구될 수 있습니다."
            },
            "잔금기한없음": {
                "keywords": ["잔금", "나머지"],
                "anti_keywords": ["까지", "이내", "기한"],
                "risk_level": "중간",
                "description": "잔금 납부 기한이 없음",
                "suggestion": "잔금을 언제까지 내야 하는지 명시해달라고 요청하세요",
                "why_risky": "잔금 미납 시 계약 해지되거나, 기납부 착수금도 환불 안 될 수 있습니다."
            },
            "임의해지": {
                "keywords": ["일방적", "임의로", "자의적"],
                "risk_level": "높음",
                "description": "변호사가 일방적으로 계약 해지 가능",
                "suggestion": "계약 해지 시 사전 통지 및 환불 규정을 명시해달라고 요청하세요",
                "why_risky": "갑자기 사임하고 착수금도 환불 안 할 수 있습니다."
            },
            "책임조항모호": {
                "keywords": ["책임", "배상"],
                "check_for_vague": True,
                "vague_keywords": ["적절한", "상당한", "합리적인", "책임진다", "배상한다"],
                "specific_keywords": ["원", "만원", "억", "지연.*이자", "지체.*이자"],
                "risk_level": "중간",
                "description": "변호사 책임 조항이 있지만 구체적이지 않음",
                "suggestion": "구체적인 금액(예: 착수금의 2배, 손해액 전액 등)과 이자율을 명시해달라고 요청하세요",
                "why_risky": "변호사가 잘못해도 '상당한 금액' 같은 애매한 표현으로 책임을 회피할 수 있습니다."
            },
            "금액표기모호": {
                "keywords": ["금액", "보수", "비용", "수임료"],
                "check_for_vague": True,
                "vague_keywords": ["적정", "합리적", "협의", "별도 협의", "추후 결정"],
                "specific_keywords": ["원", "만원", "억", "%"],
                "risk_level": "높음",
                "description": "금액이 '협의' 또는 '적정 금액' 등으로만 표기됨",
                "suggestion": "구체적인 금액 또는 계산 방식을 명시해달라고 요청하세요",
                "why_risky": "나중에 예상보다 훨씬 많은 금액이 청구될 수 있습니다."
            },
            "위임범위좁음": {
                "keywords": ["위임", "범위", "사건"],
                "anti_keywords": ["가압류", "가처분", "강제집행", "보전처분"],
                "risk_level": "높음",
                "description": "위임 범위에 가압류/가처분 등이 포함되지 않음",
                "suggestion": "가압류, 가처분, 강제집행도 포함되는지 반드시 확인하세요. 별도 비용일 수 있습니다",
                "why_risky": "본안 소송만 포함되고 가압류/가처분은 추가 비용이 발생할 수 있습니다. 의뢰인은 당연히 포함인 줄 알았는데 나중에 추가 청구됩니다."
            },
            "시간차지과다": {
                "keywords": ["시간당", "time charge", "시간제"],
                "risk_level": "높음",
                "description": "시간당 차지 금액이 과다하거나 불명확함",
                "suggestion": "대형 로펌 기준 시간당 70~150만원입니다. 이를 초과하거나 금액이 명시되지 않았다면 확인하세요",
                "why_risky": "계약 해지 시 시간당 비용으로 공제되는데, 금액이 과다하면 환불이 거의 없을 수 있습니다.",
                "check_amount": True,
                "max_reasonable": 1500000  # 150만원
            },
            "현금할인제시": {
                "keywords": ["현금", "할인", "세금", "탈세"],
                "risk_level": "매우높음",
                "description": "현금 결제 시 할인 제안",
                "suggestion": "이는 탈세 위험이 있는 불법 행위입니다. 절대 거래하지 마세요",
                "why_risky": "세무 문제에 연루될 수 있고, 나중에 계약서 효력에 문제가 생길 수 있습니다. 변호사 징계 대상입니다."
            }
        }
    
    def analyze_contract(self, text):
        """계약서 전체 분석"""
        results = {
            "score": 0,
            "max_score": 100,
            "required_check": {},
            "risk_patterns": [],
            "specificity_issues": [],
            "suggestions": []
        }
        
        # 1. 필수 조항 체크
        found_count = 0
        total_required = len([c for c in self.required_clauses.values() if c["importance"] == "필수"])
        
        for clause_name, clause_data in self.required_clauses.items():
            is_found = self._check_clause(text, clause_data["keywords"])
            results["required_check"][clause_name] = {
                "found": is_found,
                "data": clause_data
            }
            
            # 구체성 체크 (해당되는 경우만)
            specificity = self._check_clause_specificity(text, clause_name, clause_data)
            if specificity:
                results["required_check"][clause_name]["specificity"] = specificity
                if specificity["status"] == "모호함":
                    results["specificity_issues"].append({
                        "clause": clause_name,
                        "info": specificity
                    })
            
            if is_found and clause_data["importance"] == "필수":
                found_count += 1
        
        # 필수 조항 점수 (60점 만점)
        results["score"] += (found_count / total_required) * 60
        
        # 2. 위험 패턴 검사
        for pattern_name, pattern_data in self.risk_patterns.items():
            risk_found = self._check_risk_pattern(text, pattern_data)
            if risk_found:
                results["risk_patterns"].append({
                    "name": pattern_name,
                    "data": pattern_data
                })
                # 위험 패턴 발견 시 감점
                if pattern_data["risk_level"] == "매우높음":
                    results["score"] -= 15
                elif pattern_data["risk_level"] == "높음":
                    results["score"] -= 10
                elif pattern_data["risk_level"] == "중간":
                    results["score"] -= 5
        
        # 3. 권장 조항 보너스 (40점 만점)
        recommended_found = sum(1 for clause_name, clause_info in results["required_check"].items() 
                               if clause_info["data"]["importance"] == "권장" and clause_info["found"])
        total_recommended = len([c for c in self.required_clauses.values() if c["importance"] == "권장"])
        results["score"] += (recommended_found / total_recommended) * 40 if total_recommended > 0 else 0
        
        # 구체성 문제로 추가 감점 (각 5점씩)
        results["score"] -= len(results["specificity_issues"]) * 5
        
        # 점수 범위 조정 (0~100)
        results["score"] = max(0, min(100, int(results["score"])))
        
        return results
        
        # 3. 권장 조항 보너스 (40점 만점)
        recommended_count = len([c for c in self.required_clauses.values() 
                                if c["importance"] == "권장" and 
                                results["required_check"][clause_name]["found"]])
        total_recommended = len([c for c in self.required_clauses.values() if c["importance"] == "권장"])
        results["score"] += (recommended_count / total_recommended) * 40 if total_recommended > 0 else 0
        
        # 점수 범위 조정 (0~100)
        results["score"] = max(0, min(100, int(results["score"])))
        
        return results
    
    def _check_clause(self, text, keywords):
        """특정 조항이 있는지 확인"""
        for keyword in keywords:
            if keyword in text:
                return True
        return False
    
    def _check_risk_pattern(self, text, pattern_data):
        """위험 패턴 검사"""
        # 키워드가 있는지 확인
        has_keyword = any(keyword in text for keyword in pattern_data["keywords"])
        if not has_keyword:
            return False
        
        # 구체성 체크 패턴인 경우
        if pattern_data.get("check_for_vague", False):
            # 모호한 표현이 있는지 확인
            has_vague = any(vague in text for vague in pattern_data["vague_keywords"])
            # 구체적인 표현이 있는지 확인
            has_specific = any(specific in text for specific in pattern_data["specific_keywords"])
            
            # 모호한 표현은 있지만 구체적인 표현이 없으면 위험
            if has_vague and not has_specific:
                return True
            return False
        
        # anti_keywords가 있으면 (구체적 내용이 있으면) 위험 아님
        if "anti_keywords" in pattern_data:
            has_anti = any(anti in text for anti in pattern_data["anti_keywords"])
            if has_anti:
                return False
        
        return True
    
    def _check_clause_specificity(self, text, clause_name, clause_data):
        """조항의 구체성 체크 (선택적)"""
        if not clause_data.get("requires_specificity", False):
            return None
        
        # 해당 조항이 있는지 먼저 확인
        has_clause = self._check_clause(text, clause_data["keywords"])
        if not has_clause:
            return None
        
        # 구체적 키워드 확인
        has_specific = any(keyword in text for keyword in clause_data.get("specificity_keywords", []))
        
        # 모호한 키워드 확인
        has_vague = any(keyword in text for keyword in clause_data.get("vague_keywords", []))
        
        if has_vague and not has_specific:
            return {
                "status": "모호함",
                "description": f"{clause_name} 조항이 있지만 구체적이지 않음",
                "suggestion": "구체적인 금액이나 계산 방식을 명시해달라고 요청하세요"
            }
        elif has_specific:
            return {
                "status": "구체적",
                "description": f"{clause_name} 조항이 구체적으로 명시됨"
            }
        
        return None
    
    def generate_report(self, analysis_results):
        """분석 결과를 읽기 쉬운 리포트로 변환"""
        report = []
        
        # 제목
        report.append("=" * 50)
        report.append("📊 계약서 품질 분석 결과")
        report.append("=" * 50)
        report.append("")
        
        # 점수
        score = analysis_results["score"]
        if score >= 80:
            grade = "우수"
            emoji = "✅"
        elif score >= 60:
            grade = "보통"
            emoji = "⚠️"
        else:
            grade = "주의"
            emoji = "🚨"
        
        report.append(f"{emoji} 종합 점수: {score}/100 ({grade})")
        report.append("")
        
        # 위험 조항
        if analysis_results["risk_patterns"]:
            report.append("=" * 50)
            report.append(f"⚠️ 위험 조항 발견 ({len(analysis_results['risk_patterns'])}개)")
            report.append("=" * 50)
            report.append("")
            
            for i, risk in enumerate(analysis_results["risk_patterns"], 1):
                level_emoji = {"매우높음": "🔴🔴", "높음": "🔴", "중간": "🟡", "낮음": "🟢"}
                emoji = level_emoji.get(risk["data"]["risk_level"], "⚠️")
                
                report.append(f"[{i}] {emoji} {risk['data']['description']}")
                report.append(f"    위험도: {risk['data']['risk_level']}")
                report.append(f"    이유: {risk['data']['why_risky']}")
                report.append(f"    💡 제안: {risk['data']['suggestion']}")
                report.append("")
        else:
            report.append("✅ 위험 조항이 발견되지 않았습니다.")
            report.append("")
        
        # 구체성 문제
        if analysis_results["specificity_issues"]:
            report.append("=" * 50)
            report.append(f"📝 구체성 문제 ({len(analysis_results['specificity_issues'])}개)")
            report.append("=" * 50)
            report.append("")
            report.append("다음 조항들이 있지만 충분히 구체적이지 않습니다:")
            report.append("")
            
            for i, issue in enumerate(analysis_results["specificity_issues"], 1):
                report.append(f"[{i}] ⚠️ {issue['clause']}")
                report.append(f"    문제: {issue['info']['description']}")
                report.append(f"    💡 제안: {issue['info']['suggestion']}")
                report.append("")
            
            report.append("⚠️ 모호한 표현 대신 구체적인 금액/방법을 요청하세요!")
            report.append("")
        
        # 필수 조항 체크
        report.append("=" * 50)
        report.append("📋 필수 조항 체크")
        report.append("=" * 50)
        report.append("")
        
        for clause_name, clause_info in analysis_results["required_check"].items():
            if clause_info["data"]["importance"] == "필수":
                check = "✅" if clause_info["found"] else "❌"
                report.append(f"{check} {clause_name}: {clause_info['data']['description']}")
                if not clause_info["found"]:
                    report.append(f"    ⚠️ 위험: {clause_info['data']['risk_if_missing']}")
                report.append("")
        
        # 권장 조항
        report.append("=" * 50)
        report.append("📌 권장 조항")
        report.append("=" * 50)
        report.append("")
        
        for clause_name, clause_info in analysis_results["required_check"].items():
            if clause_info["data"]["importance"] == "권장":
                check = "✅" if clause_info["found"] else "⭕"
                report.append(f"{check} {clause_name}: {clause_info['data']['description']}")
                if not clause_info["found"]:
                    report.append(f"    💡 있으면 더 좋아요: {clause_info['data']['risk_if_missing']}")
                report.append("")
        
        return "\n".join(report)


# 테스트용 샘플 계약서
sample_contract_good = """
사건위임계약서

위임인(갑): 홍길동
수임인(을): 법무법인 정의

제1조【목적】갑은 을에게 위 표시 사건의 처리를 위임하고, 을은 이를 수임한다.

제2조【위임한계】갑이 을에게 위임하는 위임사무의 한계는 당해 심급에 한하고...

제4조【착수보수】갑은 을에게 위임계약의 성립과 동시에 착수보수로 금 5,000,000원을 지급한다.

제5조【성과보수】위임사무가 판결로 성공한 때에는 금 10,000,000원을 지급한다.

제6조【비용부담】인지대, 송달료, 감정료 등 실비는 갑이 부담한다.

제8조【통지의무】을은 위임사무의 중요한 처리상황을 갑에게 통지한다.

제13조【비밀유지】을은 업무상 취득한 갑의 모든 비밀정보를 비밀로 유지한다.

제14조【손해배상】을이 업무상 과실로 갑에게 손해를 입힌 경우, 을은 실손해액 전액과 지연일수에 대한 연 15%의 이자를 배상한다.

담당변호사: 김정의 (등록번호: 12345)
"""

sample_contract_bad = """
사건위임계약서

위임인(갑): 홍길동
수임인(을): XX법무법인

제1조 본 사건은 팀제로 운영됩니다.

제2조 착수금 5,000,000원은 일절 환불되지 않습니다.

제3조 추가 비용이 발생할 수 있으며, 별도로 청구합니다.

제4조 담당 변호사는 사건 진행 중 변경될 수 있습니다.

제5조 중요한 사항에 대해서만 통지합니다.
"""

sample_contract_vague = """
사건위임계약서

위임인(갑): 이철수
수임인(을): YY법률사무소

제1조 본 사건의 수임료는 적정한 금액으로 책정됩니다.

제2조 착수금은 합리적인 금액으로 협의하여 결정합니다.

제3조 추가 비용은 상황에 따라 별도 협의합니다.

제4조 변호사가 과실로 손해를 입힌 경우 적절한 배상을 책임집니다.

제5조 성공 시 상당한 성과보수를 지급합니다.

담당변호사: 박변호 (등록번호: 54321)
"""


if __name__ == "__main__":
    analyzer = ContractAnalyzer()
    
    print("=" * 60)
    print("테스트 1: 좋은 계약서 (구체적)")
    print("=" * 60)
    results_good = analyzer.analyze_contract(sample_contract_good)
    report_good = analyzer.generate_report(results_good)
    print(report_good)
    
    print("\n\n")
    
    print("=" * 60)
    print("테스트 2: 나쁜 계약서")
    print("=" * 60)
    results_bad = analyzer.analyze_contract(sample_contract_bad)
    report_bad = analyzer.generate_report(results_bad)
    print(report_bad)
    
    print("\n\n")
    
    print("=" * 60)
    print("테스트 3: 모호한 계약서 (구체성 부족)")
    print("=" * 60)
    results_vague = analyzer.analyze_contract(sample_contract_vague)
    report_vague = analyzer.generate_report(results_vague)
    print(report_vague)
