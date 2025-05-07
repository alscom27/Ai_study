import streamlit as st
import pandas as pd
from datetime import datetime, date
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import time

# import numpy

# 페이지 기본 설정
st.set_page_config(page_title="Todo List", layout="wide")

# 개체 시스템 설정
# 세션 상태 초기화 처음 실행 시 한 번만 설정됨
if "task_list" not in st.session_state:
    st.session_state.task_list = []  # 할 일 목록

# add : 등록 , edit : 수정
if "mode" not in st.session_state:
    st.session_state.mode = None  # None, "add", "edit"

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None  # 수정할 항목 인덱스

if "next_number" not in st.session_state:
    st.session_state.next_number = 0

# 앱 제목
st.title("Todo-List")


# 등록, 수정 버튼
col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 1, 1])

with col1:
    if st.button("➕ 등록하기"):
        st.session_state.mode = "add"
        st.session_state.edit_index = None  # 새 항목을 등록하는거여서 인덱스 없음

with col2:
    if st.button("✏️ 수정하기"):
        st.session_state.mode = "edit"  # 세션을 수정 모드로 전환


# 입력 폼
if st.session_state.mode in ["add", "edit"]:
    st.subheader("할 일 입력")

    default_task = ""
    default_date = date.today()

    if st.session_state.mode == "edit" and st.session_state.edit_index is not None:
        current_task = st.session_state.task_list[st.session_state.edit_index]
        default_task = current_task["할 일"]
        default_date = datetime.strptime(current_task["만료 기간"], "%Y-%m-%d").date()

    # 입력값을 바로 변수에 할당
    task = st.text_input("할 일을 입력하세요", value=default_task)
    due = st.date_input("기한을 입력하세요", value=default_date)

    # 확인, 취소 버튼
    c1, c2, c3, c4 = st.columns([6, 2, 1, 1])
    with c3:
        if st.button("확인"):
            if task:
                now = datetime.now().strftime("%Y-%m-%d")
                if st.session_state.mode == "add":

                    # st.session_state.next_number = len(st.session_state.task_list)
                    st.session_state.next_number += 1
                    # st.info(st.session_state.next_number)
                    # time.sleep(1)
                    # 새 항목 추가
                    st.session_state.task_list.append(
                        {
                            "번호": st.session_state.next_number,
                            "할 일": task,
                            "상태": "진행 중",
                            "등록 기간": now,
                            "만료 기간": due.strftime("%Y-%m-%d"),
                        }
                    )

                    with c1:
                        st.success(f"{task}가 등록 되었습니다.")
                        time.sleep(0.5)

                elif (
                    st.session_state.mode == "edit"
                    and st.session_state.edit_index is not None
                ):
                    # 기존 항목 수정
                    st.session_state.task_list[st.session_state.edit_index][
                        "할 일"
                    ] = task
                    st.session_state.task_list[st.session_state.edit_index][
                        "만료 기간"
                    ] = due.strftime("%Y-%m-%d")

                    with c1:
                        st.success(f"{task}로 수정 되었습니다.")
                        time.sleep(0.5)
                # 입력 완료 후 초기화 및 새로고침
                st.session_state.mode = None
                st.session_state.edit_index = None
                st.rerun()
            else:
                st.warning("할 일을 입력하세요.")

    with c4:
        if st.button("취소"):
            st.session_state.mode = None
            st.session_state.edit_index = None
            st.rerun()


# 표 (할 일 목록) Aggrid
if st.session_state.task_list:
    # 데이터프레임 생성 및 번호 컬럼 추가
    df = pd.DataFrame(st.session_state.task_list)
    # df.insert(0, "번호", range(1, len(df) + 1)) 힘들어서 위에 세션 리스트에 그냥 넣어버림

    # Aggrid 설정
    gb = GridOptionsBuilder.from_dataframe(df)
    # 단일 선택, 체크박스
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    gb.configure_column("번호", width=80)
    grid_options = gb.build()

    # Aggrid 출력
    grid_response = AgGrid(
        df,
        grid_options,
        height=400,
        update_mode=GridUpdateMode.SELECTION_CHANGED,  # 선택 변경 시 반영
        fit_columns_on_grid_load=True,
    )

    # 선택 행 가져오기
    selected = grid_response["selected_rows"]
    if selected is not None and len(selected) > 0:
        # row = df.values[0][0] - 1
        row = list(selected.index).pop()
        # st.info(row)
        # st.info(df)
        # st.info(df.to_numpy()[0][0])
        selected_index = int(row)
        st.session_state.edit_index = selected_index

    # 삭제 / 상태 변경 버튼
    with col3:
        if (
            st.button("❌ 선택 항목 삭제")
            and selected is not None
            and len(selected) > 0
        ):
            # selected_index = df.values[0][0] - 1
            st.session_state.task_list.pop(selected_index)
            st.success("삭제되었습니다.")

            st.rerun()

    with col4:
        if st.button("✅ 상태 변경") and selected is not None and len(selected) > 0:
            current = st.session_state.task_list[selected_index]["상태"]
            st.session_state.task_list[selected_index]["상태"] = (
                "완료" if current == "진행 중" else "진행 중"
            )
            st.success("상태가 변경되었습니다.")
            st.rerun()


else:
    st.info("할 일이 없습니다. 등록해주세요.")

with col5:
    if st.button("🔁 화면 갱신"):
        st.rerun()

with col6:
    if st.button("♻️ 번호 초기화"):
        st.session_state.next_number = 0
