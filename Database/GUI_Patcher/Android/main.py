from pathlib import Path
import os
import platform
import threading

# Must be set before importing most of Kivy.
os.environ.setdefault("KIVY_NO_ARGS", "1")

from kivy.config import Config

# Desktop/Linux testing: avoid raw /dev/input providers stealing input.
Config.set("input", "mouse", "mouse")
Config.set("input", "mtdev", "")
Config.set("input", "probesysfs", "")
Config.set("input", "linuxwacom", "")

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


ROOT = Path(__file__).resolve().parents[3]


def fixed_label(text, height=32):
    return Label(text=text, size_hint_y=None, height=height, halign="left", valign="middle")


class OptionRow(BoxLayout):
    def __init__(self, text, checkbox, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=40, **kwargs)
        self.add_widget(Label(text=text, size_hint_x=0.82, halign="left", valign="middle"))
        self.add_widget(checkbox)


class AndroidPatcherUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        scroll = ScrollView()
        body = BoxLayout(orientation="vertical", padding=12, spacing=8, size_hint_y=None)
        body.bind(minimum_height=body.setter("height"))
        scroll.add_widget(body)
        self.add_widget(scroll)

        self.rom_path = TextInput(
            multiline=False,
            size_hint_y=None,
            height=44,
            hint_text="/sdcard/Download/DQMJ2P.nds",
        )
        self.out_path = TextInput(
            multiline=False,
            size_hint_y=None,
            height=44,
            hint_text="/sdcard/Download/DQMJ2P_patched.nds",
        )
        self.work_path = TextInput(
            multiline=False,
            size_hint_y=None,
            height=44,
            text=str(ROOT / "ANDROID_WORK"),
        )

        self.new_synths = CheckBox(active=True)
        self.xvariant = CheckBox(active=True)
        self.gender_icons = CheckBox(active=True)
        self.randomizer = CheckBox(active=False)

        body.add_widget(Label(text="DQMJ2 Pro Android Patcher Prototype", size_hint_y=None, height=42))
        body.add_widget(fixed_label("Input ROM"))
        body.add_widget(self.rom_path)
        body.add_widget(fixed_label("Output ROM"))
        body.add_widget(self.out_path)
        body.add_widget(fixed_label("Work folder"))
        body.add_widget(self.work_path)

        body.add_widget(OptionRow("Add new synthesis recipes", self.new_synths))
        body.add_widget(OptionRow("X/XY suffix fix", self.xvariant))
        body.add_widget(OptionRow("Gender icons -> polarity", self.gender_icons))
        body.add_widget(OptionRow("Enable randomiser", self.randomizer))

        patch_btn = Button(text="Patch ROM", size_hint_y=None, height=52)
        patch_btn.bind(on_release=self.start_patch)
        body.add_widget(patch_btn)

        body.add_widget(fixed_label("Log", 28))
        self.log = TextInput(
            readonly=True,
            multiline=True,
            size_hint_y=None,
            height=260,
            text="Ready.\n",
        )
        body.add_widget(self.log)

    def append_log(self, text):
        self.log.text += text.rstrip() + "\n"

    def start_patch(self, *_args):
        self.log.text = ""
        threading.Thread(target=self.patch_thread, daemon=True).start()

    def patch_thread(self):
        try:
            self.run_patch()
        except Exception as exc:
            Clock.schedule_once(lambda _dt: self.append_log(f"ERROR: {exc}"))

    def run_patch(self):
        rom = Path(self.rom_path.text.strip())
        out = Path(self.out_path.text.strip())
        work = Path(self.work_path.text.strip())

        Clock.schedule_once(lambda _dt: self.append_log(f"Platform: {platform.system()}"))
        Clock.schedule_once(lambda _dt: self.append_log(f"Repo: {ROOT}"))
        Clock.schedule_once(lambda _dt: self.append_log(f"ROM: {rom}"))
        Clock.schedule_once(lambda _dt: self.append_log(f"Output: {out}"))
        Clock.schedule_once(lambda _dt: self.append_log(f"Work: {work}"))
        Clock.schedule_once(lambda _dt: self.append_log(""))
        Clock.schedule_once(lambda _dt: self.append_log("UI works. Backend/tool integration is next."))


class DQMJ2PatcherAndroidApp(App):
    def build(self):
        return AndroidPatcherUI()


if __name__ == "__main__":
    DQMJ2PatcherAndroidApp().run()
