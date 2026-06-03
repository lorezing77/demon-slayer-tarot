import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 🎯 22張大阿爾克那牌數據（用於四種主牌陣）
MAJOR_DECK = {
    0: {"name": "0. 愚者 · 嘴平伊之助", "img": "0.愚者-嘴平伊之助.jpg", "up": "衝動、自由奔放、不畏艱難、直覺行動", "down": "魯莽、不聽勸阻、缺乏策略、流於表面"},
    1: {"name": "1. 魔術師 · 我妻善逸", "img": "1.魔術師-我妻善逸.jpg", "up": "潛能爆發、專注的力量、神速創造奇蹟", "down": "缺乏自信、逃避現實、精神不集中"},
    2: {"name": "2. 女祭司 · 灶門禰豆子", "img": "2.女祭司-灶門禰豆子.jpg", "up": "潛意識的力量、溫柔的守護、內在沉靜", "down": "情緒失控、難以溝通、壓抑自我"},
    3: {"name": "3. 皇后 · 戀柱·甘露寺蜜璃", "img": "3.皇后-戀柱-甘露寺蜜璃.jpg", "up": "愛心滿溢、美麗、熱情、豐收與包容", "down": "過度依賴、情感氾濫、缺乏安全感"},
    4: {"name": "4. 皇帝 · 黑死牟", "img": "4.皇帝-黑死牟.jpg", "up": "威嚴、絕對的力量、秩序、追求極致的統治力", "down": "冷酷無情、執念過深、嫉妒與毀滅"},
    5: {"name": "5. 教皇 · 岩柱·悲鳴嶼行冥", "img": "5.教皇-岩柱-悲鳴嶼行冥.jpg", "up": "精神支柱、慈悲為懷、引導者、堅定信仰", "down": "悲觀固執、流於說教、內心沉重"},
    6: {"name": "6. 戀人 · 墮姬 & 妓夫太郎", "img": "6.戀人-墮姬 & 妓夫太郎.jpg", "up": "強烈的羈絆、共生共存、情感危機", "down": "病態的執著、互相毀滅、命運的悲劇"},
    7: {"name": "7. 戰車 · 音柱·宇髓天元", "img": "7.戰車-音柱-宇髓天元.jpg", "up": "華麗的勝利、意志力、高歌猛進、衝破阻礙", "down": "遭遇挫折、失去方向、行事過頭"},
    8: {"name": "8. 力量 · 炎柱·煉獄杏壽郎", "img": "8.力量-炎柱-煉獄杏壽郎.jpg", "up": "百折不撓的勇氣、照亮他人的意志、精神內核強大", "down": "力不從心、過度燃燒自己、遺憾"},
    9: {"name": "9. 隱士 · 蛇柱·伊黑小芭內", "img": "9.隱士-蛇柱-伊黑小芭內.jpg", "up": "內斂深沉、默默守護、獨樹一幟的敏銳", "down": "孤立自己、難以釋懷、言語刻薄"},
    10: {"name": "10. 命運之輪 · 產屋敷耀哉", "img": "10.命運之輪-產屋敷耀哉.jpg", "up": "掌握因果局勢、轉折點、宿命的宏觀指引", "down": "身體惡化、命運無常、被迫承受災難"},
    11: {"name": "11. 正義 · 水柱·富岡義勇", "img": "11.正義-水柱-富岡義勇.jpg", "up": "冷靜克制、恪守原則、公平裁決", "down": "自我懷疑、內心失衡、情感封閉"},
    12: {"name": "12. 倒吊人 · 猗窩座", "img": "12.倒吊人-猗窩座猗窩座.jpg", "up": "執著的追求、換個角度追求至高境界、淬煉", "down": "走入死胡同、盲目的犧牲、迷失真我"},
    13: {"name": "13. 死神 · 獪岳", "img": "13.死神-獪岳.jpg", "up": "決絕的徹底改變、陣營的轉換、終結過去", "down": "抗拒滅亡、走入窮途末路、墜入深淵"},
    14: {"name": "14. 節制 · 蟲柱·胡蝶忍", "img": "14.節制-蟲柱-胡蝶忍.jpg", "up": "藥理的調配與融合、克制外表下的平和、巧妙平衡", "down": "內心失衡、積壓憤怒、過度壓抑自我"},
    15: {"name": "15. 惡魔 · 鬼舞辻無慘", "img": "15.惡魔-鬼舞辻無慘.jpg", "up": "絕對的支配欲、物質永生的貪婪、強烈的控制", "down": "恐懼爆發、氣數已盡、被宿怨束縛"},
    16: {"name": "16. 高塔 · 風柱·不死川實彌", "img": "16.高塔-風柱-不死川實彌.jpg", "up": "暴風雨般的破壞力、巨變、打破現狀的憤怒", "down": "危機重重、情緒失控、傷痕累累"},
    17: {"name": "17. 星星 · 霞柱·時透無一郎", "img": "17.星星-霞柱-時透無一郎.jpg", "up": "重獲記憶後的澄澈希望、天才的光芒、寧靜", "down": "迷茫失落、失去焦點、流星般短暫"},
    18: {"name": "18. 月亮 · 童磨", "img": "18.月亮-童磨.jpg", "up": "虛幻的極樂、隱藏的危機、難以捉摸的虛無", "down": "謊言被揭穿、恐懼驅散、真相大白"},
    19: {"name": "19. 太陽 · 灶門炭治郎", "img": "19.太陽-灶門炭治郎.jpg", "up": "日之呼吸的光輝、無盡的活力、溫慢人心、大獲成功", "down": "精疲力竭、光芒被遮蔽、暫時的挫敗"},
    20: {"name": "20. 審判 · 繼國緣壹", "img": "20.審判-繼國緣壹.jpg", "up": "神級覺醒、歷史的抉擇、天命的救贖與昭雪", "down": "留下遺憾、錯失關鍵、歷史的沉重"},
    21: {"name": "21. 世界 · 青色彼岸花", "img": "21.世界-青色彼岸花.jpg", "up": "終極的追求、完美的終點、旅程的圓滿達成", "down": "可望不可即、未完成的執念、停滯不前"}
}

# 🎯 56張小阿爾克那牌數據庫
MINOR_SUITS = {
    "權杖": {"elem": "火象元素（行動、熱情與意志力）", "up_base": "具體行動的時機成熟，應以果斷決策打破僵局", "down_base": "面臨動力燃盡、方向失控或無謂的權力內耗"},
    "聖杯": {"elem": "水象元素（情感、直覺與心理狀態）", "up_base": "內心能量達成和解，請依循直覺進行人際情感修復", "down_base": "陷入情緒氾濫的漩渦，需提防感性盲點或過度期待引起的失落"},
    "寶劍": {"elem": "風象元素（理智、思考與言詞衝突）", "up_base": "理性思維正在劈開迷霧，此時需要冷酷、客觀地切割混亂", "down_base": "精神壓力過載，思緒陷入作繭自縛的死胡同"},
    "錢幣": {"elem": "土象元素（物質、現實與穩定根基）", "up_base": "現實條件穩步落地，專注於資源、財務與具體成果的累積", "down_base": "面臨現實資源卡關、缺乏遠見、或腳步過度保守停滯"}
}
NUM_NAMES = {1: "Ace", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九", 10: "十", 11: "侍從", 12: "騎士", 13: "王后", 14: "國王"}

MINOR_DECK = []
for suit, info in MINOR_SUITS.items():
    for num, num_str in NUM_NAMES.items():
        MINOR_DECK.append({
            "name": f"{suit}{num_str}",
            "file_name": f"{suit}{num_str}.jpg", # 🌟 生成對應的圖片名稱
            "elem": info["elem"],
            "up": info["up_base"],
            "down": info["down_base"]
        })

@app.route('/')
def index():
    return render_template('index.html', result=None, mode=None)

@app.route('/divine')
def divine():
    mode = request.args.get('mode', 'mode3')
    
    if mode == 'mode1':
        positions, count, title = ["今日運勢 (Daily)"], 1, "每日運氣占卜"
    elif mode == 'mode2':
        positions, count, title = ["選項 A 的優缺點 (Option A)", "選項 B 的優缺點 (Option B)"], 2, "選擇題評估占卜"
    elif mode == 'mode3':
        positions, count, title = ["過去 (Past)", "現在 (Present)", "未來 (Future)"], 3, "聖三角時空占卜"
    elif mode == 'mode4':
        positions = ["1. 現狀核心", "2. 面臨障礙", "3. 潛意識根源", "4. 過去影響", "5. 目標心願", "6. 近期未來", "7. 自我狀態", "8. 周遭環境", "9. 希望與恐懼", "10. 最終結果"]
        count, title = 10, "凱爾特十字大牌陣占卜"
    else:
        return render_template('index.html', result=None, mode=None)

    card_ids = random.sample(list(MAJOR_DECK.keys()), count)
    drawn_cards = []
    for i, cid in enumerate(card_ids):
        card_info = MAJOR_DECK[cid]
        orientation = random.choice(["正位", "逆位"])
        meaning = card_info["up"] if orientation == "正位" else card_info["down"]
        
        drawn_cards.append({
            "position": positions[i],
            "name": card_info["name"],
            "img": card_info["img"],
            "orientation": orientation,
            "meaning": meaning
        })
        
    return render_template('index.html', result=drawn_cards, mode=mode, title=title)

@app.route('/extend_query', methods=['POST'])
def extend_query():
    data = request.json
    query_type = data.get('type')
    
    minor_card = random.choice(MINOR_DECK)
    minor_orientation = random.choice(["正位", "逆位"])
    minor_meaning = minor_card["up"] if minor_orientation == "正位" else minor_card["down"]
    
    card_msg = f"【{minor_card['name']} &bull; {minor_orientation}】"

    if query_type == "q1":
        title = "💡 盲點解密：我目前忽略了什麼？"
        reply = f"大師為你加抽小阿爾克那牌 {card_msg}。映射出你目前的盲點正處於{minor_card['elem']}的範疇。具體而言：{minor_meaning}。主牌陣宏觀大牌指引的方向雖然明確，但你往往卡在這些現實元素的細微失衡中而不自知，請對照小牌指示的狀態即刻校正身心。"
    elif query_type == "q2":
        title = "⚡ 關鍵轉折：局勢何時會好轉？"
        reply = f"大師為你加抽小阿爾克那牌 {card_msg}。從元素時序推演：{minor_card['elem']}所對應的能量區間顯示，{minor_meaning}。大牌定調的靈魂課題正在發酵，而轉折點的成熟度與這張小牌息息相關，請密切留意小牌所隱喻的事件發展節奏。"
    elif query_type == "q3":
        title = "🔥 核心建議：當前最應該做出的關鍵行動？"
        reply = f"大師為你加抽小阿爾克那牌 {card_msg}。給予你最直接的現實切入方針：{minor_meaning}。請將此行動方案作為破除主牌陣中困局的『現實槓桿』，藉由落實{minor_card['elem']}的正面能量，強行推動卡關的宿命輪盤。"
    elif query_type == "q4":
        title = "🛡️ 命運防線：如果結果不盡理想，該如何避凶？"
        reply = f"大師為你加抽小阿爾克那牌 {card_msg}。為你構築的現實盾牌：{minor_meaning}。小牌展現了當前最容易破防的現實缺口（{minor_card['elem']}）。只要防範小牌所預警的負面狀態，你就能安全地將主牌陣中可能遭遇的衝擊降至最低。"
    else:
        title, reply = "神祕的指引", "請重新點擊詢問。"

    return jsonify({
        "title": title, 
        "reply": reply,
        "minor_img": minor_card["file_name"] # 🌟 同步將小牌圖片名稱送回前端
    })

if __name__ == '__main__':
# 部署時 debug 要設為 False，port 要由環境變數決定
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
