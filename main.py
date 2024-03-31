import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
def returnn(event=None):
    window.quit()
def about(event=None):
    def close():
        abt.destroy()
    abt = Toplevel()
    abt.title('Справка')
    abt.iconbitmap('msk.ico')
    abt.geometry('530x163')
    abt.resizable(FALSE, FALSE)
    txt = 'База данных: Известные исторические места Москвы\nПозволяет: добавлять / изменять / удалять информацию.\nКлавиши программы:\nCTRL-0 - Вызов справки по программе,\nCTRL-A - Добавить в базу данных,\nCTRL-D - Удалить из базы данных,\nCTRL-E - Изменить запись в базе данных.'
    Label(abt, text=txt,justify=LEFT,font="Arial 10 normal roman").pack(anchor=NW)
    Button(abt,text='Выход', command=close,bg='PINK').place(x=480,y=136)
def about_program(event=None):
    messagebox.showinfo("О программе", "База данных «Известные исторические места Москвы»\nЭлектронная почта: smartasscheeseburger@gmail.com\n(c) Эгамов Р.Б. Россия, 2077г.")

def adding(event=None):
    def open_img():
        global adding_filename
        adding_filename = filedialog.askopenfilename(title='open', filetypes=[("Image files", ".png")])
        if adding_filename == '':
            del globals()['adding_filename']
            return
        else:
            adding_photo = PhotoImage(file=adding_filename)
            adding_photo = img_size(adding_photo)
            adding_preview = Label(plus,image=adding_photo,height=200,width=200)
            adding_preview.place(x=73,y=246)
            adding_preview.image = adding_photo
    def bd_add():
        if bd_name.index('end') == 0:
            messagebox.showinfo("Внимание", 'Введите название!')
            return
        elif 'adding_filename' not in globals():
            messagebox.showinfo("Внимание", 'Выберите фотографию!')
            return
        name_add = bd_name.get()
        desc_add = bd_desc.get(1.0,END)
        for i in range(artbox.size()):
            item = artbox.get(i)
            if name_add in item:
                messagebox.showinfo("Внимание", 'Такое название уже есть, введите другое!')
                return
        with open(adding_filename, 'rb') as file:
            blobData = file.read()
        cursor.execute('INSERT INTO artist (name,text,photo) VALUES (?,?,?)',(name_add,desc_add,blobData))
        con.commit()
        artbox.delete(0,END)
        lst.clear()
        cursor.execute('SELECT name FROM artist')
        description.config(state=NORMAL)
        description.delete(1.0, END)
        description.config(state=DISABLED)
        label.config(image=quest_image)
        for cur in cursor:
            lst.append(cur)
            for i in range(len(cur)):
                artbox.insert(END, cur[i])
        del globals()['adding_filename']
        plus.destroy()
        messagebox.showinfo('Уведомление','Добавление прошло успешно!')
    def deletos():
        plus.destroy()
    plus = Toplevel()
    plus.grab_set()
    plus.iconbitmap('add.ico')
    plus.title('Добавление записи')
    plus.geometry('350x480')
    plus.resizable(FALSE, FALSE)
    quest = PhotoImage(file='no_img.png')
    quest = img_size(quest)
    Label(plus, text = 'Введите название',width=57).pack(anchor=SW)
    bd_name = Entry(plus,width=57)
    bd_name.pack(anchor=SW)
    Label(plus, text='Введите описание', width=49).pack(anchor=SW)
    bd_desc = Text(plus, wrap=WORD, width=49,height=10)
    bd_desc.pack(anchor=SW)
    Label(plus, text='Выберите картинку', width=40).pack(anchor=N)
    no_image = Label(plus, image=quest, width=200, height=200)
    no_image.pack(anchor=N)
    no_image.image = quest
    add_preview = Label(plus)
    add_preview.pack()
    Button(plus,text='Обзор',command=open_img).place(x=145,y=450)
    Button(plus,text='Добавить',command=bd_add).place(x=285,y=450)
    Button(plus, text='Выход', command=deletos).place(x=2, y=450)

def searching(event=None):
    def canceling():
        search.destroy()
    def func():
        num_flag = 0
        artbox.selection_clear(0, END)
        search_term = search_entry.get()
        list_items = artbox.get(0, END)
        for i, item in enumerate(list_items):
            if search_term.lower() in item.lower():
                num_flag += 1
                artbox.activate(i)
                artbox.selection_set(i, i)
        if num_flag == 1:
            search.destroy()
            on_change('')
        elif num_flag > 1:
            description.config(state=NORMAL)
            description.delete(1.0, END)
            description.config(state=DISABLED)
            search.destroy()
            label.config(image=quest_image)
        else:
            messagebox.showinfo('Внимание', 'Ничего не найдено. Введите снова!')
            search_entry.delete('0',END)
    search = Toplevel() #виджет
    search.geometry('200x75')
    search.grab_set()
    search.title('Поиск записи')
    search.resizable(FALSE, FALSE)
    search_label = Label(search, text="Введите название:")
    search_label.pack()
    search_entry = Entry(search)
    search_entry.pack()
    search_button = Button(search, text="Поиск", command=func)
    search_button.place(x=150,y=45)
    exit_button = Button(search, text="Выход", command=canceling)
    exit_button.place(x=2,y=45)

def delete(event=None):
    if 'selection' not in globals():
        messagebox.showinfo('Внимание','Выберите поле!')
        return
    cursor.execute('DELETE FROM artist WHERE name=?', artist_name)
    con.commit()
    artbox.delete(0, END)
    lst.clear()
    cursor.execute('SELECT name FROM artist')
    for cur in cursor:
        lst.append(cur)
        for i in range(len(cur)):
            artbox.insert(END, cur[i])
    description.config(state=NORMAL)
    description.delete(1.0, END)
    description.config(state=DISABLED)
    label.config(image=quest_image)
    del globals()['selection']

def on_change(event):
    global selection, artist_name, artist_image
    selection = artbox.curselection()
    if selection:
        artist_name = lst[selection[0]]
        cursor.execute('SELECT * FROM artist where name = ?', artist_name)
        for row in cursor.fetchall():
            description.config(state=NORMAL)
            description.delete(1.0,END)
            description.insert(1.0,row[2])
            description.config(state=DISABLED)
            image_data = row[3]
            artist_image = PhotoImage(data=image_data)
            artist_image = large_img_size(artist_image)
            label.config(image=artist_image)

def img_size(image):
    y = image.height() // 200
    x = image.width() // 200
    if y>x: x=y
    if (image.height() // 200 > 0) and (image.width() // 200 > 0):
        if image.height() - image.width() >= 200: return image.subsample(x, y + ((image.height() - image.width())//200))
        elif image.width() - image.height() >= 200: return image.subsample(x + ((image.width() - image.width())//200), y)
        else: return image.subsample(x, y)
    else:
        return image.subsample(1,1)

def large_img_size(image):
    y = image.height() // 440
    x = image.width() // 500
    if y>x: x=y
    if (image.height() // 440 > 0) and (image.width() // 500 > 0):
        if image.height() - image.width() >= 400: return image.subsample(x,y+((image.height() - image.width())//400))
        elif image.width() - image.height() >= 400: return image.subsample(x+((image.width() - image.width())//400),y)
        else: return image.subsample(x, y)
    else: return image.subsample(1,1)

def changing(event=None):
    def canceling():
        edit.destroy()
    def open_imag():
        global changing_filename
        changing_filename = filedialog.askopenfilename(title='open', filetypes=[("Image files", ".png")])
        if changing_filename == '':
            del globals()['changing_filename']
            return
        else:
            changing_photo = PhotoImage(file=changing_filename)
            changing_photo = img_size(changing_photo)
            preview_changing = Label(edit, height=200, width=200, image=changing_photo)
            preview_changing.place(x=73,y=246)
            preview_changing.image = changing_photo
    def bd_change():
        if edit_name.index('end') == 0:
            messagebox.showinfo("Внимание", 'Не оставляйте поля пустыми!')
            return
        name_edit = edit_name.get()
        desc_edit = edit_desc.get(1.0, END)
        for i in range(artbox.size()):
            item = artbox.get(i)
            if name_edit in item and name_edit != artist_name[0]:
                messagebox.showinfo("Внимание", 'Такое название уже есть, введите другое!')
                return
        cursor.execute('SELECT id FROM artist WHERE name=?',artist_name)
        artist = cursor.fetchone()
        if 'changing_filename' in globals():
            with open(changing_filename, 'rb') as file:
                blbData = file.read()
            cursor.execute('UPDATE artist SET name = ?,text = ?,photo = ? where id = ?',(name_edit, desc_edit, blbData, artist[0]))
        else: cursor.execute('UPDATE artist SET name = ?,text = ? where id = ?',(name_edit, desc_edit, artist[0]))
        con.commit()
        artbox.delete(0,END)
        lst.clear()
        cursor.execute('SELECT name FROM artist')
        for cur in cursor:
            lst.append(cur)
            for i in range(len(cur)):
                artbox.insert(END, cur[i])
        messagebox.showinfo('Уведомление','Изменение прошло успешно!')
        edit.destroy()
        description.config(state=NORMAL)
        description.delete(1.0, END)
        description.config(state=DISABLED)
        if 'changing_filename' in globals():
            del globals()['changing_filename']
        label.config(image=quest_image)
    if 'selection' not in globals():
        messagebox.showinfo('Внимание','Выберите поле!')
        return
    edit = Toplevel()
    edit.grab_set()
    edit.title('Изменение записи')
    edit.geometry('350x480')
    edit.resizable(FALSE, FALSE)
    edit.iconbitmap('rename.ico')
    Label(edit, text = 'Введите название',width=57).pack(anchor=SW)
    edit_name = Entry(edit,width=57)
    edit_name.insert(0,''.join((*map(str, artist_name), '')))
    edit_name.pack(anchor=SW)
    Label(edit, text='Введите описание', width=49).pack(anchor=SW)
    edit_desc = Text(edit, wrap=WORD, width=49,height=10)
    edit_desc.pack(anchor=SW)
    edit_desc.insert(END,description.get('1.0',END))
    Label(edit, text='Выберите картинку', width=49).pack(anchor=SW)
    small_image = img_size(artist_image)
    img_edit = Label(edit,image=small_image,height=200,width=200)
    img_edit.image = small_image
    img_edit.pack(anchor=S)
    Button(edit,text='Обзор',command=open_imag).place(x=145,y=450)
    Button(edit,text='Изменить',command=bd_change).place(x=285,y=450)
    Button(edit, text='Отмена', command=canceling).place(x=2, y=450)

#Подключение БД
con = sqlite3.connect('Artist.db')
cursor = con.cursor()
#Создание основного окна
window = Tk()
lst = []
window.title('Исторические места Москвы')
window.geometry('960x480')
window.resizable(FALSE,FALSE)
#Создание меню

main_menu = Menu()
file_menu = Menu(tearoff=0)
help_menu = Menu(tearoff=0)
help_menu.add_command(label="Содержание", command=about)
help_menu.add_separator()
help_menu.add_command(label="О программе", command=about_program, accelerator='Ctrl-0')
file_menu.add_command(label="Найти", command=searching)
file_menu.add_separator()
file_menu.add_command(label="Добавить",command=adding,accelerator='Ctrl-A')
file_menu.add_command(label="Удалить",command=delete,accelerator='Ctrl-D')
file_menu.add_command(label="Изменить",command=changing,accelerator='Ctrl-E')
file_menu.add_separator()
file_menu.add_command(label="Выход", command=returnn)
main_menu.add_cascade(label="Фонд", menu=file_menu)
main_menu.add_cascade(label="Справка", menu=help_menu)
window.config(menu=main_menu)
#Создание бокса с именами
artbox = Listbox(height=26,width=20,font="Arial 14 normal roman",activestyle='none')
artbox.pack(side=LEFT,anchor=N)
#Добавление имен авторов
cursor.execute('SELECT name FROM artist')
for cur in cursor:
    lst.append(cur)
    for i in range(len(cur)):
        artbox.insert(END, cur[i])
#Создание окошка с фото
quest_image = PhotoImage(file='no-photo-available.png')
label = Label(height=440,width=500,bg='RED')
label.config(image=quest_image)
label.pack(side=LEFT,anchor=N)
#Создание окошка с описанием
description = Text(height=18,width=345,wrap=WORD,font="Arial 16 normal roman")
description.pack(side=LEFT,anchor=N)
ttt = 'Ctrl-0 - О программе     Ctrl-A - Добавить    Ctrl-D - Удалить    Ctrl-E - Изменить'
Label(window,width=150,height=40,justify=LEFT,font="Arial 18 normal roman",text=ttt,bg='RED', fg='WHITE',anchor=NW).place(y=444,x=0)
#Привязка скрипта к артбоксу
artbox.bind('<<ListboxSelect>>',on_change)
window.bind('<Control-a>',adding)
window.bind('<Control-0>',about_program)
window.bind('<Control-d>',delete)
window.bind('<Control-e>',changing)
window.bind('<Control-A>',adding)
window.bind('<Control-D>',delete)
window.bind('<Control-E>',changing)
window.iconbitmap('msk.ico')
window.config(cursor="gumby")
window.mainloop()