import pdfplumber
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class ICICIProApp(App):
    def build(self):
        self.df = pd.DataFrame()
        layout = BoxLayout(orientation='vertical')
        self.filechooser = FileChooserListView(size_hint=(1,0.4))
        layout.add_widget(self.filechooser)

        self.search = TextInput(hint_text="Search keyword", size_hint=(1,0.1))
        layout.add_widget(self.search)

        btn_layout = BoxLayout(size_hint=(1,0.1))
        load_btn = Button(text="Load PDF")
        load_btn.bind(on_press=self.load_pdf)
        btn_layout.add_widget(load_btn)

        search_btn = Button(text="Search")
        search_btn.bind(on_press=self.search_data)
        btn_layout.add_widget(search_btn)

        export_btn = Button(text="Export CSV")
        export_btn.bind(on_press=self.export_csv)
        btn_layout.add_widget(export_btn)

        layout.add_widget(btn_layout)

        self.output = Label(size_hint_y=None, text="")
        self.output.bind(texture_size=self.output.setter('size'))
        scroll = ScrollView(size_hint=(1,0.4))
        scroll.add_widget(self.output)
        layout.add_widget(scroll)
        return layout

    def load_pdf(self, instance):
        if not self.filechooser.selection:
            self.output.text = "Select a PDF"
            return
        file_path = self.filechooser.selection[0]
        rows = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            if row and len(row)>=5:
                                date, desc, dep, wd, bal = row[:5]
                                if "date" in str(date).lower():
                                    continue
                                rows.append({"Date":date,"Particulars":desc,"Deposit":dep,"Withdrawal":wd,"Balance":bal})
            self.df = pd.DataFrame(rows)
            self.output.text = f"Loaded {len(self.df)} transactions"
        except Exception as e:
            self.output.text = f"Error: {str(e)}"

    def search_data(self, instance):
        if self.df.empty:
            self.output.text = "Load PDF first"
            return
        keyword = self.search.text.lower()
        filtered = self.df[self.df["Particulars"].str.lower().str.contains(keyword, na=False)]
        if filtered.empty:
            self.output.text = "No results found"
        else:
            text = ""
            for _, row in filtered.head(50).iterrows():
                text += f"{row['Date']} | {row['Particulars']} | {row['Deposit']} | {row['Withdrawal']} | {row['Balance']}\n"
            self.output.text = text

    def export_csv(self, instance):
        if self.df.empty:
            self.output.text = "No data to export"
            return
        self.df.to_csv("transactions.csv", index=False)
        self.output.text = "Saved as transactions.csv"

ICICIProApp().run()
