import streamlit as st

st.set_page_config(
    page_title="Options Pricing Explorer",
    layout="wide",
)

home = st.Page("pages/home_page.py", title="Home", icon=":material/home:", default=True)
bs_page = st.Page("pages/black_scholes_page.py", title="Black-Scholes", icon=":material/show_chart:")
bin_page = st.Page("pages/binomial_page.py", title="Binomial", icon=":material/account_tree:")
binary_page = st.Page("pages/binary_page.py", title="Binary / Digital", icon=":material/toggle_on:")
spread_page = st.Page("pages/binary_spread_page.py", title="Binary Spread", icon=":material/call_split:")
conv_page = st.Page("pages/convergence_page.py", title="Convergence", icon=":material/compare_arrows:")

pg = st.navigation([home, bs_page, bin_page, binary_page, spread_page, conv_page])
pg.run()
