# AWS 클라우드 환경 기반 가상 주식 거래 플랫폼

## 프로젝트 명
가상 주식 거래 플랫폼
___
<br> <br>

## 프로젝트 멤버 및 역할
클라우드 컴퓨팅 팀 14
- 추민: 프론트 UI 구성 설계 및 디자인 구상, AWS Lightsail을 통해 프로젝트 배포
- 최두환: 서비스 로그인 상태 유지 개발, 프론트 디자인 적용
- 배근호: 프로젝트 기획, 주식 거래 서비스 백엔드 기능 개발
___
<br> <br>

## 프로젝트 소개
본 프로젝트는 실제 주식 시장을 모방한 가상의 주식 거래 플랫폼입니다.
플랫폼 사용자는 증권사 직원(관리자), 일반고객(개인 투자자), 기업고객(상장기업)의 세 가지 역할로 시스템에 참여할 수 있습니다.

역할별 기능
- 증권사 직원: 기업 등록/삭제, 섹터 수정
- 일반고객/기업고객 공통: 입출금, 기업 정보 조회, 주식 주문/조회/취소, 잔고 조회 등
- 일반고객: 보유 주식의 섹터별 비중 조회
- 기업고객: 재무정보 등록

사용자는 가상의 자산으로 주식을 거래하며, 투자 전략과 포트폴리오 구성 연습을 통해 자산 관리 기술을 습득할 수 있습니다.
___
<br> <br>

## 프로젝트 필요성 소개
주식 투자에 관심은 있지만 실제 투자에 대한 두려움이 있는 초보 투자자들에게 안전한 학습 환경을 제공하는 것이 본 프로젝트의 주요 목적입니다. 가상의 돈으로 가상의 종목을 거래함으로써 주식 거래 메커니즘과 투자 전략을 실제 자금 위험 없이 학습할 수 있는 환경을 제공합니다. <br> <br>

주식 투자에서 발생할 수 있는 세금 문제 또한 중요한 학습 요소입니다. 특히, 주식 매매 차익에 대해 부과되는 양도소득세는 대부분의 증권사에서 사용하는 선입선출(FIFO, First-In-First-Out) 방식으로 계산됩니다. 이 방식에 따라 어떤 주식이 먼저 매도 처리되는지에 따라 세금이 달라질 수 있으며, 이를 제대로 이해하지 못하면 불필요한 세금이 발생할 수 있습니다. 본 프로젝트는 이를 반영하여, 사용자가 자신의 거래 내역을 기반으로 선입선출 방식으로 양도소득을 자동 계산하고 시뮬레이션할 수 있도록 구현함으로써 실전 투자에서 세금 전략까지 고려할 수 있도록 돕습니다. <br> <br>

또한, 실제 주식 시장에서는 일시적인 이용자 폭주로 인해 플랫폼 접속이 지연되는 사례가 있었습니다. 예를 들어, 2021년 주식 시장에 대한 열기가 높았을 때 일부 증권사에서는 접속 지연 현상이 발생한 바 있습니다. 최근 새로 선출된 대통령이 코스피 5000을 목표로 제시하면서 다시 한번 대중의 주식 투자에 대한 관심이 높아질 수 있습니다. 이로 인해 플랫폼 접속자가 급격히 증가할 수 있으며, 이에 따라 유연하게 서버 용량을 확장할 수 있는 클라우드 기반 인프라가 필수적입니다. 따라서 본 프로젝트는 AWS Lightsail 클라우드 서비스를 통해 안정적으로 서비스를 제공합니다.
___
<br> <br>

## 관련 기술/논문/특허 조사 내용 소개
본 프로젝트는 가상 주식 거래 시스템을 구현함에 있어, 다음과 같은 기술 및 관련 연구를 참고하였습니다.

### 관련 기술
- FastAPI: 빠른 API 개발 및 테스트를 지원하는 Python 백엔드 프레임워크
- PostgreSQL: 신뢰성 높은 오픈소스 RDBMS
- React: 사용자 인터페이스 구축을 위한 프론트엔드 라이브러리
- JWT (JSON Web Token): 사용자 인증 및 세션 유지 기술
- AWS Lightsail: 클라우드 서버 배포 및 운영

### 관련 특허
제목: 가상계좌를 이용한 증권거래 체험 서비스 장치 및 방법 <br>
KIPRIS 특허출원번호: 1020130028009 <br>
출원인: 대신증권 주식회사
<br> <br>
본 발명은 사용자가 증권사에서 운영하는 사이트나 HTS 프로그램에 가입하지 않고, 자동으로 체험용 가상계좌를 개설하여 가상계좌를 통해 증권 거래를 체험할 수 있도록 하는 가상계좌를 이용한 증권거래 체험 서비스 장치 및 방법에 관한 것이다.

본 발명에 따른 가상계좌를 이용한 증권거래 체험 서비스 장치는, 네트워크를 통해 접속한 사용자 단말기에 대해 임의로 가상계좌를 개설하여 할당하고, 상기 사용자 단말기가 할당된 가상계좌를 이용해 둘러보기 증권거래 서비스를 체험할 수 있도록 하는 증권거래 서버; 및 상기 증권거래 서버에 네트워크를 통해 접속하여 가상계좌를 할당받고, 상기 할당받은 가상계좌를 이용해 둘러보기 증권거래 서비스를 이용하는 사용자 단말기를 포함하는 것을 특징으로 한다.
___
<br> <br>

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

<figure style="text-align: center;">
<img src="https://github.com/user-attachments/assets/7099147b-456b-4f13-8eef-ff30ed4ac3a0" width=1000, height=600>
<figcaption>다이어그램 1. 회원가입 및 로그인 기능</figcaption> 
</figure>
<br>

<figure style="text-align: center;">
<img src="https://github.com/user-attachments/assets/1f1c0d12-f987-445c-a653-f6e34e476f5e" width=1000, height=600>
<figcaption>다이어그램 2. 증권사 직원 기능</figcaption> 
</figure>
<br>

<figure style="text-align: center;">
<img src="https://github.com/user-attachments/assets/30db3ce5-a218-4922-9464-38af787a334c" width=1000, height=600>
<figcaption>다이어그램 3. 고객 계정 공통 기능</figcaption>  
</figure>
<br>

<figure style="text-align: center;">
<img src="https://github.com/user-attachments/assets/dad33270-4691-4491-91f7-a3813e8bf210" width=1000, height=600>
<figcaption>다이어그램 4. 고객 계정 공통 주식 거래 기능</figcaption> 
</figure>
<br>

<figure style="text-align: center;">
<img src="https://github.com/user-attachments/assets/fa9ce8bb-2867-4e28-b2e0-08ee6721ef82" width=1000, height=600>
<figcaption>다이어그램 5. 고객 계정 공통 주문 조회 및 취소 기능</figcaption>  
</figure>
<br>

<figure style="text-align: center;">
<img src="https://github.com/user-attachments/assets/2ba8a412-62e7-4dcc-95fd-4d327a8efd09" width=1000, height=600>
<figcaption>다이어그램 6. 일반 고객 전용 기능</figcaption>  
</figure>
<br>

<figure style="text-align: center;"> 
<img src="https://github.com/user-attachments/assets/93c0be48-20fd-4128-aad9-606bcba5f7cd" width=1000, height=600>
<figcaption>다이어그램 7. 기업 고객 전용 기능</figcaption>  
</figure>
<br>

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
<img src="https://github.com/user-attachments/assets/3582505a-05cb-4a81-b91f-1a1b8946a0db" width=800, height=600> <br>
___
<br> <br>


## 프로젝트 사용 방법
### 프로젝트 개발환경
- Python 3.12.7
- DBMS: PostgreSQL 15.10
- Node.JS v22.16.0
- npm 10.9.2

### 프로젝트 전체 구성
```
stock_trade_project/
├── app/                       # 백엔드(FastAPI)
│   ├── api/v1/endpoints
│   ├── api/v1/api.py
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── dependencies.py
│   └── main.py
├── front/                  	# 프론트엔드(React)
      ├── public/
      │   └── index.html
      └── src/
      │   ├── admin/
      │   ├── api/
      │   ├── auth/
      │   ├── company/
      │   ├── customer/
      │   ├── App.jsx
      │   └── index.js
      └── package-lock.json
      └── package.json
      └── postcss.config.json
      └── tailwind.config.json
```

### 프로젝트 프론트엔드 구성
```
src/
├── api/
│   └── api.js
├── auth/
│   ├── LoginPage.jsx
│   └── RegisterPage.jsx
├── customer/
│   ├── CustomerHome.jsx
│   ├── DepositWithdrawPage.jsx
│   ├── CompanyListPage.jsx
│   ├── CompanyFinancePage.jsx
│   ├── OrderbookAndOrderPage.jsx
│   ├── OrderListPage
│   ├── BalancePage.jsx
│   └── PortfolioWeightPage.jsx
├── admin/
│   ├── AdminHome.jsx
│   ├── RegisterCompanyPage.jsx
│   ├── UpdateSectorPage.jsx
│   └── DeleteCompanyPage.jsx
├── company/
│   ├── CompanyHome.jsx
│   ├── DepositWithdrawPage.jsx
│   ├── CompanyListPage.jsx
│   ├── CompanyFinancePage.jsx
│   ├── OrderbookAndOrderPage.jsx
│   ├── OrderListPage.jsx
│   ├── BalancePage.jsx
│   └── CompanyFinancialInfoPage.jsx
├── App.jsx
├── index.css
└── index.js
```

### 프로젝트 백엔드 구성
```
app/
├── main.py                    # FastAPI 애플리케이션 엔트리포인트
├── core/
│   ├── __init__.py
│   ├── config.py             # 환경 설정 및 데이터베이스 연결 정보
│   ├── security.py           # JWT 토큰 인증 및 보안
│   └── database.py           # SQLAlchemy 엔진 및 세션 관리
├── models/                   # SQLAlchemy 모델 (Entity)
│   ├── __init__.py
│   ├── account.py
│   ├── company.py
│   ├── order.py
│   └── transaction.py
├── schemas/                  # Pydantic 스키마
│   ├── __init__.py
│   ├── account.py
│   ├── company.py
│   └── order.py
├── repositories/             	# 데이터 액세스 계층
│   ├── __init__.py
│   ├── account_repository.py
│   ├── company_repository.py
│   └── order_repository.py
├── services/                 	# 비즈니스 로직 계층
│   ├── __init__.py
│   ├── admin_service.py
│   ├── customer_service.py
│   └── company_service.py
├── api/
│   └── v1/
│       ├── __init__.py
│       ├── endpoints/
│       │   ├── __init__.py
│       │   ├── admin.py
│       │   ├── customer.py
│       │   ├── company.py
│       │   └── auth.py
│       └── api.py
└── dependencies.py           # 의존성 주입 관리
```

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
본 프로젝트는 안정적이고 확장 가능한 서비스 제공을 위해 AWS Lightsail 클라우드 플랫폼을 활용하여 배포되었습니다. AWS Lightsail은 가상 사설 서버(VPS) 서비스로, 복잡한 클라우드 설정 없이도 웹 애플리케이션을 쉽게 배포할 수 있는 솔루션입니다.

### 배포 아키텍처

- **서버 환경**: Ubuntu 22.04 LTS 기반 AWS Lightsail 인스턴스
- **웹 서버**: Nginx (리버스 프록시 및 정적 파일 서빙)
- **백엔드**: FastAPI (Python) + Uvicorn ASGI 서버
- **프론트엔드**: React.js (빌드된 정적 파일)
- **데이터베이스**: PostgreSQL
- **프로세스 관리**: systemd를 통한 백엔드 서비스 데몬화

### 배포 과정

#### 1. AWS Lightsail 인스턴스 생성 및 초기 설정
- Ubuntu 22.04 LTS 인스턴스 생성
- SSH 키 페어 설정 및 보안 그룹 구성
- 방화벽 설정으로 HTTP(80), HTTPS(443), TCP(3000), TCP(8000) 포트 개방

#### 2. 시스템 환경 구성
- 시스템 패키지 업데이트 및 필수 도구 설치 (git, curl, nginx)
- Python 3.10+ 환경 구성 및 가상 환경 생성
- Node.js 및 npm 설치 (프론트엔드 빌드용)

#### 3. 데이터베이스 설정
- PostgreSQL 설치 및 초기 설정
- 프로젝트용 데이터베이스 및 사용자 계정 생성
- DDL 스크립트를 통한 테이블 구조 생성
- 초기 테스트 데이터 삽입

#### 4. 백엔드 배포
- GitHub에서 프로젝트 소스코드 클론
- Python 의존성 패키지 설치 (requirements.txt)
- FastAPI 애플리케이션 설정 및 데이터베이스 연결 구성
- systemd 서비스 파일 생성으로 백엔드 프로세스 데몬화
- 서비스 자동 시작 및 재시작 정책 설정

#### 5. 프론트엔드 배포
- React 프로젝트 의존성 설치 (npm install)
- 프로덕션 빌드 생성 (npm run build)
- API 엔드포인트 설정을 서버 환경에 맞게 구성

#### 6. Nginx 웹 서버 설정
- 프론트엔드 정적 파일 서빙을 위한 document root 설정
- `/api/` 경로의 요청을 백엔드 FastAPI 서버로 프록시하는 리버스 프록시 구성
- CORS 헤더 설정 및 보안 정책 적용
- 파일 권한 설정 및 접근 제어

#### 7. 서비스 통합 및 테스트
- 프론트엔드와 백엔드 간 API 통신 검증
- 데이터베이스 연결 및 CRUD 작업 테스트
- 사용자 인증 및 권한 관리 기능 검증
- 주식 거래 시뮬레이션 기능 통합 테스트

### 배포의 기술적 특징

Nginx를 통한 리버스 프록시 설정으로 프론트엔드와 백엔드를 분리하여 독립적인 개발과 배포가 가능하며, systemd를 활용한 프로세스 관리로 서비스의 안정성과 자동 복구 기능을 확보했습니다. 또한 PostgreSQL을 활용한 관계형 데이터베이스 설계로 금융 거래 데이터의 무결성과 일관성을 보장하고 있습니다.
___
<br> <br>

## 프로젝트 활용 방안
증권사 API 연결을 통해 시스템 기능을 확장하여 아래와 같이 사용할 수 있습니다.
- 개인 투자자: 실제 투자 전 다양한 전략을 테스트하고 자신의 투자 패턴 분석
- 금융 관련 학과 학생: 증권 시장의 작동 원리와 다양한 역할에 대한 이해 증진
- 스타트업/기업: 기업 공개(IPO) 과정을 시뮬레이션 하여 이해관계자에게 교육
- 투자 스터디 그룹: 그룹 내 모의 투자 대회 및 학습 도구로 활용
