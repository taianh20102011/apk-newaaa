# main.py
import json
import os
import random
from datetime import datetime

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import DictProperty, StringProperty, BooleanProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp

# ---------------- KV (giao diện) ----------------
KV = r'''
#:import dp kivy.metrics.dp

ScreenManager:
    MainMenuScreen:
    ScenarioListScreen:
    ScenarioScreen:
    ResultScreen:
    KnowledgeScreen:
    HistoryScreen:
    ProfileScreen:

<MainMenuScreen>:
    name: "menu"
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "⚡ Cảnh báo tình huống"
            elevation: 6

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(16)

            MDCard:
                radius: [14,]
                padding: dp(14)
                md_bg_color: app.theme_cls.primary_light
                elevation: 8
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Ứng dụng mô phỏng tình huống an toàn"
                    font_style: "H6"
                    halign: "left"

                MDLabel:
                    text: "Học sinh THCS — phân biệt an toàn / nguy hiểm"
                    font_style: "Caption"
                    halign: "left"

            MDRaisedButton:
                text: "🚀 Bắt đầu mô phỏng"
                size_hint_y: None
                height: dp(48)
                on_release: app.root.current = "scenario_list"

            MDRaisedButton:
                text: "📘 Kho kiến thức"
                size_hint_y: None
                height: dp(48)
                on_release: app.root.current = "knowledge"

            MDRaisedButton:
                text: "📊 Lịch sử / Báo cáo"
                size_hint_y: None
                height: dp(48)
                on_release: app.root.current = "history"

            MDRaisedButton:
                text: "👤 Hồ sơ"
                size_hint_y: None
                height: dp(48)
                on_release: app.root.current = "profile"

        MDLabel:
            text: "© 2025 - Nhóm học sinh THCS Lý Tự Trọng | Fanpage: Lý Tự Trọng Gò Vấp"
            halign: "center"
            font_style: "Caption"
            size_hint_y: None
            height: dp(28)


<ScenarioListScreen>:
    name: "scenario_list"
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "📋 Danh sách tình huống"
            left_action_items: [["arrow-left", lambda x: app.go_back("menu")]]
            elevation: 6

        ScrollView:
            MDList:
                id: list_container
                padding: dp(8)

        MDBoxLayout:
            size_hint_y: None
            height: dp(64)
            padding: dp(12)
            MDRaisedButton:
                text: "🔀 Random thử"
                pos_hint: {"center_x": 0.5}
                on_release: root.open_random()

        MDLabel:
            text: "© 2025 - Nhóm học sinh THCS Lý Tự Trọng | Fanpage: Lý Tự Trọng Gò Vấp"
            halign: "center"
            font_style: "Caption"
            size_hint_y: None
            height: dp(28)


<ScenarioScreen>:
    name: "scenario"
    scenario: {}
    current_index: -1
    answered: False

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: root.scenario.get("title", "Tình huống")
            left_action_items: [["arrow-left", lambda x: app.go_back("scenario_list")]]
            elevation: 6

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(12)
                adaptive_height: True

                MDCard:
                    radius: [12,]
                    padding: dp(12)
                    md_bg_color: app.theme_cls.primary_light
                    elevation: 6
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        id: desc_label
                        text: root.scenario.get("description", "")
                        halign: "left"
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1]

                MDSeparator:
                    height: dp(1)

                MDLabel:
                    text: "Chọn phương án:"
                    font_style: "Subtitle1"
                    size_hint_y: None
                    height: dp(28)

                MDBoxLayout:
                    id: choice_box
                    orientation: "vertical"
                    spacing: dp(10)
                    adaptive_height: True

                MDLabel:
                    id: feedback
                    text: ""
                    theme_text_color: "Error"
                    halign: "center"
                    size_hint_y: None
                    height: dp(36)

        MDBoxLayout:
            size_hint_y: None
            height: dp(72)
            spacing: dp(12)
            padding: dp(12)

            MDRaisedButton:
                text: "📢 Gửi báo cáo"
                on_release: root.send_report()

            MDRaisedButton:
                text: "ℹ️ Giải thích"
                on_release: root.show_explanation()

        MDLabel:
            text: "© 2025 - Nhóm học sinh THCS Lý Tự Trọng | Fanpage: Lý Tự Trọng Gò Vấp"
            halign: "center"
            font_style: "Caption"
            size_hint_y: None
            height: dp(28)


<ResultScreen>:
    name: "result"
    title: "Kết quả"
    verdict_text: ""
    explanation: ""
    current_index: -1

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: root.title
            left_action_items: [["arrow-left", lambda x: app.go_back("scenario_list")]]
            elevation: 6

        MDLabel:
            id: verdict
            text: root.verdict_text
            halign: "center"
            font_style: "H6"
            size_hint_y: None
            height: dp(72)

        ScrollView:
            MDLabel:
                id: explanation
                text: root.explanation
                halign: "left"
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]

        MDBoxLayout:
            size_hint_y: None
            height: dp(64)
            spacing: dp(12)
            padding: dp(12)

            MDRaisedButton:
                text: "⬅️ Quay lại danh sách"
                on_release: app.go_back("scenario_list")

            MDRaisedButton:
                text: "➡️ Next"
                on_release: root.go_next()

        MDLabel:
            text: "© 2025 - Nhóm học sinh THCS Lý Tự Trọng | Fanpage: Lý Tự Trọng Gò Vấp"
            halign: "center"
            font_style: "Caption"
            size_hint_y: None
            height: dp(28)


<KnowledgeScreen>:
    name: "knowledge"
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "📖 Kho mẹo an toàn"
            left_action_items: [["arrow-left", lambda x: app.go_back("menu")]]
            elevation: 6

        ScrollView:
            MDList:
                id: tips_box
                padding: dp(8)

        MDLabel:
            text: "© 2025 - Nhóm học sinh THCS Lý Tự Trọng | Fanpage: Lý Tự Trọng Gò Vấp"
            halign: "center"
            font_style: "Caption"
            size_hint_y: None
            height: dp(28)


<HistoryScreen>:
    name: "history"
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "📊 Lịch sử"
            left_action_items: [["arrow-left", lambda x: app.go_back("menu")]]
            elevation: 6

        ScrollView:
            MDList:
                id: history_box
                padding: dp(8)

        MDBoxLayout:
            size_hint_y: None
            height: dp(72)
            spacing: dp(12)
            padding: dp(12)
            MDRaisedButton:
                text: "🗑️ Xoá lịch sử"
                on_release: root.clear_history()
            MDRaisedButton:
                text: "📤 Gửi báo cáo mẫu"
                on_release: root.send_sample_report()

        MDLabel:
            text: "© 2025 - Nhóm học sinh THCS Lý Tự Trọng | Fanpage: Lý Tự Trọng Gò Vấp"
            halign: "center"
            font_style: "Caption"
            size_hint_y: None
            height: dp(28)


<ProfileScreen>:
    name: "profile"
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "👤 Hồ sơ"
            left_action_items: [["arrow-left", lambda x: app.go_back("menu")]]
            elevation: 6

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(12)

            MDLabel:
                text: "Xin chào, Học viên!"
                font_style: "H6"
                halign: "center"

            MDProgressBar:
                id: profile_progress
                value: 0
                size_hint_y: None
                height: dp(8)

            MDLabel:
                id: profile_stat
                text: "Đã làm: 0  •  Đúng: 0  •  Tỉ lệ: 0%"
                halign: "center"
                font_style: "Caption"

        MDLabel:
            text: "© 2025 - Nhóm học sinh THCS Lý Tự Trọng | Fanpage: Lý Tự Trọng Gò Vấp"
            halign: "center"
            font_style: "Caption"
            size_hint_y: None
            height: dp(28)
'''

# ---------------- Data files & defaults ----------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "data_files")
os.makedirs(DATA_DIR, exist_ok=True)

SCENARIO_FILE = os.path.join(DATA_DIR, "scenarios.json")
USER_DATA_FILE = os.path.join(DATA_DIR, "user_data.json")
REPORTS_FILE = os.path.join(DATA_DIR, "reports.json")

DEFAULT_SCENARIOS = [
    {
        "id": "s1",
        "title": "Tin nhắn lạ",
        "description": "Bạn nhận được tin nhắn yêu cầu gửi mã OTP để nhận quà.",
        "choices": ["Gửi mã OTP", "Báo cho người lớn", "Gọi lại số lạ", "Xoá tin nhắn"],
        "correct_index": 1,
        "explanation": "Không bao giờ chia sẻ mã OTP. Báo cho người lớn hoặc quản trị."
    },
    {
        "id": "s2",
        "title": "Lời mời gặp mặt từ người lạ",
        "description": "Một người quen trên mạng mời bạn gặp ở quán cà phê một mình.",
        "choices": ["Đồng ý gặp 1-1", "Báo cho phụ huynh và chọn nơi công cộng", "Gửi địa chỉ nhà", "Gửi ảnh giấy tờ"],
        "correct_index": 1,
        "explanation": "Không nên gặp người lạ một mình; hãy thông báo người lớn và chọn nơi công cộng."
    },
    {
        "id": "s3",
        "title": "Tin nhắn yêu cầu chuyển tiền",
        "description": "Tin nhắn báo tài khoản bị khoá, yêu cầu chuyển tiền để mở.",
        "choices": ["Chuyển tiền ngay", "Kiểm tra kênh chính thức và hỏi người lớn", "Gửi OTP để xác minh", "Gọi lại số lạ"],
        "correct_index": 1,
        "explanation": "Đây có thể là lừa đảo. Kiểm tra kênh chính thức, không gửi OTP hay chuyển tiền."
    },
    {
        "id": "s4",
        "title": "Link lạ trong chat",
        "description": "Bạn được gửi link bảo 'nhận quà miễn phí' từ người lạ.",
        "choices": ["Click ngay", "Hỏi người gửi", "Không click và báo người lớn", "Chia sẻ link cho bạn bè"],
        "correct_index": 1,
        "explanation": "Không click link lạ, có thể chứa mã độc."
    },
    {
        "id": "s5",
        "title": "Yêu cầu địa chỉ nhà",
        "description": "Người lạ trên mạng yêu cầu địa chỉ để gửi quà.",
        "choices": ["Gửi địa chỉ thật", "Không gửi, báo cho người lớn", "Gửi địa chỉ giả", "Hẹn giao trong game"],
        "correct_index": 1,
        "explanation": "Không cung cấp thông tin cá nhân với người lạ."
    }
]
TIPS = [
    "Không chia sẻ địa chỉ, số điện thoại, mã OTP cho người lạ.",
    "Không nhấp vào link lạ, không tải file từ nguồn không rõ.",
    "Nếu có lời mời gặp mặt, hãy báo cho người lớn.",
    "Sử dụng mật khẩu mạnh, bật xác thực 2 yếu tố.",
    "Nếu bị quấy rối, chặn và báo cáo cho quản trị hoặc người lớn."
]

# ---------------- Helpers ----------------
def load_json_default(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ensure_default_files():
    if not os.path.exists(SCENARIO_FILE):
        save_json(SCENARIO_FILE, DEFAULT_SCENARIOS)
    if not os.path.exists(USER_DATA_FILE):
        save_json(USER_DATA_FILE, [])
    if not os.path.exists(REPORTS_FILE):
        save_json(REPORTS_FILE, [])


# ---------------- Screens logic ----------------
class MainMenuScreen(Screen):
    pass


class ScenarioListScreen(Screen):
    def on_pre_enter(self, *args):
        self.populate_list()

    def populate_list(self):
        self.ids.list_container.clear_widgets()
        scenarios = load_json_default(SCENARIO_FILE, [])
        from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
        for idx, s in enumerate(scenarios):
            item = OneLineAvatarIconListItem(text=f"{s.get('title')}",
                                            on_release=lambda inst, i=idx: self.open_index(i))
            item.add_widget(IconLeftWidget(icon="alert-circle"))
            self.ids.list_container.add_widget(item)

    def open_index(self, idx):
        scenarios = load_json_default(SCENARIO_FILE, [])
        if 0 <= idx < len(scenarios):
            sc = self.manager.get_screen("scenario")
            sc.set_scenario(scenarios[idx], idx)
            self.manager.current = "scenario"

    def open_random(self):
        scenarios = load_json_default(SCENARIO_FILE, [])
        if scenarios:
            idx = random.randrange(len(scenarios))
            self.open_index(idx)


class ScenarioScreen(Screen):
    scenario = DictProperty({})
    current_index = NumericProperty(-1)
    answered = BooleanProperty(False)

    def set_scenario(self, scenario, index):
        self.scenario = scenario
        self.current_index = index
        self.answered = False
        self.ids.choice_box.clear_widgets()
        from kivymd.uix.button import MDRaisedButton
        from kivymd.app import MDApp as _MDApp
        theme = _MDApp.get_running_app().theme_cls
        for i, choice in enumerate(scenario.get("choices", [])):
            btn = MDRaisedButton(
                text=f"{i+1}. {choice}",
                size_hint_y=None,
                height=dp(48),
                md_bg_color=theme.primary_light,
                on_release=lambda inst, idx=i: self.on_choose(idx)
            )
            self.ids.choice_box.add_widget(btn)
        self.ids.desc_label.text = scenario.get("description", "")
        self.ids.feedback.text = ""

    def on_choose(self, idx):
        if self.answered:
            return
        self.answered = True
        correct = self.scenario.get("correct_index", 0)
        is_correct = (idx == correct)
        # save answer
        data = load_json_default(USER_DATA_FILE, [])
        data.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "scenario_id": self.scenario.get("id"),
            "scenario_title": self.scenario.get("title"),
            "choice_index": idx,
            "choice_text": self.scenario.get("choices", [])[idx] if idx < len(self.scenario.get("choices", [])) else "",
            "correct_index": correct,
            "is_correct": is_correct
        })
        save_json(USER_DATA_FILE, data)

        # populate result screen
        res = self.manager.get_screen("result")
        res.title = self.scenario.get("title", "Kết quả")
        res.current_index = self.current_index
        if is_correct:
            res.verdict_text = "✅ AN TOÀN — Lựa chọn đúng"
        else:
            res.verdict_text = "⚠️ NGUY HIỂM — Lựa chọn sai"
        res.explanation = f"{self.scenario.get('explanation','')}\n\nPhương án đúng: {self.scenario.get('choices',[])[correct]}"
        self.manager.current = "result"

    def show_explanation(self):
        self.ids.feedback.text = self.scenario.get("explanation", "")

    def send_report(self):
        reports = load_json_default(REPORTS_FILE, [])
        reports.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "scenario_id": self.scenario.get("id"),
            "note": f"Người dùng gửi báo cáo cho '{self.scenario.get('title')}'."
        })
        save_json(REPORTS_FILE, reports)
        self.ids.feedback.text = "📤 Đã gửi báo cáo (mô phỏng)"


class ResultScreen(Screen):
    title = StringProperty("Kết quả")
    verdict_text = StringProperty("")
    explanation = StringProperty("")
    current_index = NumericProperty(-1)

    def go_next(self):
        scenarios = load_json_default(SCENARIO_FILE, [])
        next_idx = self.current_index + 1
        if next_idx < len(scenarios):
            sc = self.manager.get_screen("scenario")
            sc.set_scenario(scenarios[next_idx], next_idx)
            self.manager.current = "scenario"
        else:
            # nếu hết câu -> quay về danh sách
            self.manager.current = "scenario_list"


class KnowledgeScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.tips_box.clear_widgets()
        from kivymd.uix.list import OneLineListItem
        for t in TIPS:
            self.ids.tips_box.add_widget(OneLineListItem(text=t))


class HistoryScreen(Screen):
    def on_pre_enter(self, *args):
        Clock.schedule_once(lambda dt: self.populate(), 0.02)

    def populate(self):
        self.ids.history_box.clear_widgets()
        data = load_json_default(USER_DATA_FILE, [])
        reports = load_json_default(REPORTS_FILE, [])
        from kivymd.uix.list import OneLineListItem
        if not data and not reports:
            self.ids.history_box.add_widget(OneLineListItem(text="Chưa có lịch sử."))
            return
        for e in reversed(data):
            ok = "Đúng" if e.get("is_correct") else "Sai"
            self.ids.history_box.add_widget(OneLineListItem(text=f"[{e.get('timestamp')}] {e.get('scenario_title')} — {ok}"))
        if reports:
            self.ids.history_box.add_widget(OneLineListItem(text="--- Báo cáo ---"))
            for r in reversed(reports):
                self.ids.history_box.add_widget(OneLineListItem(text=f"[{r.get('timestamp')}] {r.get('note')}"))

    def clear_history(self):
        save_json(USER_DATA_FILE, [])
        save_json(REPORTS_FILE, [])
        self.populate()

    def send_sample_report(self):
        reports = load_json_default(REPORTS_FILE, [])
        reports.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "scenario_id": "sample",
            "note": "📢 Báo cáo mẫu"
        })
        save_json(REPORTS_FILE, reports)
        self.populate()


class ProfileScreen(Screen):
    def on_pre_enter(self, *args):
        data = load_json_default(USER_DATA_FILE, [])
        scenarios = load_json_default(SCENARIO_FILE, [])
        total_done = len(data)
        total_q = len(scenarios)
        done_pct = int(total_done / total_q * 100) if total_q else 0
        correct_count = sum(1 for d in data if d.get("is_correct"))
        correct_pct = int(correct_count / total_done * 100) if total_done else 0
        # set UI
        self.ids.profile_progress.value = done_pct
        self.ids.profile_stat.text = f"Đã làm: {total_done}  •  Đúng: {correct_count}  •  Tỉ lệ: {correct_pct}%"


# ---------------- App ----------------
class Canh_Giac_Online(MDApp):
    def build(self):
        ensure_default_files()
        # Material 3
        try:
            self.theme_cls.material_style = "M3"
        except Exception:
            pass
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def go_back(self, screen_name):
        self.root.current = screen_name


if __name__ == "__main__":
    Canh_Giac_Online().run()
