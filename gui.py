import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
import functions
from concurrent.futures import ThreadPoolExecutor
import threading
import os
from tqdm import tqdm
import sys

VER = "α0.6"
WORKERS = 4
l=[]
no=0
dir=""
#FROM CUI

def main():
    global l
    global VER
    global WORKERS
    global silence
    global dir
    global isSilence
    global statusLabel
    global update
    print(l)
    #ユーザー設定の変数
    downloadDir = (dir + '/' + functions.makeDirName() + '/')
    now = silence.get()
    print(now)
    if now == 0:
        isSilence = "true"
    elif now == 1:
        isSilence = "false"
    print(isSilence)
    print('[System:notice]\u0020ダウンロードを開始します')
    #l配列内の全ての値をdownload関数へ代入
    statusLabel.config(text="動作中")
    with ThreadPoolExecutor(max_workers=WORKERS) as tpe:
        for onel in l:
            print('[System:Start]\u0020' + onel[1] + onel[2])
            #MVを検索ワードに追加することでFIRSTTAKE回避
            #マルチスレッド処理にsubmit
            tpe.submit(functions.download,onel[1] + onel[2] + 'mv',downloadDir,isSilence)
            update()
    tpe.shutdown()
    print('[System:notice]\u0020すべてのダウンロードが完了しました')
    statusLabel.config(text="完了")
    return

#backendここから
def update():
    global pbval
    global pbmax
    global pb
    pbval.set(pbval.get() + 1)
    if pbval.get() > pbmax:
        pbval.set(0)
def quit_me(root_window):
    root_window.quit()
    root_window.destroy()
def updateList():
    global l
    for i in l:
        list.insert("","end",values=(i[0],i[1],i[2]))
def addMusic():
    global no
    global l
    no += 1
    artist = addArtistBox.get()
    title = addTitleBox.get()
    #if not artist or not title:
    #    messagebox.showwarning('ROX Assistant Error', 'アーティスト名と曲名、またはその片方が不正な値です。')
    #    return
    l.append([no,artist,title])
    list.insert("","end",values=(no,artist,title))
    addArtistBox.delete(0, tk.END)
    addTitleBox.delete(0, tk.END)
def removeMusic():
    global no
    global list
    global l
    id = list.focus()
    value = list.item(id, 'values')
    rid = int(value[0]) - 1
    list.delete(id)
    del l[rid]
    no=0
    l = sorted(l, key=lambda x: x[0])
    for i in l:
        no +=1
        i[0] = no
    list.delete(*list.get_children())
    updateList()
def clear():
    global list
    global l
    global no
    res = messagebox.askokcancel(title="リストのクリア", message="リストの内容が全て削除されます。よろしいですか？")
    if res == True:
        no = 0
        l = []
        list.delete(*list.get_children())
def dir_click():
    global dir
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    dirName.set(iDirPath)
    dir = iDirPath
def click_download():
    global pbmax
    pbmax = len(l)
    thread1 = threading.Thread(target=main)
    thread1.start()
    statusLabel["text"] = "完了"
    return
#backendここまで
#frontendここから
root = tk.Tk()
root.title(u"ROX Assistant")
root.protocol("WM_DELETE_WINDOW", lambda :quit_me(root))
root.geometry("1000x600")

#フレーム作成
titleFrame = tk.Frame(root)
addFrame = tk.LabelFrame(root,bd=2,relief="ridge",text="追加フォーム")
listFrame = tk.LabelFrame(root,bd=2,relief="ridge",text="ダウンロードリスト")
listControlFrame = tk.Frame(root)
controlFrame = tk.Frame(root)
silenceFrame = tk.LabelFrame(controlFrame,bd=2,relief="ridge",text="無音削除")
dirFrame = tk.LabelFrame(controlFrame,bd=2,relief="ridge",text="保存フォルダ")
runFrame = tk.LabelFrame(controlFrame,bd=2,relief="ridge",text="実行")
statusFrame = tk.LabelFrame(controlFrame,bd=2,relief="ridge",text="ステータス")
progressbarFrame = tk.LabelFrame(root,bd=2,relief="ridge",text="進捗バー")

#ロゴ・タイトル
logo = tk.PhotoImage(file="/Users/nswk/Documents/GitHub/rox/images/logo_small.png")

image=tk.Label(titleFrame,image=logo)
image['bg'] = root['bg']

#アーティスト・曲名入力
addArtistLabel = tk.Label(addFrame,text='アーティスト名', width=10)
addArtistBox = tk.Entry(addFrame,width=20)

addTitleLabel = tk.Label(addFrame,text='曲名', width=10)
addTitleBox = tk.Entry(addFrame,width=20)

addSubmit = tk.Button(addFrame,text='追加', width=10, command=addMusic)
#list
list = ttk.Treeview(listFrame)
list["column"] = (1,2,3)
list["show"] = "headings"
list.heading(1,text="No.")
list.heading(2,text="アーティスト")
list.heading(3,text="曲名")
list.column(1, width=6)
list.column(2, width=207)
list.column(3, width=207)
scroll = tk.Scrollbar(listFrame, orient=tk.VERTICAL, command=list.yview)
scroll.pack(side=tk.RIGHT, fill="y")
list["yscrollcommand"] = scroll.set

#list操作
listDelete = tk.Button(listControlFrame,text='選択した項目を削除', width=20,command=removeMusic)
listClear = tk.Button(listControlFrame,text='リストをクリア', width=20,command=clear)

#操作
controlRun = tk.Button(runFrame, text='ダウンロードを開始',width=20,command=click_download)

#無音削除
silence = tk.IntVar()
silence.set(0)
silenceEnable = tk.Radiobutton(silenceFrame,value=0,variable=silence,text='有効')
silenceDisable = tk.Radiobutton(silenceFrame,value=1,variable=silence,text='無効')

#ディレクトリ選択
dirName = tk.StringVar()
IDirEntry = ttk.Entry(dirFrame, textvariable=dirName, width=30)
IDirButton = ttk.Button(dirFrame, text="参照", command=dir_click)

#ダウンロード中
statusLabel = tk.Label(statusFrame,text=u"　", font=("", 12))
statusLabel["text"] = "停止中"

#status


#配置
titleFrame.pack(fill="x",padx=60,pady=0)
addFrame.pack(fill="x",padx=60,pady=0)
listFrame.pack(fill="x",padx=60,pady=0)
listControlFrame.pack(fill="x",padx=60,pady=0)
controlFrame.pack(fill="x",padx=60,pady=0)
silenceFrame.pack(side=tk.LEFT,padx=0,pady=10)
dirFrame.pack(side=tk.LEFT,padx=10,pady=10)
runFrame.pack(fill="x",side=tk.LEFT,padx=10,pady=10)
statusFrame.pack(fill="x",side=tk.LEFT,padx=0,pady=10)
progressbarFrame.pack(fill="x",side=tk.LEFT,padx=0,pady=10)

image.pack(side=tk.LEFT)

addArtistLabel.pack(side=tk.LEFT, anchor = tk.W)
addArtistBox.pack(side=tk.LEFT, anchor = tk.W)

addTitleLabel.pack(side=tk.LEFT, anchor = tk.W)
addTitleBox.pack(side=tk.LEFT, anchor = tk.W)

addSubmit.pack(side=tk.RIGHT, anchor = tk.W)

list.pack(side=tk.TOP ,fill=tk.BOTH)
listDelete.pack(side=tk.RIGHT, anchor = tk.W)
listClear.pack(side=tk.RIGHT, anchor= tk.W)

silenceEnable.pack(side=tk.LEFT,anchor = tk.W)
silenceDisable.pack(side=tk.LEFT,anchor = tk.W)

IDirEntry.pack(side=tk.LEFT)
IDirButton.pack(side=tk.LEFT)

controlRun.pack(side=tk.LEFT,anchor = tk.W)

statusLabel.pack(side=tk.TOP)

pb.pack(side=tk.BOTTOM)

#表示
if __name__ == "__main__":
    root.mainloop()