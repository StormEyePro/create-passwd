from PyQt5.Qt import QTextEdit,QPushButton,QWidget,QApplication,QThread,pyqtSignal,QTextCursor,QComboBox,QLabel
import sys
import os
import re
import threading
import time
import chardet

class Worker(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        #设置工作状态与初始num数值
        self.working = False
        self.num = 0

    def __del__(self):
        #线程状态改变与线程终止
        self.working = False
        self.wait()


    def run(self):
        print('run')
        while True:
            time.sleep(1)
            if self.working:
                #获取文本
                file_str = 'File index{0}'.format(self.num)
                self.num += 1
                # 发射信号
                self.sinOut.emit(file_str)
                # 线程休眠2秒
                self.working=False
                self.__del__()




class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('根据用户名生成弱口令')
        self.resize(500, 430)
        file = 'get_banner'
        self.response=''
        self.s = set()
        self.txt = set()
        self.pass_file=''
        self.user_file = ''
        self.usernames=''
        if not os.path.exists('tmp'):
            os.mkdir('tmp')

        with open('config/dynamic_password.txt', 'r', encoding='utf-8') as f:
            for line in f:
                self.s.add(line)
        self.base_password=os.path.dirname(os.path.realpath(__file__))+'/config/static_password/'+'空.txt'
        self.setup_ui()

    def get_encoding(self,file):
        with open(file, 'rb') as f:
            cd = chardet.detect(f.read())
        return cd['encoding']

    def thread_get_banner(self,usernames):

        with open(self.base_password, 'r', encoding=self.get_encoding(self.base_password)) as f:
            self.txt=self.txt|set(f.readlines())
        usernames = usernames.split('\n')
        for user in usernames:
            for ss in self.s:
                if re.search(r'%user%',ss):
                    ss=ss.replace('%user%',user)
                self.txt.add(ss)

        self.response=''
        self.response=''.join(self.txt)
        self.pass_file=os.path.dirname(os.path.realpath(__file__))+'/tmp/pass_'+str(time.strftime("%Y.%m.%d-%H.%M.%S", time.localtime()))+'.txt'
        self.user_file = os.path.dirname(os.path.realpath(__file__)) + '/tmp/user_' + str(
            time.strftime("%Y.%m.%d-%H.%M.%S", time.localtime())) + '.txt'
        with open(self.pass_file,'w',encoding='utf-8') as f:
            f.write(self.response)
        with open(self.user_file,'w',encoding='utf-8') as f:
            f.write(self.usernames)
        self.txt.clear()

        self.info.setText('正在刷新...')
        self.flush.working = True


    def flush_ui(self,response):
        self.ql_c.setText(self.response)
        self.info.setText('完成！')

    def setup_ui(self):


        ql_b = QTextEdit(self)
        ql_b.move(0, 80)
        ql_b.resize(245,350)
        ql_b.setPlaceholderText('输入用户名，以换行分割。\n用户名会根据config/dynamic_password.txt的规则进行替换；\n可选择右侧的密码追加进结果里，默认为空.txt。')

        self.ql_c = QTextEdit(self)
        self.ql_c.move(255, 80)
        self.ql_c.resize(245, 350)

        btn = QPushButton(self)
        btn.setText('生成')
        btn.resize(100,40)
        btn.move(200, 40)

        bt2=QComboBox(self)
        bt2.move(300,41)
        bt2.resize(200,38)
        bt2.AdjustToContentsOnFirstShow
        files=os.listdir(os.path.dirname(os.path.realpath(__file__))+'/config/static_password')
        bt2.addItems(files)
        self.base_password=os.path.dirname(os.path.realpath(__file__))+'/config/static_password/'+files[0]

        fzyh_bt = QPushButton(self)
        fzyh_bt.setText('copy用户名路径')
        fzyh_bt.resize(100, 40)
        fzyh_bt.move(0, 40)

        fz_bt=QPushButton(self)
        fz_bt.setText('copy密码路径')
        fz_bt.resize(100,40)
        fz_bt.move(100,40)

        self.info=QLabel(self)
        self.info.resize(100,30)
        self.info.move(0,0)


        self.flush = Worker()
        self.flush.sinOut.connect(self.flush_ui)


        def go():
            self.usernames = ql_b.toPlainText()

            self.flush.start()
            self.info.setText('正在生成...')
            t=threading.Thread(target=self.thread_get_banner,args=(self.usernames,))
            t.start()




        btn.clicked.connect(go)
        bt2.currentIndexChanged[str].connect(self.print_value)
        fz_bt.clicked.connect(self.fz)
        fzyh_bt.clicked.connect(self.fzyh)

    def print_value(self,str):
        self.base_password=os.path.dirname(os.path.realpath(__file__))+'/config/static_password/'+str

    def fz(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.pass_file)

    def fzyh(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.user_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from PyQt5 import QtCore
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    window = Window()
    window.show()
    sys.exit(app.exec_())