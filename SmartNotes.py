import json
notes ={
    "Newnote":{
            "текст":"Привіт",
            "теги":["new","Hello"]
}}

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
app=QApplication([])

notes_win=QWidget()
notes_win.setWindowTitle("Розумні нотатки")
notes_win.resize(900,600)

list_notes=QListWidget()
notes_list_name=QLabel("Список нотаток")

btn_create_note=QPushButton("Створити нотатку")
btn_del_note=QPushButton("Видалити нотатку")
btn_save_note=QPushButton("Зберегти нотатку")


list_tags=QListWidget()
tags_list_name=QLabel("Список тегів")
name_tag=QLineEdit("")
name_tag.setPlaceholderText("Введіть тег:")

btn_create_tag=QPushButton("Створити тег")
btn_del_tag=QPushButton("Видалити тег")
btn_search_tag=QPushButton("Шукати нотатку по тегам")


text_notes=QTextEdit()


layout_notes=QHBoxLayout()


col1=QVBoxLayout()
col1.addWidget(text_notes)

col2=QVBoxLayout()
col2.addWidget(notes_list_name)
col2.addWidget(list_notes)

row1=QHBoxLayout()
row1.addWidget(btn_create_note)
row1.addWidget(btn_del_note)

row2=QHBoxLayout()
row2.addWidget(btn_save_note)

col2.addLayout(row1)
col2.addLayout(row2)

col2.addWidget(tags_list_name)
col2.addWidget(list_tags)
col2.addWidget(list_notes)
col2.addWidget(name_tag)

row3=QHBoxLayout()
row3.addWidget(btn_create_tag)
row3.addWidget(btn_del_tag)


row4=QHBoxLayout()
row4.addWidget(btn_search_tag)


col2.addLayout(row3)
col2.addLayout(row4)

layout_notes.addLayout(col1,stretch=2)
layout_notes.addLayout(col2,stretch=1)


notes_win.setLayout(layout_notes)

def ShowNotes():
    key=list_notes.selectedItems()[0].text()
    print(key)
    for note in notes:
        if key==note[0]:
            text_notes.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])

list_notes.itemClicked.connect(ShowNotes)


def AddNote ():
    note_name, ok = QInputDialog.getText(notes_win,"Додати нотатку","Назва нотатки")
    if note_name and ok!="":
        notes[note_name]={"текст":"","теги":[]}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        print(notes)
def DelNote ():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        text_notes.clear()
        list_notes.addItems(notes)
        with open("notes_data.json","w",encoding="UTF-8") as file :
            json.dump(notes,file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Щось пішло не так")

def SaveNote ():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"]=text_notes.toPlainText()
        with open("notes_data.json", "w",encoding="UTF-8")as file:
            json.dump(notes,file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Щось пішло не так")


def AddTag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = name_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            name_tag.clear()
        with open("notes_data.json", "w",encoding="UTF-8")as file:
            json.dump(notes,file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Щось пішло не таааааааааааак")
def DelTag ():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w",encoding="UTF-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)


def SearchTag():
    print(btn_search_tag.text())
    tag=name_tag.text()
    if btn_search_tag.text()=="Шукати нотатку по тегам" and tag:
        print(tag)
        notes_filtered={}
        for note in notes:
            if tag in notes[note]["теги"] :
                notes_filtered[note]= notes[note]
        btn_search_tag.setText("скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(btn_search_tag.text())
    elif btn_search_tag.text()=="скинути пошук":
        name_tag.clear()
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(notes)
        btn_search_tag.setText("Шукати нотатку по тегам")
        print(btn_search_tag.text())
    else:
        pass


btn_create_note.clicked.connect(AddNote)
list_notes.itemClicked.connect(ShowNotes)
btn_del_note.clicked.connect(DelNote)
btn_save_note.clicked.connect(SaveNote)
btn_create_tag.clicked.connect(AddTag)
btn_search_tag.clicked.connect(SearchTag)
btn_del_tag.clicked.connect(DelTag)

notes_win.show()

with open ("notes_data.json", "r")as file:
    notes=json.load(file)
list_notes.addItems(notes)
app.exec_()