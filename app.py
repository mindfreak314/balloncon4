import streamlit as st
import time
import pandas as pd
import utils

st.set_page_config(page_title="BC4", page_icon = "👑",  layout="wide")

st.title("Ballon Con 4 @ Countdown")

ranking_method = utils.hareruya_permutations_with_draw_and_byes

current_round = utils.get_finished_round()

control_sheet = utils.get_control_sheet()
oppo_dict = utils.get_oppo_dict(control_sheet)
match_logs = utils.get_match_logs(control_sheet)
# standings_after_rounds = utils.get_standings_after_rounds(control_sheet, match_logs, method=ranking_method)

round_df = pd.read_excel("control_sheet.ods", engine="odf", sheet_name=f"round {current_round}")


########################################################################################################################
# maual R1 losses
r1_loss = [
    # "",
]
loss_matches = []
for player in r1_loss:
    match_log_element = {}
    match_log_element["match_players"] = [player]
    match_log_element["match_result"] = "loss"
    match_log_element["round"] = 1
    match_log_element["pod"] = 0
    loss_matches.append(match_log_element)
match_logs = loss_matches + match_logs
########################################################################################################################

# # @st.cache_data
# def prep_control_sheet(control_sheet):
#     control_sheet = utils.add_wld(control_sheet, match_logs)
#     control_sheet = utils.add_standing(control_sheet, match_logs, method=ranking_method)

#     return control_sheet

# control_sheet = prep_control_sheet(control_sheet)

# search_player = st.text_input('Search player...', '', )


def color_result(result):
    color_map = {
        "win": "green",
        "loss": "red",
        "draw": "yellow", 
        "BYE": "white"
    }
    color = color_map[result]
    return f'color: {color}'

f = {
'Points before':'{:.2f}',
'Points after':'{:.2f}',
'Points':'{:.2f}',
}

show_current_round = True
top16_df = pd.read_excel("control_sheet.ods", engine="odf", sheet_name="top 16")
# if 'Result' in top16_df.columns:
#     top16_df = top16_df.style.applymap(color_result, subset=['Result']).format(f).hide(axis="index")
# else:
#     top16_df = top16_df.style.hide(axis="index")

# st.markdown(top16_df.to_html(), unsafe_allow_html=True)
try:
    with st.expander("Top 16"):

        columns = st.columns(4)

        col_counter = 0
        for i in top16_df.Pod.unique():
            columns[col_counter%4].markdown(top16_df[top16_df.Pod == i].style.hide(axis="index").to_html(), unsafe_allow_html=True)
            columns[col_counter%4].write("")
            col_counter += 1
        show_current_round=False
except:
    pass

# try:
#     top4_df = pd.read_excel("control_sheet.ods", engine="odf", sheet_name="top 4")
#     if 'Result' in top4_df.columns:
#         top4_df = top4_df.style.applymap(color_result, subset=['Result']).format(f).hide(axis="index")
#     else:
#         top4_df = top4_df.style.hide(axis="index")
#     with st.expander("Top 4"):
#         st.markdown(top4_df.to_html(), unsafe_allow_html=True)
#     show_current_round=False
# except:
#     pass

# try:
#     top16_df = pd.read_excel("control_sheet.ods", engine="odf", sheet_name="top 16")
#     if 'Result' in top16_df.columns:
#         top16_df = top16_df.style.applymap(color_result, subset=['Result']).format(f).hide(axis="index")
#     else:
#         top16_df = top16_df.style.hide(axis="index")
#     with st.expander("Top 16"):
#         st.markdown(top16_df.to_html(), unsafe_allow_html=True)
#     show_current_round=False
# except:
#     pass




if show_current_round:
    # st.title(f"Pairings for round {current_round}")

    # Sort players by name
    # df = round_df.sort_values(by="Player").rename({"Player": "Player (sorted alphabetically)"}, axis=1).drop("Result", axis=1).reset_index(drop=True)

    st.title("Game Results after Round 5")
    df = pd.read_csv("current_standing.csv").sort_values("Player")

    # with st.expander("",expanded =True):
        # st.markdown(round_df.sort_values("Player").drop("Result", axis=1).style.hide(axis="index").to_html(), unsafe_allow_html=True)
    st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    # Configuration
    scroll_speed = 75  # Adjust scrolling speed (lower = faster)

    # Custom CSS for transparent headers, equal column widths & smooth scrolling
    st.markdown(f"""
        <style>
        .scroll-container {{
            width: 100%;
            overflow: hidden;
            position: relative;
            height: 800px; /* Adjust height */
            border: 1px solid #ddd;
        }}
        
        .scrolling-table {{
            display: flex;
            flex-direction: column;
            animation: marquee {scroll_speed}s linear infinite;
        }}

        /* Duplicate content for seamless loop */
        .scrolling-table::after {{
            content: "";
            display: block;
            height: 100%;
        }}

        @keyframes marquee {{
            from {{ transform: translateY(0%); }}
            to {{ transform: translateY(-50%); }} /* Scroll only half so it loops seamlessly */
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 0;
            table-layout: fixed; /* Ensures equal column widths */
        }}

        th {{
            position: sticky;
            top: 0;
            background: rgba(255, 255, 255, 0.1); /* Transparent background */
            backdrop-filter: blur(5px); /* Smooth blending effect */
            z-index: 2;
            text-align: left;
            padding: 10px;
            border-bottom: 2px solid black;
        }}

        td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Generate HTML table (duplicated for seamless scrolling)
    table_html = df.to_html(index=False, escape=False)

    # Inject headers separately to keep them fixed
    styled_table = f"""
        <div class="scroll-container">
            <table>
                <thead>{table_html.split("<thead>")[1].split("</thead>")[0]}</thead>
            </table>
            <div class="scrolling-table">
                <table>{table_html.split("</thead>")[1]}</table>
                <table>{table_html.split("</thead>")[1]}</table> <!-- Duplicate for seamless looping -->
            </div>
        </div>
    """

    # Display scrolling table
    st.markdown(styled_table, unsafe_allow_html=True)

    #######

    # df = round_df.sort_values(by="Player").reset_index(drop=True)

    # # Configuration
    # chunk_size = 10  # Number of players to show at once
    # scroll_speed = 1  # Seconds before updating

    # # Custom CSS for smooth scrolling effect
    # st.markdown("""
    #     <style>
    #     @keyframes scroll {
    #         from { opacity: 0; transform: translateY(10px); }
    #         to { opacity: 1; transform: translateY(0px); }
    #     }
    #     .scrolling-table {
    #         animation: scroll 0.8s ease-in-out;
    #     }
    #     table {
    #         width: 100%;
    #         border-collapse: collapse;
    #     }
    #     th, td {
    #         padding: 8px;
    #         text-align: left;
    #         border-bottom: 1px solid #ddd;
    #     }
    #     </style>
    # """, unsafe_allow_html=True)
    # display_area = st.empty()
    # index = 0

    # while True:
    #     # Get current chunk of players
    #     chunk = pd.concat([df.iloc[index:], df.iloc[:index]]).head(chunk_size)

    #     # Convert chunk to HTML table with animation class
    #     table_html = chunk.to_html(index=False, escape=False)
    #     styled_table = f'<div class="scrolling-table">{table_html}</div>'

    #     # Display with smooth transition
    #     display_area.markdown(styled_table, unsafe_allow_html=True)

    #     # Increment index for scrolling effect
    #     index = (index + 1) % len(df)

    #     # Pause before next update
    #     time.sleep(scroll_speed)

    ########
    
    # st.markdown(round_df.sort_values("Player").drop("Result", axis=1).style.hide(axis="index").to_html(), unsafe_allow_html=True)


    



# with st.expander("Standing"):
#     control_sheet_standing = control_sheet.copy().reset_index()
#     if search_player:
#         control_sheet_standing = control_sheet_standing[control_sheet_standing.Player.str.lower().str.contains(search_player.lower())]
#     # control_sheet_standing.drop(["dropped", "n_3P_pods"], axis = 1, inplace=True)
#     # control_sheet_standing = control_sheet_standing[["Rank", "Player", "Points", "Regular points", "win", "loss", "draw"]]
#     control_sheet_standing = control_sheet_standing[["Rank", "Player", "Points", "win", "loss", "draw", "bye"]]
#     control_sheet_standing[["win", "loss", "draw", "bye"]] = control_sheet_standing[["win", "loss", "draw", "bye"]].astype(int)
#     # control_sheet_standing["Points"] = control_sheet_standing["Points"].astype(int)
#     st.markdown(control_sheet_standing.style.format(f).hide(axis="index").to_html(), unsafe_allow_html=True)



# replace_round_strings = {
#     6: "Top 16",
#     7: "Top 4",
# }

# round_strings = [x+1 for x in reversed(range(current_round))]

# new_round_strings = []
# for ele in round_strings:
#     if ele in replace_round_strings.keys():
#         print("sjdbfgsohdgbsludfebsoihfb", ele)
#         new_round_strings.append(replace_round_strings[ele])
#     else:
#         new_round_strings.append(ele)

# round_strings = new_round_strings

# display_round = st.radio("Round selection", round_strings, horizontal = True)




# if current_round > 0:

#     round_df = pd.read_excel("control_sheet.ods", engine="odf", sheet_name=f"round {display_round}")
#     if search_player:
#         round_df = round_df[round_df.Player.str.lower().str.contains(search_player.lower())]

#     if 'Result' in round_df.columns:
#         # merge with poitns before and after
#         round_df = (
#             round_df
#             # .merge(standings_after_rounds[display_round-1].rename({"Points":"Points before"}, axis = 1).reset_index(),  on="Player")
#             # .merge(standings_after_rounds[display_round].rename({"Points":"Points after"}, axis = 1).reset_index(),  on="Player")
#             )
        
#         # round_df[["Points before", "Points after"]] = round_df[["Points before", "Points after"]].astype(int)
#         # round_df[["Points before", "Points after"]] = round_df[["Points before", "Points after"]].round(decimals=2)
#         round_df = round_df.style.applymap(color_result, subset=['Result']).format(f).hide(axis="index")
#     else:
#         round_df = round_df.style.hide(axis="index")

#     st.markdown(round_df.to_html(), unsafe_allow_html=True)

#     st.write("")
#     with st.expander("Pairings for beamer"):
#         columns = st.columns(4)

#         col_counter = 0
#         for i in round_df.Pod.unique():
#             columns[col_counter%4].markdown(round_df[round_df.Pod == i].style.hide(axis="index").to_html(), unsafe_allow_html=True)
#             columns[col_counter%4].write("")
#             col_counter += 1