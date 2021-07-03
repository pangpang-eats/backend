# PANGPANG-EATS BACKEND

[![test & codecov](https://github.com/pangpang-eats/backend/actions/workflows/codecov.yml/badge.svg?branch=master)](https://github.com/pangpang-eats/backend/actions/workflows/codecov.yml)
[![codecov](https://codecov.io/gh/pangpang-eats/backend/branch/master/graph/badge.svg?token=TC0BEXC75T)](https://codecov.io/gh/pangpang-eats/backend)

## 프로젝트 소개

Coupang Eats의 클론 코딩, PangPang Eats의 백엔드 소스코드입니다.  
모든 커밋은 semantic 커밋 메시지 규칙을 따라 한국어 설명으로 작성되며, 가능한 작은 단위로 진행되어야 합니다.

## 프로젝트 목표

-   확장가능한 설계
    -   읽기 쉬운 코드
-   100% 커버리지의 테스트를 통해 안정적으로 배포되는 백엔드 시스템
    -   TDD와 함께 유닛테스트, API 별 통합 테스트 진행
-   많은 요청을 안정적으로 감당 할 수 있는 백엔드 인프라 구축
    -   매 버전 마다 JMeter를 활용하여 벤치마크 진행 및 이를 개선하는 방식으로 진행

## 기술 스택

-   Language: Python3
-   Framework: Django
-   Infra: AWS, Docker, Docker Compose
-   Database: PostgreSQL
-   CI / CD: Github Action

## 프로젝트 실행 - 파이썬

### 필요한 것들

-   Python 3.9.5

### 필요한 패키지 설치

진행에 앞서, 다음의 명령어를 이용해 파이썬 가상환경을 만드는것을 추천합니다.  
다음의 명령어는 가상환경을 생성하고, 가상환경 안으로 들어가 pip를 최신버전으로 업그레이드 하는 내용입니다.

```sh
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

다음의 명령어로 필요한 패키지들을 설치하세요.

```sh
pip install -r requirements.txt
```

### 개발 서버 실행

configs/envs.py 에서 필요한 설정들을 적절히 수정해주세요.

다음의 명령어로 개발 서버를 실행 할 수 있습니다.

```sh
python3 manage.py runserver
```

### 프로덕션 서버 실행

다음의 명령어로 8000번 포트에 gunicorn을 사용해 프로덕션 서버를 실행 할 수 있습니다.

```sh
gunicorn -b 0.0.0.0:8000 pangpangeats.wsgi:application
```

혹은 UNIX 소켓을 사용해 서버를 실행 할 수 있습니다.

```sh
gunicorn -b unix:/tmp/gunicorn.sock pangpangeats.wsgi:application
```
