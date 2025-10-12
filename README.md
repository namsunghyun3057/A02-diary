# A02-diary
전공기초프로젝트 A02팀 - 일정 관리 다이어리

[팀 프로젝트 기획서 PDF](https://docs.google.com/document/d/1AZPqi3LDcepCAO7eozJwEEPKuB4trnr2aOvMOX5yBGg/edit?usp=sharing)

## 🌳 Git 브랜치 전략 (Branch Strategy)

우리 팀은 **Git Flow의 단순화된 버전**을 사용하여 안정적인 코드 관리와 협업 효율성을 높입니다.

### 1. 핵심 브랜치

| 브랜치 이름 | 역할 및 규칙 |
| :--- | :--- |
| **`main` (또는 `master`)** | **최종 배포(Production) 코드**입니다. **절대로 이 브랜치에 직접 커밋하지 않습니다.** `develop` 브랜치에서 병합(Merge)만 허용됩니다. |
| **`develop`** | **다음 릴리즈를 위한 개발 통합 브랜치**입니다. 모든 기능 브랜치(`feature/`)는 이 브랜치로 병합됩니다. |

### 2. 개발용 브랜치 (보조 브랜치)

| 브랜치 이름 형식 | 역할 및 사용 시점 |
| :--- | :--- |
| **`feature/기능_이름`** | **새로운 기능 개발**을 위한 브랜치입니다. (`develop`에서 분기) |
| **`bugfix/버그_이름`** | `develop` 또는 `main`에서 발견된 **버그 수정**을 위한 브랜치입니다. (버그가 발견된 브랜치에서 분기) |
| **`refactor/이름`** | 기능 추가 없이 **코드 구조 개선** 작업을 할 때 사용합니다. (`develop`에서 분기) |

---

## ⚙️ Git 작업 흐름 (Workflow)

새로운 기능을 개발할 때 팀원들이 따라야 할 단계별 작업 흐름입니다.

### 1단계: 작업 시작

1.  **`develop` 브랜치로 이동 및 최신화:**
    ```bash
    git checkout develop
    git pull origin develop
    ```
2.  **새 기능 브랜치 생성 및 이동:**
    ```bash
    git checkout -b feature/새로운-기능-이름
    ```

### 2단계: 작업 및 커밋

1.  로컬에서 작업을 진행합니다.
2.  작은 단위로 자주 커밋합니다. (커밋 메시지 규칙은 아래 [커밋 메시지 규칙](#3-커밋-메시지-규칙-commit-message-convention) 참고)
    ```bash
    git add .
    git commit -m "feat: 사용자 로그인 폼 레이아웃 구현"
    ```

### 3단계: 통합 요청 (Pull Request)

1.  **원격 저장소에 푸시:**
    ```bash
    git push origin feature/새로운-기능-이름
    ```
2.  **Pull Request (PR) 생성:** Git 서비스 (GitHub, GitLab 등)에서 **`feature/새로운-기능-이름`** 브랜치를 **`develop`** 브랜치로 병합하는 PR을 생성합니다.
    * **PR 내용 작성:** PR 템플릿에 따라 변경 사항, 해결한 이슈 등을 명확히 기재합니다.
3.  **코드 리뷰 및 병합:** 팀원의 리뷰를 받고, 승인되면 `develop` 브랜치로 병합(Merge)합니다.

---

## 3. 커밋 메시지 규칙 (Commit Message Convention)

명확한 기록 유지를 위해 **Conventional Commits** 규칙을 따릅니다.

**형식:** `<Type>: <Subject>`

| Type | 설명 | 예시 |
| :--- | :--- | :--- |
| **`feat`** | 새로운 기능 추가 (A new feature) | `feat: 사용자 프로필 수정 기능 추가` |
| **`fix`** | 버그 수정 (A bug fix) | `fix: 로그인 시 발생하던 오류 수정` |
| **`docs`** | 문서 수정 (Documentation only changes) | `docs: README.md에 브랜치 전략 추가` |
| **`style`** | 코드 포맷팅, 세미콜론 누락 등 (Code style changes) | `style: 함수 이름 컨벤션 통일` |
| **`refactor`** | 리팩토링 (기능 변경 없이 코드 구조 개선) | `refactor: 로그인 API 호출 로직 분리` |
| **`test`** | 테스트 코드 추가 및 수정 | `test: 회원가입 성공 케이스 추가` |
| **`chore`** | 빌드 시스템, 라이브러리 설치 등 기타 변경 사항 | `chore: ESLint 설정 업데이트` |