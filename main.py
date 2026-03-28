import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from plyer import filechooser

import fitz
import re
import pandas as pd

date_pattern = r'\d{2}/\d{2}/\d{4}'
amount_pattern = r'\d+\.\d{2}'
pattern = re.compile(f'({date_pattern})\s+(.*?)\s+({amount_pattern})')


class UI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.label = Label(text="Select a PDF file")
        self.add_widget(self.label)

        self.btn = Button(text="Choose PDF")
        self.btn.bind(on_press=self.pick_file)
        self.add_widget(self.btn)

        self.run_btn = Button(text="Extract")
        self.run_btn.bind(on_press=self.extract)
        self.add_widget(self.run_btn)

        self.file_path = None

    def pick_file(self, instance):
        filechooser.open_file(on_selection=self.set_file)

    def set_file(self, selection):
        if selection:
            self.file_path = selection[0]
            self.label.text = f"Selected:\n{self.file_path}"

    def extract(self, instance):
        if not self.file_path:
            self.label.text = "No file selected"
            return

        try:
            doc = fitz.open(self.file_path)
            lines = []

            for page in doc:
                for b in page.get_text("blocks"):
                    if b[4].strip():
                        lines.append(b[4].strip())

            data = []
            for i, line in enumerate(lines):
                combined = line + " " + (lines[i+1] if i+1 < len(lines) else "")
                m = pattern.search(combined)
                if m:
                    date, desc, amount = m.groups()
                    data.append([date, desc, amount])

            df = pd.DataFrame(data, columns=["Date", "Description", "Amount"])

            output = "/sdcard/Download/transactions.csv"
            df.to_csv(output, index=False)

            self.label.text = f"✅ Saved: {len(data)} rows\n{output}"

        except Exception as e:
            self.label.text = f"Error:\n{str(e)}"


class MyApp(App):
    def build(self):
        return UI()


MyApp().run()
