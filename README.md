# Track Cracker
Divide and Conquer your Objectives.

## Motivation
학습 계획과 달성률을 쉽게 작성/기록 및 보여주는 앱을 찾기 쉽지 않다.  
Objective를 정하고 이에 대한 Key Result 들을 Subtask 들로 나눈 뒤, 각 Task와 Objective의 달성률을 계산해 보여주는 어플리케이션을 구현하고자 한다.

## 기능명세
### Index 페이지
Task 목록을 나타내는 페이지. 각 Subtask 목록을 나타내기 위해서도 사용된다.

- Task 목록(테이블)
- 각 task title 클릭시
    - Subtask가 있다면 → subtask 목록으로 이동 ✅
    - 없다면 → `hx-confirm="서브태스크 생성 페이지로 이동합니다."` 또는 완료?? 완료 어떻게 하지? ✅
- 제목에 Objective 유지하기
- Navbar에 breadcrum 구현하기

### Create 페이지 ✅
Supertask가 없는 태스크(`supertask=None`. Objective라 칭한다) 및 subtask를 생성하기 위해서 사용된다.

- pk를 받을 수도 있고, 받지 않을 수도 있다.
    - pk가 None일 경우 Objective를 생성한다 → Index 페이지로 리다이렉트한다.
    - pk가 유효할 경우 Task를 생성한다 → 같은 레벨에 있는 Task 목록을 렌더링한다.

### Task 페이지
Supertask를 갖는 Task 목록을 보여주는 페이지.

## 데이터
### 테이블
1. title
2. 달성률
3. 시간 측정 버튼
4. 완료 버튼(Completed)
5. 각 Subtask가 현재 Task에서 차지하는 비율
0. 테이블 밑에 Create Subtask

### 사이드바(팝업)
1. Description ✅
    - (마크다운)
2. Subtask 한눈에 보기(title, 달성률/완료여부) → 리스트로 일단 구현
3. Create Subtask ✅
4. 선택한 Task Update, Delete → 버튼 구현됨.

#### 구현할 기능들
- Update
- Delete
- 달성률 계산해 보여주기
- 완료여부
    - 달성률 100% 또는 체크되었을 때 완료가 됨.
- 마크다운
- 브레드크럼 → 캐시? 세션?
- 시간 측정하기 → 쿠키 + `setInterval` (js, [코딩애플](https://youtu.be/oWSNOrBbOIU?t=246))
- 시간 측정해 데이터베이스에 기록하기 (`DurationField`?)
- 타입별 필터링하기.
- 타입별 평균 완료 시간 측정하기 → 같은 타입을 가진 다른 태스크에 추정 완료 시간 보여주기
- 완료되지 않은 목록만 볼 수 있게 필터링하기
- 완료한 목록 보기
