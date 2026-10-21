import streamlit as st
import random
import time

# 1. 頁面基本配置與全域樣式（隱藏 Streamlit 預設元件）
st.set_page_config(page_title="Happy Birthday Surprise!", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

# 壽星設定（可自由修改名字）
SU_XING_NAME = "壽星名字"

# 2. 初始化 Session State 狀態控制
if "page" not in st.session_state:
    st.session_state.page = "button_page"

# 初始化隨機顏色（固定在 session_state 中，避免每次 rerun 都變色）
if "chosen_name_color" not in st.session_state:
    text_colors = ["#FF6B6B", "#4DABF7", "#FFD43B", "#69DB7C", "#DA77F2", "#A9E34B"]
    st.session_state.chosen_name_color = random.choice(text_colors)
    st.session_state.chosen_hb_color = random.choice([c for c in text_colors if c != st.session_state.chosen_name_color])

# 3. 監聽網址上的 query_params（新版 Streamlit 使用 st.query_params）
# 只要偵測到 click_trigger=true，就代表使用者真的按下了紅色按鈕
if st.query_params.get("click_trigger") == "true":
    st.session_state.page = "surprise_page"

# --- 頁面路由分流 ---
if st.session_state.page == "button_page":
    
    # 僅注入給 Streamlit 按鈕外觀的純 CSS 樣式（完全移除了排版、定位與 HTML 標籤）
    st.markdown("""
    <style>
    /* 這裡將原本的 .real-metal-button 樣式直接綁定給 Streamlit 的按鈕元素 */
    div.stButton > button {
        position: relative !important; /* 必須設定為 relative，以便讓偽元素絕對定位 */
        width: 160px !important;
        height: 160px !important;
        border-radius: 50% !important;
        background: radial-gradient(circle at 50% 30%, #ffffff 0%, #dcdcdc 40%, #aaaaaa 70%, #555555 100%) !important;
        border: 2px solid #666666 !important;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.25), inset 0 -5px 15px rgba(0,0,0,0.2) !important;
        cursor: pointer !important;
        transition: all 0.2s ease-in-out !important;
        padding: 0 !important; /* 清空內距，避免干擾 */
        overflow: hidden !important;
    }
    
    /* 利用偽元素 (::after) 精確將紅色的核心置中塞進按鈕裡 */
    div.stButton > button::after {
        content: "" !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important; /* 絕對置中 */
        width: 80% !important;  /* 紅色核心佔大按鈕的比例 */
        height: 80% !important;
        border-radius: 50% !important;
        background-color: #ff0000 !important;
        background-image: radial-gradient(circle at 50% 30%, #ff6b6b 0%, #ff0000 50%, #aa0000 90%) !important;
        box-shadow: inset 0 5px 10px rgba(255,255,255,0.4), 0 5px 10px rgba(0,0,0,0.3) !important;
    }

    /* 懸停與點擊特效 */
    div.stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 20px 40px rgba(255, 0, 0, 0.3), 0 0 15px rgba(0, 0, 0, 0.1) !important;
    }
    div.stButton > button:active {
        transform: scale(0.98) !important;
    }
    </style>
""", unsafe_allow_html=True)

    # 1. 垂直置中：利用多個內建空行，將中間的按鈕穩穩推到網頁的垂直中央
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    # 2. 水平置中：使用超高比例 [2.5, 1, 2.5] 進行極限壓縮，把中間格子縮小到跟按鈕一樣寬
    col1, col2, col3 = st.columns([2, 1, 2.5])
    
    with col2:
        if st.button("", key="red_button"): # 按鈕文字留空，只秀出紅鈕外觀
            st.session_state.page = "surprise_page"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 畫面 2：煙火與 Dinotaeng Quokka 驚喜慶生 ---
elif st.session_state.page == "surprise_page":
    st.html("""
        <style>
        /* 1. 全黑夜空背景 */
        .stApp {
            background-color: #000000 !important;
        }
        
        /* 2. 文字與圖片發光樣式 */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp li, 
        .stMarkdown p, .stText, [data-testid="stMarkdownContainer"] p {
            color: #FFFFFF !important;
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.6);
        }
        [data-testid="stImage"] img {
            background-color: rgba(255, 255, 255, 0.95) !important;
            border-radius: 16px !important;
            padding: 12px !important;
            box-shadow: 0 0 25px rgba(255, 255, 255, 0.8) !important;
        }
        [data-testid="stAppViewContainer"], .main, .block-container {
            background: transparent !important;
        }

        /* 🎇 強制讓中間欄位裡面的所有 Streamlit 區塊物件（文字、圖片、空位）全部完美水平居中 */
        div[data-testid="stColumn"]:nth-of-type(2) [data-testid="stVerticalBlock"] > div {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            width: 100% !important;
        }
        
        /* 確保中間欄位的 markdown 容器和文字本身也是置中的 */
        div[data-testid="stColumn"]:nth-of-type(2) .stMarkdown {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
        }

        /* 3. 煙火畫布 */
        .firework-canvas {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            pointer-events: none;
            z-index: 99999;
        }
        
        /* 火箭升空軌跡 */
        .rocket {
            position: absolute;
            bottom: 0; width: 3px; height: 40px;
            background: linear-gradient(to top, transparent, #FFF, #FFA07A); 
            border-radius: 50%; opacity: 0;
        }
        
        .burst {
            position: absolute; 
            transform: translate(-50%, -50%);
            width: 1px; height: 1px; opacity: 0;
        }
        
        .line-particle {
            position: absolute; 
            bottom: 0; left: 50%;
            width: 3px; height: 0px;
            border-radius: 4px;
            transform-origin: bottom center;
        }

        /* 三發煙火的位置、顏色與交錯時間控制 */
        .r1 { left: 50%; animation: launch 6.0s ease-in infinite; animation-delay: 0s; }
        .b1 { top: 35%; left: 50%; animation: explode 6.0s ease-out infinite; animation-delay: 0s; }
        .b1 .line-particle { 
            background: linear-gradient(to top, #FFA07A, #FF7F50, #FFF); 
            box-shadow: 0 0 8px #FF7F50;
            animation: spark-spread 6.0s cubic-bezier(0.1, 0.8, 0.25, 1) infinite; animation-delay: 0s;
        }

        .r2 { left: 20%; animation: launch-low 6.0s ease-in infinite; animation-delay: 1.8s; }
        .b2 { top: 50%; left: 20%; animation: explode 6.0s ease-out infinite; animation-delay: 1.8s; }
        .b2 .line-particle { 
            background: linear-gradient(to top, #EEE8AA, #DAA520, #FFF); 
            box-shadow: 0 0 8px #DAA520;
            animation: spark-spread 6.0s cubic-bezier(0.1, 0.8, 0.25, 1) infinite; animation-delay: 1.8s;
        }

        .r3 { left: 80%; animation: launch-high 6.0s ease-in infinite; animation-delay: 3.6s; }
        .b3 { top: 42%; left: 80%; animation: explode 6.0s ease-out infinite; animation-delay: 3.6s; }
        .b3 .line-particle { 
            background: linear-gradient(to top, #DDA0DD, #BA55D3, #FFF); 
            box-shadow: 0 0 8px #BA55D3;
            animation: spark-spread 6.0s cubic-bezier(0.1, 0.8, 0.25, 1) infinite; animation-delay: 3.6s;
        }

        @keyframes launch { 0% { bottom: 0; opacity: 1; height: 50px; } 18% { opacity: 1; } 20%, 100% { bottom: 65%; opacity: 0; height: 5px; } }
        @keyframes launch-low { 0% { bottom: 0; opacity: 1; height: 50px; } 18% { opacity: 1; } 20%, 100% { bottom: 50%; opacity: 0; height: 5px; } }
        @keyframes launch-high { 0% { bottom: 0; opacity: 1; height: 50px; } 18% { opacity: 1; } 20%, 100% { bottom: 58%; opacity: 0; height: 5px; } }
        @keyframes explode { 0%, 19% { opacity: 0; } 21%, 70% { opacity: 1; } 85%, 100% { opacity: 0; } }
        @keyframes spark-spread {
            0%, 19% { height: 0px; transform: rotate(var(--rot)) translateY(0px); opacity: 0; }
            21% { height: 35px; transform: rotate(var(--rot)) translateY(0px); opacity: 1; }
            35%, 70% { height: 75px; transform: rotate(var(--rot)) translateY(var(--dist, 100px)); opacity: 1; }
            85%, 100% { height: 10px; transform: rotate(var(--rot)) translateY(var(--dist, 120px)); opacity: 0; }
        }
        </style>
        
        <div class="firework-canvas">
            <div class="rocket r1"></div>
            <div class="burst b1">
                <div class="line-particle" style="--rot:0deg; --dist:120px;"></div><div class="line-particle" style="--rot:22.5deg; --dist:110px;"></div>
                <div class="line-particle" style="--rot:45deg; --dist:125px;"></div><div class="line-particle" style="--rot:67.5deg; --dist:115px;"></div>
                <div class="line-particle" style="--rot:90deg; --dist:130px;"></div><div class="line-particle" style="--rot:112.5deg; --dist:110px;"></div>
                <div class="line-particle" style="--rot:135deg; --dist:120px;"></div><div class="line-particle" style="--rot:157.5deg; --dist:115px;"></div>
                <div class="line-particle" style="--rot:180deg; --dist:125px;"></div><div class="line-particle" style="--rot:202.5deg; --dist:110px;"></div>
                <div class="line-particle" style="--rot:225deg; --dist:130px;"></div><div class="line-particle" style="--rot:247.5deg; --dist:115px;"></div>
                <div class="line-particle" style="--rot:270deg; --dist:120px;"></div><div class="line-particle" style="--rot:292.5deg; --dist:110px;"></div>
                <div class="line-particle" style="--rot:315deg; --dist:125px;"></div><div class="line-particle" style="--rot:337.5deg; --dist:115px;"></div>
            </div>
            <div class="rocket r2"></div>
            <div class="burst b2">
                <div class="line-particle" style="--rot:10deg; --dist:90px;"></div><div class="line-particle" style="--rot:35deg; --dist:85px;"></div>
                <div class="line-particle" style="--rot:65deg; --dist:95px;"></div><div class="line-particle" style="--rot:95deg; --dist:80px;"></div>
                <div class="line-particle" style="--rot:120deg; --dist:90px;"></div><div class="line-particle" style="--rot:145deg; --dist:85px;"></div>
                <div class="line-particle" style="--rot:175deg; --dist:100px;"></div><div class="line-particle" style="--rot:205deg; --dist:80px;"></div>
                <div class="line-particle" style="--rot:230deg; --dist:95px;"></div><div class="line-particle" style="--rot:255deg; --dist:85px;"></div>
                <div class="line-particle" style="--rot:285deg; --dist:90px;"></div><div class="line-particle" style="--rot:315deg; --dist:80px;"></div>
                <div class="line-particle" style="--rot:340deg; --dist:95px;"></div>
            </div>
            <div class="rocket r3"></div>
            <div class="burst b3">
                <div class="line-particle" style="--rot:0deg; --dist:100px;"></div><div class="line-particle" style="--rot:30deg; --dist:105px;"></div>
                <div class="line-particle" style="--rot:60deg; --dist:95px;"></div><div class="line-particle" style="--rot:90deg; --dist:110px;"></div>
                <div class="line-particle" style="--rot:120deg; --dist:100px;"></div><div class="line-particle" style="--rot:150deg; --dist:95px;"></div>
                <div class="line-particle" style="--rot:180deg; --dist:105px;"></div><div class="line-particle" style="--rot:210deg; --dist:90px;"></div>
                <div class="line-particle" style="--rot:240deg; --dist:110px;"></div><div class="line-particle" style="--rot:270deg; --dist:100px;"></div>
                <div class="line-particle" style="--rot:300deg; --dist:95px;"></div><div class="line-particle" style="--rot:330deg; --dist:105px;"></div>
            </div>
        </div>
    """)
    
    # 設置三欄佈局：左可愛動圖 | 中間主秀區（文字+蛋糕） | 右可愛動圖
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.write("")

        st.image("https://cdn2.cdnstep.com/VukU4adwKcicOyiBKqfI/15-1.png", use_container_width=True)

    with col3:
        st.write("")
        st.image("https://cdn2.cdnstep.com/2O2ry7IEp5pFMHQyybcs/5-1.png", use_container_width=True)
        

    with col2:
        # 使用內聯樣式建立一個 flex 置中容器
        st.markdown('', unsafe_allow_html=True)
        
        name_placeholder = st.empty()
        hb_placeholder = st.empty()
        
        time.sleep(1.5)

        SU_XING_NAME = "Tracy"  
        chosen_name_color = "#FF4B4B"  
        chosen_hb_color = "#FFD700"    
       
        
        full_name_text = f" {SU_XING_NAME} "
        current_name = ""
        for char in full_name_text:
            current_name += char
            name_placeholder.markdown(f"<h1 style='color: {chosen_name_color}; font-size: 35px; font-weight: 900; font-family: \"Comic Sans MS\", sans-serif; text-shadow: 0 0 10px {chosen_name_color}; text-align: center; width: 100%; margin-bottom: 10px;'>{current_name}</h1>", unsafe_allow_html=True)
            time.sleep(0.15)
            
        
        full_hb_text = "🎉生日快樂🎉"
        current_hb = ""
        for char in full_hb_text:
            current_hb += char
            hb_placeholder.markdown(f"<h2 style='color: {chosen_hb_color}; font-size: 45px; font-weight: 900; font-family: \"Comic Sans MS\", sans-serif; text-shadow: 0 0 15px {chosen_hb_color}; text-align: center; width: 100%;'>{current_hb}</h2>", unsafe_allow_html=True)
            time.sleep(0.15)

        # 🟢 蛋糕往下移：margin-top 從 30px 增加到 70px，拉開與文字的距離
        st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)

        # 渲染置中蛋糕圖片與說明文字
        st.markdown(
            """
            <div style="display: flex; justify-content: center; width: 100%;">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgh2i9XJe27DGb1JGHaUhCJ5j-nwt7nAJ0oxYKmDOYODM1cbyJ19LjMagL&s=10">
            </div>
            <p style="text-align: center; font-size: 16px; margin-top: 15px; color: rgba(255,255,255,0.8) !important; font-weight: bold;">
                來自明賢與愛喝小鯨魚的同事的祝福~~
            </p>
            """, 
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
