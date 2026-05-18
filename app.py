import streamlit as st
import main
import result

# 최초 실행 시 page 초기화
if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    main.show()

elif st.session_state.page == "result":
    result.show()