# AWS 클라우드 환경 기반 가상 주식 거래 플랫폼

## 프로젝트 명
가상 주식 거래 플랫폼

## 프로젝트 멤버 및 역할
- 추민: 프론트 UI 구성 설계 및 디자인 구상, AWS Lightsail을 통해 프로젝트 배포
- 최두환: 서비스 로그인 상태 유지 개발, 프론트 디자인 적용
- 배근호: 프로젝트 기획, 주식 거래 서비스 백엔드 기능 개발


## 프로젝트 소개
본 프로젝트는 실제 주식 시장을 모방한 가상의 주식 거래 플랫폼입니다.
플랫폼 사용자는 증권사 직원(관리자), 일반고객(개인 투자자), 기업고객(상장기업)의 세 가지 역할로 시스템에 참여할 수 있습니다.

역할별 기능
- 증권사 직원: 기업 등록/삭제, 섹터 수정
- 일반고객/기업고객 공통: 입출금, 기업 정보 조회, 주식 주문/조회/취소, 잔고 조회 등
- 일반고객: 보유 주식의 섹터별 비중 조회
- 기업고객: 재무정보 등록

사용자는 가상의 자산으로 주식을 거래하며, 투자 전략과 포트폴리오 구성 연습을 통해 자산 관리 기술을 습득할 수 있습니다.

## 프로젝트 필요성 소개
주식 투자에 관심은 있지만 실제 투자에 대한 두려움이 있는 초보 투자자들에게 안전한 학습 환경을 제공하는 것이 본 프로젝트의 주요 목적입니다. 가상의 돈으로 가상의 종목을 거래함으로써 주식 거래 메커니즘과 투자 전략을 실제 자금 위험 없이 학습할 수 있는 환경을 제공합니다. <br> <br>

주식 투자에서 발생할 수 있는 세금 문제 또한 중요한 학습 요소입니다. 특히, 주식 매매 차익에 대해 부과되는 양도소득세는 대부분의 증권사에서 사용하는 선입선출(FIFO, First-In-First-Out) 방식으로 계산됩니다. 이 방식에 따라 어떤 주식이 먼저 매도 처리되는지에 따라 세금이 달라질 수 있으며, 이를 제대로 이해하지 못하면 불필요한 세금이 발생할 수 있습니다. 본 프로젝트는 이를 반영하여, 사용자가 자신의 거래 내역을 기반으로 선입선출 방식으로 양도소득을 자동 계산하고 시뮬레이션할 수 있도록 구현함으로써 실전 투자에서 세금 전략까지 고려할 수 있도록 돕습니다. <br> <br>

또한, 실제 주식 시장에서는 일시적인 이용자 폭주로 인해 플랫폼 접속이 지연되는 사례가 있었습니다. 예를 들어, 2021년 주식 시장에 대한 열기가 높았을 때 일부 증권사에서는 접속 지연 현상이 발생한 바 있습니다. 최근 새로 선출된 대통령이 코스피 5000을 목표로 제시하면서 다시 한번 대중의 주식 투자에 대한 관심이 높아질 수 있습니다. 이로 인해 플랫폼 접속자가 급격히 증가할 수 있으며, 이에 따라 유연하게 서버 용량을 확장할 수 있는 클라우드 기반 인프라가 필수적입니다. 따라서 본 프로젝트는 AWS Lightsail 클라우드 서비스를 통해 안정적으로 서비스를 제공합니다.

## 관련 기술/논문/특허 조사 내용 소개
본 프로젝트는 가상 주식 거래 시스템을 구현함에 있어, 다음과 같은 기술 및 관련 연구를 참고하였습니다.

### 관련 기술
- FastAPI: 빠른 API 개발 및 테스트를 지원하는 Python 백엔드 프레임워크
- PostgreSQL: 신뢰성 높은 오픈소스 RDBMS
- React: 사용자 인터페이스 구축을 위한 프론트엔드 라이브러리
- JWT (JSON Web Token): 사용자 인증 및 세션 유지 기술
- AWS Lightsail: 클라우드 서버 배포 및 운영

### 관련 논문
(채울 예정)

## 프로젝트 개발 결과물 (+ 다이어그램)
본 프로젝트는 백엔드 API 서버, 프론트엔드 인터페이스, PostgreSQL 데이터베이스로 구성됩니다.

### 시스템 구성도
```
[사용자]
   ↓
[React 기반 프론트엔드 (AWS Lightsail)]
   ↓ REST API 호출
[FastAPI 백엔드 서버 (AWS Lightsail)] ←→ [PostgreSQL DB (AWS Lightsail)]
```

### 프로젝트 개발 결과
[POSTMAN API 명세서](https://documenter.getpostman.com/view/11352518/2sB2x3msei) <br>

회원가입 및 로그인 기능 <br>
![Image](https://github.com/user-attachments/assets/7099147b-456b-4f13-8eef-ff30ed4ac3a0)

증권사 직원 기능 <br>
![Image](https://github.com/user-attachments/assets/1f1c0d12-f987-445c-a653-f6e34e476f5e)

고객 계정 공통 기능 <br>
![Image](https://github.com/user-attachments/assets/30db3ce5-a218-4922-9464-38af787a334c)

고객 계정 공통 주식 거래 기능 <br>
![Image](https://github.com/user-attachments/assets/dad33270-4691-4491-91f7-a3813e8bf210)

고객 계정 공통 주문 조회 및 취소 기능 <br>
![Image](https://github.com/user-attachments/assets/fa9ce8bb-2867-4e28-b2e0-08ee6721ef82)

일반 고객 전용 기능 <br>
![Image](https://github.com/user-attachments/assets/2ba8a412-62e7-4dcc-95fd-4d327a8efd09)

기업 고객 전용 기능 <br>
![Image](https://github.com/user-attachments/assets/93c0be48-20fd-4128-aad9-606bcba5f7cd)

### DB 테이블 구조
- account: 개인 및 기업 고객 계정 테이블 (id, password, 계좌번호, 계좌유형, 이름, 연락처, 보유현금, 누적 양도소득)
- admin: 관리자 계정 테이블 (id, password, 계좌유형)
- company: 상장 기업 목록 테이블 (기업 이름, 주당 가격, 발행 주식 수, 시가총액, 섹터)
- financial_info: 기업 재무정보 테이블 (기업 이름, 연도, 매출액, 영업이익, 순이익)
- order_list: 주문 목록 테이블 (계좌번호, 주문유형, 기업 이름, 주당 주문 가격, 주문 개수, 주문번호)
- buy_list: 매수 내역 테이블 (매수주문 체결번호, 계좌번호, 기업이름, 주당 매수가격, 주문체결 날짜, 주문체결 시간, 매수 체결 개수, 매도 체결 누적 개수)
- sell_list: 매도 내역 테이블 (매도주문 체결번호, 계좌번호, 기업이름, 판매한 주식의 주당 매수했던 가격, 주당 매도 가격, 주문체결 날짜, 주문체결 시간, 매도 체결 개수)
- customer_balance: 개인(일반)고객 계정의 보유 주식 잔고 테이블 (계좌번호, 기업이름, 주식 보유 개수, 평균 매수 단가)
- company_balance: 기업고객 계정의 보유 주식 잔고 테이블 (계좌번호, 기업이름, 주식 보유 개수, 평균 매수 단가)
<img src="https://github.com/user-attachments/assets/3582505a-05cb-4a81-b91f-1a1b8946a0db" width=600, height=400>




## 프로젝트 사용 방법
### 프로젝트 개발환경
- Python 3.12.7
- DBMS: PostgreSQL 15.10
- Node.JS v22.16.0
- npm 10.9.2

### 백엔드 설치 라이브러리
```
pip install "FastAPI[standard]"
pip install sqlalchemy
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install pydantic
pip install pydantic-settings
pip install psycopg2-binary
```

### 프론트 설치 패키지
```
npm install react-scripts --save
npm install @heroicons/react

// front 디렉토리에서
npm install
```

### 로컬 환경에서 프로젝트 동작

```
// 백엔드 코드
// 프로젝트 root 폴더에서
uvicorn app.main:app --reload

// 프론트엔드 코드
// front 디렉토리에서
npm start
```

### AWS Lightsail 배포 과정
- (채울 예정)

## 프로젝트 활용 방안
증권사 API 연결을 통해 시스템 기능을 확장하여 아래와 같이 사용할 수 있습니다.
- 개인 투자자: 실제 투자 전 다양한 전략을 테스트하고 자신의 투자 패턴 분석
- 금융 관련 학과 학생: 증권 시장의 작동 원리와 다양한 역할에 대한 이해 증진
- 스타트업/기업: 기업 공개(IPO) 과정을 시뮬레이션 하여 이해관계자에게 교육
- 투자 스터디 그룹: 그룹 내 모의 투자 대회 및 학습 도구로 활용
