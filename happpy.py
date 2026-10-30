import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval
import random
# ==============================================================================
# 初始化與全域樣式設定
# ==============================================================================
st.set_page_config(page_title="2026 獵人試驗-壽星專屬場", page_icon="🎴", layout="centered")

# 初始化 Session State 用來控制關卡流程 (login -> water_test -> license)
if "stage" not in st.session_state:
    st.session_state.stage = "login"

# 用來記錄是否喝到了東巴的毒果汁
if "tonpa_trap" not in st.session_state:
    st.session_state.tonpa_trap = False


# 用來記錄水見式是否已經測試完成
if "water_test_completed" not in st.session_state:
    st.session_state.water_test_completed = False

# 監聽來自 HTML5 Canvas 小遊戲的通關訊號
if "game_passed" in st.query_params:
    st.session_state.stage = "water_test"
    # 清除 query_params 避免無限重整
    st.query_params.clear()
    st.rerun()

if "game_completed" not in st.session_state:
    st.session_state.game_completed = False

if "win" in st.query_params:
    st.session_state.game_completed = True

if st.session_state.game_completed:
    st.session_state.stage = "water_test"
    st.session_state.game_completed = False # 重設變數
    st.rerun()

if st.session_state.game_completed:
    st.session_state.stage = "test2_game"  # 👈 將原本的 "water_test" 改為 "test2_game"
    st.session_state.game_completed = False # 重置變數
    st.rerun()

if "stage" not in st.session_state:
    st.session_state.stage = "license"

if "page" not in st.session_state:
    st.session_state.page = "birthday_wish"

# 【字體調亮優化】自訂獵人風 CSS 樣式
st.markdown("""
<style>
    body { background-color: #1a1a1a; color: #ffffff; }
    .stApp { background-color: #1a1a1a; }
    
    /* 🛠️ 終極修正：強制按鈕、按鈕內的所有文字標籤（span, p）全部變深色 */
    .stApp div[data-testid="stButton"] button,
    .stApp div[data-testid="stButton"] button *,
    .stApp button[kind="secondary"],
    .stApp button[kind="secondary"] * {
        color: #1a1a1a !important;            /* 強制讓文字顯示深色（接近黑色） */
        background-color: transparent;         /* 內層標籤背景透明，才不會遮擋外層 */
        font-weight: bold !important;
        font-size: 16px !important;
    }

    /* 針對按鈕本體強制設定背景色與邊框 */
    .stApp div[data-testid="stButton"] button,
    .stApp button[kind="secondary"] {
        background-color: #ffffff !important;   /* 強制背景為白色 */
        border: 2px solid #ffcc00 !important;   /* 黃色邊框 */
        transition: all 0.3s ease !important;
    }
    
    /* 滑鼠移上去時的發光效果與文字色彩維持 */
    .stApp div[data-testid="stButton"] button:hover,
    .stApp div[data-testid="stButton"] button:hover *,
    .stApp button[kind="secondary"]:hover,
    .stApp button[kind="secondary"]:hover * {
        color: #1a1a1a !important;              /* 文字維持深色 */
    }

    .stApp div[data-testid="stButton"] button:hover,
    .stApp button[kind="secondary"]:hover {
        background-color: #ffcc00 !important;   /* 背景變黃色 */
        box-shadow: 0 0 15px #ffcc00 !important;
    }
    
    /* 🛠️ 東巴毒果汁按鈕專屬特殊樣式（亮橘色誘敵） */
    div[data-testid="stMarkdownContainer"] + div .tonpa-btn button {
        background: linear-gradient(45deg, #ff9900, #ff5500) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(255,85,0,0.4) !important;
    }
    div[data-testid="stMarkdownContainer"] + div .tonpa-btn button:hover {
        background: #ff5500 !important;
        box-shadow: 0 0 20px #ff5500 !important;
    }

    /* 標題調亮：增加強烈的發光特效 */
    .hunter-title { 
        font-family: 'Courier New', Courier, monospace; 
        color: #ffff00; 
        text-align: center; 
        font-weight: 900; 
        text-shadow: 0 0 15px #ffcc00, 0 0 5px #ff8800;
        letter-spacing: 2px;
    }
    
    /* 副標題與普通文字調亮 */
    h3, p, label, .stMarkdown { 
        color: #ffffff !important; 
        font-weight: 500;
    }
    
    /* 提示文字調亮：從暗灰改為清晰的亮白灰色 */
    .hint-text { 
        color: #e0e0e0 !important; 
        font-size: 0.95rem; 
        text-align: center; 
        margin-top: 10px; 
        text-shadow: 0 0 5px rgba(255,255,255,0.5);
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 【第一關】獵人試驗網站登入（號碼牌意象）
# ==============================================================================
if st.session_state.stage == "login":
    if st.session_state.tonpa_trap:
        st.markdown("<h1 style='color: #ff3333; text-align: center; font-weight: bold; text-shadow: 0 0 10px #ff0000;'>不要小看人類的惡意，呵！</h1>", unsafe_allow_html=True)
        
        # 顯示東巴
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQiXY9lg_blaVGMIPrOwzBuck0bojmV20j5ss4e7NacQ8WwqcbE6JQc2mqG&s=10", caption="東巴：『嘿嘿嘿』", use_container_width=True)
        
        st.error("真好騙。")
        
        btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 2])
        with btn_col2:
            if st.button("喝解藥", use_container_width=True):
                st.session_state.tonpa_trap = False
                st.rerun()

    else:
        st.markdown("<h1 class='hunter-title'>第 287 期 獵人試驗報到處</h1>", unsafe_allow_html=True)
        st.image("https://megapx-assets.dcard.tw/images/0f9e512e-a246-4435-9797-43f1a50d7bfc/640.jpeg", use_container_width=True)
    
        st.write("---")
        
        st.markdown("### 福利區")
        st.write("慶祝我們相識，要不要來杯果汁？")
        
        juice_col1, juice_col2, juice_col3 = st.columns([1.2, 1.6, 1.2])
        with juice_col2:
            with st.container():
                st.markdown('<div class="tonpa-btn">', unsafe_allow_html=True)
                if st.button("免費領取", use_container_width=True):
                    st.session_state.tonpa_trap = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### 奪取號碼牌")
        st.write("---")

        col1, col2 = st.columns(2)
    
        with col1:
            gon_code = st.text_input("小傑的編號：", type="default", placeholder="")
        
        with col2:
            killua_code = st.text_input("奇犽的編號：", type="default", placeholder="")
    
             
        st.markdown("""
            <style>
            div[data-testid="stTextInput"] { display: none !important; }
            div[data-testid="stButton"]:has(button:contains("提交報到資訊")) { display: none !important; }
            
            div.element-container:has(button[key="visible_gate_btn"]) { display: none; }
            </style>
        """, unsafe_allow_html=True)

        #  宣告畫面上唯一的實體跳轉按鈕
        if st.button("前往下個挑戰", key="visible_gate_btn", use_container_width=False):
            st.session_state.stage = "test1_game"  
            st.rerun()

        # 會到處狂飛的數字代碼
        flying_inputs_html = """
        <div id="game-container" style="position: relative; width: 100%; height: 450px; background-color: #262626; border-radius: 10px; border: 2px dashed #7f8c8d; overflow: hidden;">
            <div style="position: absolute; top: 12px; left: 12px; color: #ffcc00; font-size: 14px; font-weight: bold; text-shadow: 0 0 5px rgba(255,204,0,0.5);"></div>
            <div id="score-board" style="position: absolute; top: 12px; right: 12px; color: #ffffff; font-size: 14px; font-weight: bold;">
                抓到：<span id="captured-gon">❌ 小傑</span> | <span id="captured-killua">❌ 奇犽</span>
            </div>
            
            <!-- 🔴 【真實】小傑的號碼牌 -->
            <div id="gon-num" class="hunter-badge" style="position: absolute; left: 80px; top: 120px; width: 65px; height: 65px; background: #ffffff; border: 3px solid #e74c3c; border-radius: 50%; color: #1a1a1a; font-size: 22px; font-weight: 900; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 0 15px rgba(231,76,60,0.4); user-select: none; transition: transform 0.1s;">
                405
            </div>

            <!-- 🔴 【真實】奇犽的號碼牌 -->
            <div id="killua-num" class="hunter-badge" style="position: absolute; left: 400px; top: 220px; width: 65px; height: 65px; background: #ffffff; border: 3px solid #e74c3c; border-radius: 50%; color: #1a1a1a; font-size: 22px; font-weight: 900; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 0 15px rgba(231,76,60,0.4); user-select: none; transition: transform 0.1s;">
                99
            </div>

            <!-- 🔴 【假號碼干擾 1】 -->
            <div id="fake-1" class="hunter-badge" style="position: absolute; left: 200px; top: 80px; width: 65px; height: 65px; background: #ffffff; border: 3px solid #e74c3c; border-radius: 50%; color: #1a1a1a; font-size: 22px; font-weight: 900; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 0 15px rgba(231,76,60,0.4); user-select: none; transition: transform 0.1s;">
                404
            </div>

            <!-- 🔴 【假號碼干擾 2】 -->
            <div id="fake-2" class="hunter-badge" style="position: absolute; left: 550px; top: 150px; width: 65px; height: 65px; background: #ffffff; border: 3px solid #e74c3c; border-radius: 50%; color: #1a1a1a; font-size: 22px; font-weight: 900; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 0 15px rgba(231,76,60,0.4); user-select: none; transition: transform 0.1s;">
                403
            </div>

            <!-- 🔴 【假號碼干擾 3】 -->
            <div id="fake-3" class="hunter-badge" style="position: absolute; left: 300px; top: 320px; width: 65px; height: 65px; background: #ffffff; border: 3px solid #e74c3c; border-radius: 50%; color: #1a1a1a; font-size: 22px; font-weight: 900; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 0 15px rgba(231,76,60,0.4); user-select: none; transition: transform 0.1s;">
                16
            </div>
        </div>

        <script>
        function setupFlyingNumber(elementId, baseSpeed) {
            const el = document.getElementById(elementId);
            const container = document.getElementById('game-container');
            
            let dx = (Math.random() - 0.5) * baseSpeed;
            let dy = (Math.random() - 0.5) * baseSpeed;
            let posX = parseFloat(el.style.left);
            let posY = parseFloat(el.style.top);
            let isHovered = false;

            setInterval(() => {
                if (!isHovered) {
                    posX += dx;
                    posY += dy;

                    if (posX <= 0 || posX >= container.clientWidth - el.clientWidth) dx *= -1;
                    if (posY <= 0 || posY >= container.clientHeight - el.clientHeight) dy *= -1;

                    posX = Math.max(0, Math.min(posX, container.clientWidth - el.clientWidth));
                    posY = Math.max(0, Math.min(posY, container.clientHeight - el.clientHeight));

                    el.style.left = posX + 'px';
                    el.style.top = posY + 'px';
                }
            }, 16);

            el.addEventListener('mouseenter', () => {
                isHovered = true;
                if(Math.random() > 0.5) { 
                    posX = Math.random() * (container.clientWidth - el.clientWidth);
                    posY = Math.random() * (container.clientHeight - el.clientHeight);
                    el.style.left = posX + 'px';
                    el.style.top = posY + 'px';
                }
            });

            el.addEventListener('mouseleave', () => {
                isHovered = false;
                dx = (Math.random() - 0.5) * (baseSpeed + 5);
                dy = (Math.random() - 0.5) * (baseSpeed + 5);
            });
        }

        // 啟動所有號碼球的飛行
        setupFlyingNumber('gon-num', 13);
        setupFlyingNumber('killua-num', 16);
        setupFlyingNumber('fake-1', 14);
        setupFlyingNumber('fake-2', 12);
        setupFlyingNumber('fake-3', 15);

        // 正確點擊小傑
        document.getElementById('gon-num').addEventListener('click', function() {
            document.getElementById('captured-gon').innerHTML = "✅ 小傑(405)";
            document.getElementById('captured-gon').style.color = "#2ecc71";
            this.style.display = "none";
        });

        // 正確點擊奇犽
        document.getElementById('killua-num').addEventListener('click', function() {
            document.getElementById('captured-killua').innerHTML = "✅ 奇犽(99)";
            document.getElementById('captured-killua').style.color = "#3498db";
            this.style.display = "none";
        });
        </script>
        """
        components.html(flying_inputs_html, height=470)
       
# ==============================================================================
# 【第二關】「專注力」測驗
# ==============================================================================
elif st.session_state.stage == "test1_game":
    st.title("挑戰專注力的時候到了！")
    st.caption("控制藍色小方塊，沿著白色路徑移動到紅色終點。")

    game_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                background-color: #000;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: 'Arial', sans-serif;
                overflow: hidden;
            }
            #gameCanvas {
                border: 4px solid #333;
                background-color: #000;
                cursor: crosshair;
            }
            #jumpscare {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background-color: #000;
                z-index: 9999;
                text-align: center;
            }
            #jumpscare img {
                height: 100vh;
                width: auto;
            }
        </style>
    </head>
    <body>

        <canvas id="gameCanvas" width="800" height="600"></canvas>
        
        <div id="jumpscare">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaoHBEGXxkI4jtJ54AZwlEDD_K0o-hF0_R65wuQtGbItbb8fXnZzK12SQ&s=10" alt="Jumpscare">
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const jumpscareDiv = document.getElementById('jumpscare');

            let gameStarted = false;
            let player = { x: 100, y: 560, size: 8 }; 

            const whitePaths = [
                { x: 50, y: 530, w: 700, h: 50 },
                { x: 700, y: 350, w: 50, h: 230 },
                { x: 100, y: 350, w: 650, h: 50 },
                { x: 100, y: 170, w: 50, h: 230 },
                { x: 100, y: 170, w: 330, h: 50 },
                { x: 400, y: 130, w: 20, h: 40 },
                { x: 350, y: 130, w: 70, h: 20 },
                { x: 350, y: 90, w: 20, h: 50 },
                { x: 350, y: 90, w: 70, h: 20 },
                { x: 400, y: 60, w: 20, h: 45 },
                { x: 380, y: 0, w: 60, h: 60 }
            ];

            function drawMap() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#000000';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#ffffff'; 
                for (let i = 0; i < whitePaths.length - 1; i++) {
                    let p = whitePaths[i];
                    ctx.fillRect(p.x, p.y, p.w, p.h);
                }

                ctx.fillStyle = '#ff3c00';
                let end = whitePaths[whitePaths.length - 1];
                ctx.fillRect(end.x, end.y, end.w, end.h);
            }

            function drawPlayer() {
                ctx.fillStyle = '#0026ff';
                ctx.fillRect(player.x - player.size/2, player.y - player.size/2, player.size, player.size);
            }

            function checkInPath(x, y) {
                for (let i = 0; i < whitePaths.length; i++) {
                    let p = whitePaths[i];
                    if (x >= p.x && x <= p.x + p.w && y >= p.y && y <= p.y + p.h) {
                        return true;
                    }
                }
                return false;
            }

            canvas.addEventListener('mousemove', (e) => {
                const rect = canvas.getBoundingClientRect();
                const mouseX = e.clientX - rect.left;
                const mouseY = e.clientY - rect.top;

                if (!gameStarted) {
                    if (mouseX >= 50 && mouseX <= 150 && mouseY >= 530 && mouseY <= 580) {
                        gameStarted = true;
                    }
                } else {
                    player.x = mouseX;
                    player.y = mouseY;

                    drawMap();

                    const half = player.size / 2;
                    const p1 = checkInPath(player.x - half, player.y - half);
                    const p2 = checkInPath(player.x + half, player.y - half);
                    const p3 = checkInPath(player.x - half, player.y + half);
                    const p4 = checkInPath(player.x + half, player.y + half);

                    if (!p1 || !p2 || !p3 || !p4) {
                        gameStarted = false; 
                        player = { x: 100, y: 560, size: 8 }; 
                        
                        ctx.fillStyle = 'red';
                        ctx.fillRect(0, 0, canvas.width, canvas.height);
                        setTimeout(() => {
                            drawMap();
                            drawPlayer();
                        }, 100);
                        return;
                    }

                    drawPlayer();

                    if (mouseX >= 380 && mouseX <= 440 && mouseY >= 0 && mouseY <= 60) {
                        triggerJumpscare();
                    }
                }
            });

            function triggerJumpscare() {
                gameStarted = false;
                jumpscareDiv.style.display = 'block'; 
                
                window.parent.postMessage({st_game_status: "WIN"}, "*");
            }

            drawMap();
            drawPlayer();
        </script>
    </body>
    </html>
    """
    
    # 渲染遊戲
    components.html(game_html, height=620, width=820)
   
    receiver_html = """
    <div style="display:none;">
        <button id="streamlit_hidden_trigger">Trigger</button>
    </div>
    <script>
        window.addEventListener('message', function(e) {
            if (e.data && e.data.st_game_status === "WIN") {
                const doc = window.parent.document;
                const buttons = doc.querySelectorAll('button');
                for (let btn of buttons) {
                    if (btn.innerText && btn.innerText.includes("挑戰完才可以按喔，先按的人是小狗")) {
                        btn.click();
                        break;
                    }
                }
            }
        });
    </script>
    """
    components.html(receiver_html, height=0, width=0)

    st.write("---")
    
    if st.button("挑戰完才可以按喔，先按的人是小狗", use_container_width=True):
        st.session_state.game_completed = True
        st.rerun()

    if st.session_state.game_completed:
        if st.button("挑戰完才可以按喔，先按的人是小狗", use_container_width=True):
            st.session_state.stage = "water_test"    # 前往下一關
            st.session_state.game_completed = False  # 重設狀態
            st.rerun()
# ==============================================================================
# 【第三關】「水見式」測驗
# ==============================================================================
elif st.session_state.stage == "water_test":
    st.markdown("<h1 class='hunter-title'>水見式分氣法</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 18px; text-align: center; color: #ffffff;'>雙手靠近水杯，並專注發出你的念能力。<br><b>長按按鈕</b>以注入念氣！</p>",
        unsafe_allow_html=True,
    )
    st.write("---")

    st.set_page_config(layout="wide")
    col1, col2, col3 = st.columns([0.8, 1.6, 1], gap="large")

    with col1:
        st.write("只要努力，誰都可以修習成念")
        st.image(
            "https://i.imgur.com/44mlcYK.jpg",
            caption="集中精神，將氣引導至雙手...",
            use_container_width=True,
        )

    with col3:
            st.write("噴得跟我的頭髮一樣高")
            st.image(
                "https://blog-imgs-43.fc2.com/y/a/r/yaraon/234b855e.jpg",
                caption="老子直接水見式",
                use_container_width=True,
            )

    with col2:
        st.markdown(
            """
            <style>
                div[data-testid="stCheckbox"] {
                    position: absolute !important;
                    width: 0px !important;
                    height: 0px !important;
                    overflow: hidden !important;
                    opacity: 0 !important;
                    pointer-events: none !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        is_completed = st.checkbox("", value=False, key="water_test_bridge")

        if not is_completed:
            water_test_html = """
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background-color: #222; padding: 25px; border-radius: 15px; box-shadow: 0 0 20px rgba(0,0,0,0.5); min-height: 460px;">
                <div id="glass" style="position: relative; width: 150px; height: 200px; border: 5px solid #fff; border-top: none; border-bottom-left-radius: 25px; border-bottom-right-radius: 25px; margin: 10px auto 25px auto; background: rgba(255,255,255,0.1); overflow: visible;">
                    <div id="water" style="position: absolute; bottom: 0; width: 100%; height: 75%; background: rgba(0, 191, 255, 0.4); transition: background 2s, height 2s;"></div>
                    <div id="leaf" style="position: absolute; top: 20%; left: 40%; width: 35px; height: 16px; background: #556B2F; border-radius: 50% 0 50% 0; transform: rotate(-10deg); transition: transform 2s, top 2s, left 2s, opacity 2s;"></div>
                </div>
                
                <button id="charge-btn" style="background: linear-gradient(45deg, #ff4b4b, #ff7676); color: white; border: none; padding: 12px 30px; font-size: 18px; font-weight: bold; border-radius: 30px; cursor: pointer; user-select: none; box-shadow: 0 5px 20px rgba(255,75,75,0.6); outline: none;">
                    注入念能力
                </button>
                
                <p id="status-text" style="color: #ffffff; margin-top: 15px; font-size: 16px; font-weight: bold; text-shadow: 0 0 8px rgba(255,255,255,0.6);">等待念力注入...</p>
                
                <!-- 領取執照按鈕 -->
                <button id="next-stage-btn" style="display: none; width: 100%; margin-top: 20px; background: #fff; color: #111; border: 2px solid #ffcc00; padding: 12px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 15px rgba(255,204,0,0.4);" onclick="navigateToLicense()">
                    挑戰大魔王
                </button>
            </div>

            <canvas id="particle-canvas" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9999;"></canvas>

            <script>
                let holdTimer;
                const btn = document.getElementById('charge-btn');
                const statusText = document.getElementById('status-text');
                const water = document.getElementById('water');
                const leaf = document.getElementById('leaf');
                const canvas = document.getElementById('particle-canvas');
                const nextBtn = document.getElementById('next-stage-btn');
                const ctx = canvas.getContext('2d');
                
                let particles = [];
                let isExploding = false;

                function resizeCanvas() {
                    canvas.width = window.innerWidth;
                    canvas.height = window.innerHeight;
                }
                window.addEventListener('resize', resizeCanvas);
                resizeCanvas();

                class Particle {
                    constructor(x, y, color) {
                        this.x = x;
                        this.y = y;
                        this.size = Math.random() * 6 + 2;
                        this.speedX = (Math.random() - 0.5) * 15;
                        this.speedY = (Math.random() - 0.5) * 15;
                        this.color = color;
                        this.alpha = 1;
                    }
                    update() {
                        this.x += this.speedX;
                        this.y += this.speedY;
                        this.alpha -= 0.015;
                        if (this.size > 0.1) this.size -= 0.05;
                    }
                    draw() {
                        ctx.save();
                        ctx.globalAlpha = this.alpha;
                        ctx.beginPath();
                        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                        ctx.fillStyle = this.color;
                        ctx.shadowBlur = 15;
                        ctx.shadowColor = this.color;
                        ctx.fill();
                        ctx.restore();
                    }
                }

                function animateParticles() {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    for (let i = 0; i < particles.length; i++) {
                        particles[i].update();
                        particles[i].draw();
                        if (particles[i].alpha <= 0) {
                            particles.splice(i, 1);
                            i--;
                        }
                    }
                    if (isExploding || particles.length > 0) {
                        requestAnimationFrame(animateParticles);
                    }
                }

                function triggerGlow() {
                    isExploding = true;
                    const rect = document.getElementById('glass').getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    
                    const nenTypes = [
                        { name: '強化系', color: '#FFD700', action: () => { water.style.height = '90%'; } },
                        { name: '變化系', color: '#FF69B4', action: () => { water.style.background = 'rgba(255, 105, 180, 0.7)'; } },
                        { name: '放出系', color: '#00FFFF', action: () => { water.style.background = 'rgba(0, 255, 255, 0.7)'; } },
                        { name: '具現化系', color: '#7CFC00', action: () => { water.style.background = 'rgba(124, 252, 0, 0.4)'; water.innerHTML = '<div style="position:absolute;top:20%;width:100%;text-align:center;color:#fff;font-size:12px;">厲害哦~~</div>'; } },
                        { name: '操作系', color: '#1E90FF', action: () => { leaf.style.transform = 'rotate(180deg) scale(1.3)'; leaf.style.left = '10%'; } },
                        { name: '特質系', color: '#E066FF', action: () => { water.style.background = 'rgba(224, 102, 255, 0.8)'; leaf.style.opacity = '0.3'; } }
                    ];
                    
                    const result = nenTypes[Math.floor(Math.random() * nenTypes.length)];
                    result.action();

                    for (let i = 0; i < 150; i++) {
                        particles.push(new Particle(centerX, centerY, result.color));
                    }
                    animateParticles();
                    
                    statusText.innerHTML = `<b style="color:${result.color}; font-size: 22px; text-shadow: 0 0 15px ${result.color};">覺醒成功：【${result.name}】！</b>`;
                    nextBtn.style.display = 'block';
                }

                function navigateToLicense() {
                    const streamlitInputs = window.parent.document.querySelectorAll('input[type="checkbox"]');
                    for (let input of streamlitInputs) {
                        if (!input.checked) {
                            input.click(); 
                            break;
                        }
                    }
                }

                btn.addEventListener('mousedown', startHold);
                btn.addEventListener('touchstart', startHold);

                function startHold(e) {
                    e.preventDefault();
                    btn.style.transform = 'scale(0.95)';
                    statusText.innerHTML = "念力注入中...";
                    holdTimer = setTimeout(() => {
                        btn.style.display = 'none';
                        triggerGlow();
                    }, 2000);
                }
            </script>
            """
            import streamlit.components.v1 as components
            components.html(water_test_html, height=520)
        
        else:
            st.session_state.stage = "test2_game"
            st.rerun()

# ==============================================================================
# 【第四關】「戰鬥」測驗
# ==============================================================================
elif st.session_state.stage == "test2_game":
    if "gon_hp" not in st.session_state:
        st.session_state.gon_hp = 50
        st.session_state.birthday_boy_hp = 1
        st.session_state.killua_hp = 45
        st.session_state.hisoka_hp = 150
        st.session_state.current_turn = 1
        st.session_state.log_message = " 西索 擋住了去路！<br>小傑、奇犽與路過的你準備迎戰！"
        st.session_state.game_over = False


    def reset_battle():
        st.session_state.gon_hp = 50
        st.session_state.birthday_boy_hp = 1
        st.session_state.killua_hp = 45
        st.session_state.hisoka_hp = 150
        st.session_state.current_turn = 1
        st.session_state.log_message = "戰鬥重新開始！西索 再次擋住了去路！"
        st.session_state.game_over = False

    # ----------------- 畫面渲染 -----------------
    st.markdown(
        f"""
        <div style='text-align: left; margin-bottom: 6px;'>
            <span style='background-color: #1a252c; border: 1.5px solid #f3e5ab; padding: 3px 8px; border-radius: 3px; color: #f3e5ab; font-family: monospace; font-weight: bold; font-size: 13px; letter-spacing: 0.5px;'>⏳ {st.session_state.current_turn} TURN</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # 2. 戰鬥訊息框
    st.markdown(
        f"""
        <div style='background-color: #1a252c; border: 2px solid #f3e5ab; border-radius: 5px; padding: 12px 15px; color: #ffffff; font-family: monospace; font-size: 15px; font-weight: bold; line-height: 1.5; box-shadow: 0px 3px 10px rgba(0,0,0,0.4); width: 100%;'>
            {st.session_state.log_message}
        </div>
        """, 
        unsafe_allow_html=True
    )

    # 西索照片與血量條
    st.write("")
    col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
    with col_m2:
        if st.session_state.hisoka_hp > 0:
            st.progress(st.session_state.hisoka_hp / 150, text=f"西索 HP: {st.session_state.hisoka_hp} / 150")
            st.markdown("<h3 style='text-align:center; color:#ffb703; margin:10px 0;'> 西索 </h3>", unsafe_allow_html=True)
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSroX247tp4bqOS-L-jSLkcngpCvxs0UANA0JRvs2OtUOrqR3aCTrNHyOs&s=10", width=350)
        else:
            st.markdown("<h2 style='text-align:center; color:gray; margin:30px 0;'> 西索已陣亡</h2>", unsafe_allow_html=True)
    st.write("")

    # 處理回合戰鬥邏輯
    player_action = None

    # 指令與隊伍狀態
    st.markdown("---")
    s_col1, s_col2, s_col3 = st.columns(3)

    with s_col1:
        if not st.session_state.game_over and st.session_state.gon_hp > 0:
            if st.button("剪刀石頭布", key="gon_btn", use_container_width=True):
                player_action = "gon_skill"
        else:
            st.button("無法行動", key="gon_btn_dis", disabled=True, use_container_width=True)
            
        st.markdown(f"""
            <div class='status-grid'>
                <div class='status-name'>小傑</div>
                <div class='status-value'>HP <b>{st.session_state.gon_hp}</b> / 50</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.image("https://truth.bahamut.com.tw/s01/201810/81b61c4e067cde0ecda69336140a890b.JPG", use_container_width=True)

    with s_col2:
        if not st.session_state.game_over and st.session_state.birthday_boy_hp > 0:
            if st.button("嘴砲攻擊", key="birthday_btn", use_container_width=True):
                player_action = "birthday_skill"
        else:
            st.button("無法行動", key="birthday_btn_dis", disabled=True, use_container_width=True)
            
        st.markdown(f"""
            <div class='status-grid'>
                <div class='status-name'> 你 </div>
                <div class='status-value'>HP <b>{st.session_state.birthday_boy_hp}</b> / 1</div>
            </div>
        """, unsafe_allow_html=True)
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlvvpgqtB7AcNLcaQQ8kW-gapN7q_FhBQdiH886jnxao7hpIYH-_ghHmQ&s=10", use_container_width=True)

    with s_col3:
        if not st.session_state.game_over and st.session_state.killua_hp > 0:
            if st.button("溜溜球", key="killua_btn", use_container_width=True):
                player_action = "killua_skill"
        else:
            st.button("無法行動", key="killua_btn_dis", disabled=True, use_container_width=True)
            
        st.markdown(f"""
            <div class='status-grid'>
                <div class='status-name'>奇犽</div>
                <div class='status-value'>HP <b>{st.session_state.killua_hp}</b> / 45</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTaEaAqlyXd16CDjRbWp0VjXuff77pCtc3RirlloJ1NdPw9TKQgFgjpzrU&s=10", use_container_width=True)

    # 處理戰鬥運算
    if player_action:
        msg = ""
        
        # 玩家攻擊
        if player_action == "gon_skill":
            if random.random() < 0.7:
                dmg = random.randint(35, 50)
                st.session_state.hisoka_hp -= dmg
                msg = f"小傑 使出了 <b>剪刀石頭布！</b><br> 暴擊！對西索造成了 {dmg} 點傷害！"
            else:
                msg = "小傑 使出了 剪刀石頭布！<br> 被西索靈巧地閃過了！"
                
        elif player_action == "birthday_skill":
            roasts = [
                "「自以為是娃娃臉攻擊！」",
                "「整天站起來長痔瘡是不是！」",
                "「好多事情好煩喔，你給我閉嘴！」",
                "「甩鍋甩起來，誰都別煩我！」"
            ]
            chosen_roast = random.choice(roasts)
            dmg = random.randint(25, 45) 
            st.session_state.hisoka_hp -= dmg
            msg = f"壽星 發動了 <b>嘴砲攻擊</b>！<br>🗣️ {chosen_roast}<br> 西索被嘴砲到開始懷疑人生，損失了 {dmg} 點 HP！"
            
        elif player_action == "killua_skill":
            dmg = random.randint(20, 35)
            st.session_state.hisoka_hp -= dmg
            msg = f"奇犽 化為閃電！使出了 <b>溜溜球！</b><br> 擊中！對西索造成了 {dmg} 點傷害！"

        # 西索是否陣亡
        if st.session_state.hisoka_hp <= 0:
            st.session_state.hisoka_hp = 0
            st.session_state.game_over = True
            st.session_state.log_message = msg + "<br> 西索倒下了！你們獲得了天空競技場的勝利！"
            st.rerun()

        # 西索反擊
        alive_targets = []
        if st.session_state.gon_hp > 0: alive_targets.append("gon")
        if st.session_state.birthday_boy_hp > 0: alive_targets.append("birthday")
        if st.session_state.killua_hp > 0: alive_targets.append("killua")
        
        if alive_targets:
            target = random.choice(alive_targets)
            e_dmg = random.randint(15, 30)
            
            if target == "gon":
                st.session_state.gon_hp -= e_dmg
                msg += f"<br>西索 使用 <b>伸縮自如的愛</b> 反擊！<br> 小傑受到了 {e_dmg} 點傷害！"
            elif target == "birthday":
                st.session_state.birthday_boy_hp -= e_dmg
                msg += f"<br>西索 被嘴到受不了！直接對你丟出 <b>一把刀子</b>！<br> 壽星只有 1 HP 慘遭秒殺，受到了 {e_dmg} 點傷害！"
            else:
                st.session_state.killua_hp -= e_dmg
                msg += f"<br>西索 飛快擲出 <b>銳利撲克牌</b> 反擊！<br> 奇犽受到了 {e_dmg} 點傷害！"

        # 血量下限
        if st.session_state.gon_hp <= 0: st.session_state.gon_hp = 0
        if st.session_state.birthday_boy_hp <= 0: st.session_state.birthday_boy_hp = 0
        if st.session_state.killua_hp <= 0: st.session_state.killua_hp = 0

        # 所有人全滅
        if st.session_state.gon_hp == 0 and st.session_state.birthday_boy_hp == 0 and st.session_state.killua_hp == 0:
            st.session_state.game_over = True
            msg += "<br> 全員都倒下了... 有夠菜，這樣還贏不了。"

        st.session_state.log_message = msg
        st.session_state.current_turn += 1
        st.rerun()

    # 結算
    if st.session_state.game_over:
        st.write("")
        
        # 情況 A：成功打贏西索
        if st.session_state.hisoka_hp == 0:
            if st.button("領取獵人執照", use_container_width=True):
                # 清理本關卡的暫存變數
                del st.session_state.gon_hp
                del st.session_state.birthday_boy_hp
                del st.session_state.killua_hp
                del st.session_state.hisoka_hp
                st.session_state.stage = "license"  # 切換至下一關
                st.rerun()
                
        # 情況 B：玩家全員陣亡打輸了
        else:
            if st.button("我太爛了哭，只能再戰一次", use_container_width=True):
                reset_battle()
                st.rerun()

# ==============================================================================
# 【第五關】解鎖獵人執照 與 祝福煙火
# ==============================================================================
elif st.session_state.stage == "license":
    # 建立一個動態容器
    top_container = st.empty()
    
    if "registered_name" not in st.session_state:
        st.session_state.registered_name = ""

    if not st.session_state.registered_name:
        with top_container.container():
            st.markdown("<h1 class='hunter-title'>恭喜恭喜！這是你應得的！</h1>", unsafe_allow_html=True)
            
            birthday_name = st.text_input(" 登記姓名：", placeholder="", key="name_input")
            
            gif_url = "https://i.imgur.com/JyRtBuI.gif" 
            st.markdown(
                f"""
                <div style="text-align: center; margin-top: 25px;">
                    <img src="{gif_url}" style="width: 650px; max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5);">
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if birthday_name:
                st.session_state.registered_name = birthday_name
                st.rerun() 

    
    if st.session_state.registered_name:
        top_container.empty()
        current_user_name = st.session_state.registered_name   
        
        # 顯示卡片頁面的標題
        st.markdown(f"<h1 class='hunter-title'>恭喜 {st.session_state.registered_name}！</h1>", unsafe_allow_html=True)
        st.info("這可是一年一次的生日，當然要開開心心 :)")
        
        license_and_birthday_html = f"""
        <div style="text-align: center; color: white; font-family: sans-serif;">
            
            <!-- ====== 第三關：獵人執照卡面視覺 (純 CSS 刻劃版) ====== -->
            <div id="hunter-card" style="width: 320px; height: 480px; background-color: #fff; border: 12px solid #fff; border-radius: 20px; margin: 20px auto; box-shadow: 0 10px 25px rgba(0,0,0,0.6); position: relative; box-sizing: border-box; overflow: hidden; display: flex; flex-direction: column;">
                
                <!-- 內部黑色邊框線 -->
                <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; border: 2px solid #000; border-radius: 8px; pointer-events: none; z-index: 10;"></div>
                
                <!-- 上半部：黑底與獵人標誌 -->
                <div style="background-color: #000; flex: 1.1; position: relative; display: flex; align-items: center; justify-content: center;">
                    <!-- 獵人標誌外圍白框 -->
                    <div style="width: 190px; height: 110px; background-color: #fff; border: 3px solid #000; display: flex; align-items: center; justify-content: center; position: relative;">
                        <!-- 兩個大 X 裝飾線 -->
                        <div style="position: absolute; width: 100%; height: 100%; background: 
                            linear-gradient(45deg, transparent 44%, #000 44%, #000 48%, transparent 48%),
                            linear-gradient(-45deg, transparent 44%, #000 44%, #000 48%, transparent 48%),
                            linear-gradient(45deg, transparent 52%, #000 52%, #000 56%, transparent 56%),
                            linear-gradient(-45deg, transparent 52%, #000 52%, #000 56%, transparent 56%);">
                        </div>
                        <!-- 中央紅色菱形 -->
                        <div style="width: 45px; height: 45px; background-color: #d11a2a; transform: rotate(45deg); z-index: 2;"></div>
                        <!-- 覆蓋上下橫條 -->
                        <div style="position: absolute; top: 12px; width: 150px; height: 6px; background-color: #000; z-index: 3;"></div>
                        <div style="position: absolute; bottom: 12px; width: 150px; height: 6px; background-color: #000; z-index: 3;"></div>
                    </div>
                </div>
                
                <!-- 中間層：模擬真實條碼 -->
                <div style="height: 55px; background: repeating-linear-gradient(90deg, #000, #000 2px, #fff 2px, #fff 4px, #000 4px, #000 5px, #fff 5px, #fff 8px); border-top: 4px solid #000; border-bottom: 4px solid #000; box-sizing: border-box;"></div>
                
                <!-- 下半部：水藍色資訊區 -->
                <div style="background-color: #a4d4f4; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding-top: 15px; position: relative;">
                    
                    <!-- 替換原本獵人文字的【壽星名字專屬框】 -->
                    <div style="width: 250px; height: 42px; background-color: #e2e8f0; border: 3px solid #1a2a3a; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);">
                        <div style="font-size: 18px; font-weight: bold; color: #111; font-family: 'Courier New', monospace; letter-spacing: 1px;" id="card-name">
                            {current_user_name}
                        </div>
                    </div>
                    
                    <!-- 底部裝飾三星與小文字 -->
                    <div style="font-size: 16px; margin-top: 12px; color: #1a2a3a; letter-spacing: 3px;">好 快 樂 喔</div>
                    <div style="font-size: 16px; margin-top: 12px; color: #1a2a3a; letter-spacing: 3px;">努 力 的 過 好 每 天</div>
                    
                    <!-- 最底部版權與暗號小字 -->
                    <div style="position: absolute; bottom: 8px; width: 100%; display: flex; justify-content: space-between; padding: 0 15px; box-sizing: border-box; font-size: 8px; color: #335577; font-family: monospace;">
                        <span>©P98-24 ©V·N·M</span>
                        <span>No.287-SECRET</span>
                    </div>
                </div>
            </div>

            <!-- ====== 刷卡滑桿元件 ====== -->
            <div style="width: 320px; margin: 20px auto; position: relative; background: #333; height: 50px; border-radius: 25px; overflow: hidden; border: 2px solid #555;">
                <div id="slider-bar" style="position: absolute; left: 0; top: 0; height: 100%; width: 50px; background: linear-gradient(90deg, #ffcc00, #ff6600); z-index: 1; transition: width 0.1s ease-out;"></div>
                <div style="position: absolute; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: #aaa; z-index: 2; font-size: 14px; pointer-events: none;">
                    ▶▶ 向右滑動磁條刷卡 ▶▶
                </div>
                <input id="swipe-slider" type="range" min="0" max="100" value="0" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; opacity: 0; cursor: pointer; z-index: 3;">
            </div>

            <!-- ====== 最後收尾：滿版煙火與全螢幕祝賀彈窗 ====== -->
            <div id="birthday-overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 9999; flex-direction: column; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box;">
                <canvas id="fireworks-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;"></canvas>
                
                <div style="position: relative; z-index: 10000; background: rgba(20, 20, 20, 0.9); border: 3px solid #ffcc00; padding: 30px; border-radius: 15px; max-width: 500px; text-align: left; box-shadow: 0 0 30px rgba(255,204,0,0.5);">
                    <h2 style="color: #ffcc00; text-align: center; margin-top: 0;"> 生日快快快樂，{current_user_name} </h2>
                    <p style="color: #fff; text-align: center; font-size: 14px; margin-bottom: 20px;">恭喜正式成為 287 期獵人！</p>
                    
                    <div style="margin-bottom: 15px; border-left: 4px solid #ffcc00; padding-left: 10px;">
                        <b style="color: #ffcc00;"> 小傑：</b>
                        <p style="margin: 5px 0 0 0; color: #ddd; font-size: 14px; line-height: 1.4;">「太棒了！以後我們就可以一起去世界各地冒險了！生日快樂！」</p>
                    </div>
                    
                    <div style="margin-bottom: 25px; border-left: 4px solid #ffcc00; padding-left: 10px;">
                        <b style="color: #ffcc00;"> 奇犽：</b>
                        <p style="margin: 5px 0 0 0; color: #ddd; font-size: 14px; line-height: 1.4;">「哼，能通過試驗算你厲害！你可別高興得太早，真正的冒險才剛開始呢！」</p>
                    </div>

                    <div style="margin-bottom: 25px; border-left: 4px solid #ffcc00; padding-left: 10px;">
                        <b style="color: #ffcc00;"> 作者：</b>
                        <p style="margin: 5px 0 0 0; color: #ddd; font-size: 14px; line-height: 1.4;">「這可是花費我每天1~2小時的嘔心瀝血之作，祝你生日快樂ㄚㄚㄚㄚ！」</p>
                    </div>
                    
                   <button onclick="document.getElementById('birthday-overlay').style.display='none'; document.getElementById('next-stage-view').style.display='flex';" style="display: block; width: 100%; padding: 10px; background: #ffcc00; border: none; color: black; font-weight: bold; border-radius: 5px; cursor: pointer; font-size: 14px;">關閉祝福</button>
                </div>
            </div>
        </div>

        <!-- ====== 下一個畫面（按鈕）與滿版照片的 HTML 結構 ====== -->
        <!-- 下一個畫面：包含一個居中按鈕 -->
        <div id="next-stage-view" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #222; justify-content: center; align-items: center; z-index: 99998;">
            <!-- 點擊後隱藏自己，顯示照片 -->
            <button onclick="document.getElementById('next-stage-view').style.display='none'; document.getElementById('full-image-view').style.display='flex';" style="padding: 15px 30px; background: #00ffcc; border: none; color: black; font-weight: bold; border-radius: 30px; cursor: pointer; font-size: 18px; box-shadow: 0 4px 15px rgba(0,255,204,0.4);">
                查看驚喜
            </button>
        </div>

        <!-- 滿版照片畫面：初始隱藏，z-index 設為最高確保不被任何元件擋住 -->
        <div id="full-image-view" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #000; z-index: 99999; justify-content: center; align-items: center;">
            <!-- 請將下面的 src 網址替換成您的照片網址 -->
            <img src="https://i.pinimg.com/736x/5f/33/a3/5f33a33e94ba696fb0f7aed7b79007e6.jpg" alt="Surprise" style="width: 100%; height: 100%; object-fit: contain;">
        
        </div>

        <!-- ====== 前端控制腳本 ====== -->
<script>
    const slider = document.getElementById('swipe-slider');
    const sliderBar = document.getElementById('slider-bar');
    const overlay = document.getElementById('birthday-overlay');
    const fCanvas = document.getElementById('fireworks-canvas');
    const fCtx = fCanvas.getContext('2d');
    
    let fireworks = [];
    let particles = [];
    let animationId = null;

    // 調整畫布大小
    function resizeCanvas() {{
        fCanvas.width = window.innerWidth;
        fCanvas.height = window.innerHeight;
    }}
    window.addEventListener('resize', resizeCanvas);

    // 監聽刷卡滑桿動作
    slider.addEventListener('input', (e) => {{
        let val = e.target.value;
        sliderBar.style.width = `calc(${{val}}% + 50px)`;
        
        if (val >= 95) {{
            slider.value = 100;
            sliderBar.style.width = '100%';
            slider.disabled = true; // 鎖定滑桿防止重複觸發
            
            // 名稱：與下方的煙火控制引擎對齊
            triggerFireworks();
        }}
    }});

    // 煙火特效控制引擎
    let fwParticles = [];
    function resizeFCanvas() {{
        fCanvas.width = window.innerWidth;
        fCanvas.height = window.innerHeight;
    }}
    window.addEventListener('resize', resizeFCanvas);

    function triggerFireworks() {{
        overlay.style.display = 'flex';
        resizeFCanvas();
        setupFireworksLoop();
    }}

    class FWParticle {{
        constructor(x, y, color) {{
            this.x = x;
            this.y = y;
            this.color = color;
            this.radius = Math.random() * 3 + 1;
            this.velocity = {{
                x: (Math.random() - 0.5) * 8,
                y: (Math.random() - 0.5) * 8
            }};
            this.alpha = 1;
        }}
        draw() {{
            fCtx.save();
            fCtx.globalAlpha = this.alpha;
            fCtx.beginPath();
            fCtx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            fCtx.fillStyle = this.color;
            fCtx.fill();
            fCtx.restore();
        }}
        update() {{
            this.x += this.velocity.x;
            this.y += this.velocity.y;
            this.velocity.y += 0.05; // 模擬下墜
            this.alpha -= 0.01;
        }}
    }}

    function spawnFirework() {{
        const x = Math.random() * fCanvas.width;
        const y = Math.random() * (fCanvas.height * 0.6);
        const colors = ['#ff0055', '#00ffcc', '#ffcc00', '#ff6600', '#cc00ff'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        for (let i = 0; i < 40; i++) {{
            fwParticles.push(new FWParticle(x, y, color));
        }}
    }}

    let frameCount = 0;
    function setupFireworksLoop() {{
        fCtx.fillStyle = 'rgba(0, 0, 0, 0.15)';
        fCtx.fillRect(0, 0, fCanvas.width, fCanvas.height);
        if (frameCount % 25 === 0) spawnFirework();
        frameCount++;
        for (let i = 0; i < fwParticles.length; i++) {{
            fwParticles[i].update();
            fwParticles[i].draw();
            if (fwParticles[i].alpha <= 0) {{
                fwParticles.splice(i, 1);
                i--;
            }}
        }}
        if(overlay.style.display === 'flex') {{
            requestAnimationFrame(setupFireworksLoop);
        }}
    }}
</script>
        """   
        # 渲染 HTML 元件
        st.components.v1.html(license_and_birthday_html, height=600, scrolling=False)

