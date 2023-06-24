# Track Cracker
Divide and Conquer your Objectives.

## Motivation
학습 계획과 달성률을 쉽게 작성/기록 및 보여주는 앱을 찾기 쉽지 않다.  
Objective를 정하고 이에 대한 Key Result 들을 Subtask 들로 나눈 뒤, 각 Task와 Objective의 달성률을 계산해 보여주는 어플리케이션을 구현하고자 한다.

## 기능명세
### Index 페이지
Task 목록을 나타내는 페이지. 각 Subtask 목록을 나타내기 위해서도 사용된다.

- Task 목록(테이블)
- 각 row 클릭시
    - Subtask가 있다면 → subtask 목록으로 이동
    - 없다면 → `hx-confirm="서브태스크 생성 페이지로 이동합니다."` 또는 완료?? 완료 어떻게 하지?
- 제목에 Objective 유지하기
- Navbar에 breadcrum 구현하기

### Create 페이지
Supertask가 없는 태스크(`supertask=None`. Objective라 칭한다) 및 subtask를 생성하기 위해서 사용된다.

- pk를 받을 수도 있고, 받지 않을 수도 있다.
    - pk가 None일 경우 Objective를 생성한다 → Index 페이지로 리다이렉트한다.
    - pk가 유효할 경우 Task를 생성한다 → 같은 레벨에 있는 Task 목록을 렌더링한다.
