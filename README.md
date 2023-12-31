# Track Cracker
Divide and Conquer your Objectives.  
[Link](http://43.201.65.107/)

## Motivation
학습 계획과 달성률을 쉽게 작성/기록 및 보여주는 앱을 찾기 쉽지 않다.  
Objective를 정하고 이에 대한 Key Result 들을 Subtask 들로 나눈 뒤, 각 Task와 Objective의 달성률을 계산해 보여주는 어플리케이션을 구현하고자 한다.

## 기능명세
### Index 페이지
Objective와 서브태스크 목록을 나타내는 페이지.

- Objective 이름
- Objective 테이블
    - Objective Name 클릭시 offcanvas로 해당 objective의 description과 subtask 목록을 보여준다.
- CREATE objective, DELETE objective(table, offcanvas), UPDATE objective(offcanvas)

### Task 페이지
Task와 서브태스크 목록을 나타내는 페이지.

- Objective 이름
- Objective 달성률
- Task 테이블
    - Task Name 클릭시 offcanvas에 해당 Task의 description과 subtask 목록을 보여준다.
- CREATE task, DELETE task(table, offcanvas), UPDATE task(offcanvas)


### Subtask 페이지

- Objective 이름 및 달성률
- Task 이름 및 달성률
- Subtask 테이블
    - Task Name 클릭시 offcanvas에 해당 Task의 description과 subtask 목록을 보여준다.
- CREATE(subtask), DELETE task(table, offcanvas), UPDATE task(offcanvas)


### Evaluating Achievement
- Task 생성, 삭제시 참조 Supertask의 Subtasks의 Proportion, Achievement를 사용해 Supertask의 Achievement를 다시 작성한다.
- `post_save`, `post_delete` 시그널을 사용하고 아래에서 supertask가 `None`이 될 때까지 올라가며 작성한다.


# 구현할 것들
- Navbar에 해당 Objective Title 유지하기, 달성률 보여주기 ✅ → task, subtask 페이지 상단에 구현
- Achievement → Progress Bar로 구현하기 ✅
- breadcrumb 구현하기(링크) ✅
- `Task` 모델 하나만 사용하도록 리팩토링 ✅
- 완료 체크하기
    - 완료 체크시 Achievement는 1.0이 되지만, 서브태스크들의 Achievement는 그대로 유지한다. ✅
    - `completed`가 `True`일 때 `achievement` → `1.0` ✅
    - `completed`가 `False`일 때 `achievement` → 다시 계산 ✅
    - Achievement가 1.0이 되면 완료 체크, 내려가면 완료 체크 해제 ✅
        - 처음 생성된 객체에는 수행할 필요 없으니 handler에서 작업
        - 만약 하위 태스크가 모두 completed라면 supertask의 completed는 disabled
- Accumulate Proportion 입력할 수 있게 하기
    - FormHelper? 사용
- detail offcanvas 스타일링 ✅
- 랜딩페이지 ✅
- Account ✅
- 타입별 필터, 완료, 미완 모아보기
- 오늘의 할일 목록에 추가하기 기능 → 오늘의 할일 페이지
- 소요시간 측정
    - 예상 소요시간 계산하기