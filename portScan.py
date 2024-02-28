import wx
import socket
from dicio import services_dict

class ResultDialog(wx.Dialog):
    def __init__(self, parent, data):
        super(ResultDialog, self).__init__(parent, title='Resultados', size=(300, 300))

        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Ip', width=50)
        self.list_ctrl.InsertColumn(1, 'Serviço', width=150)
        self.list_ctrl.InsertColumn(2, 'Estado', width=100)

        for index, (id, service, state) in enumerate(data):
            self.list_ctrl.InsertItem(index, str(id))
            self.list_ctrl.SetItem(index, 1, service)
            self.list_ctrl.SetItem(index, 2, state)

        # Ajustar o layout usando um BoxSizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.panel = wx.Panel(self)
        # Campo para inserir o IP
        self.ip_label = wx.StaticText(self.panel, label="IP:", pos=(10, 10))
        self.ip_text = wx.TextCtrl(self.panel, pos=(70, 10), size=(150, -1))

        # Campos para definir o range
        self.min_label = wx.StaticText(self.panel, label="Mínimo:", pos=(10, 40))
        self.min_text = wx.TextCtrl(self.panel, pos=(70, 40), size=(70, -1))

        self.max_label = wx.StaticText(self.panel, label="Máximo:", pos=(10, 70))
        self.max_text = wx.TextCtrl(self.panel, pos=(70, 70), size=(70, -1))

        # Botão para processar os valores
        self.process_button = wx.Button(self.panel, label="Processar", pos=(10, 120))
        self.Bind(wx.EVT_BUTTON, self.on_process_button_click, self.process_button)

        self.checkbox = wx.CheckBox(self.panel, label="Well-Known", pos=(10, 100))
        self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change, self.checkbox)


    def on_checkbox_change(self, event):
        # Lógica a ser executada quando o estado do checkbox é alterado
        if self.checkbox.GetValue():
            wx.MessageBox("Marcando isso você passsará apenas pelas Well-Know Ports!", "Informação", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Desmarcando passará por todas as portas!", "Informação", wx.OK | wx.ICON_INFORMATION)
 

    def on_process_button_click(self, event):
        ip_value = self.ip_text.GetValue()
        min_value = int(self.min_text.GetValue())
        max_value = int(self.max_text.GetValue())
        check_box_value = self.checkbox.GetValue()

        server_ip = socket.gethostbyname(ip_value)

        string = []

        for port in range(min_value, max_value+1):
            if port in services_dict.keys() and check_box_value:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((server_ip, port))
                if result == 0:
                    name = services_dict.get(port)
                    string.append((port, name, "Open"))
                else:
                    name = services_dict.get(port)
                    string.append((port,name,"Closed"))
                sock.close()
            elif not check_box_value:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((server_ip, port))
                if result == 0:
                    name = services_dict.get(port, "Unknown Service")
                    string.append((port, name, "Open"))
                else:
                    name = services_dict.get(port, "Unknown Service")
                    string.append((port,name,"Closed"))
                sock.close()

        # Criar uma instância da ResultDialog
        result_dialog = ResultDialog(self, string)
        result_dialog.ShowModal()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, title='Preencha com o ip e o intervalo', size=(300, 200))
    frame.Show()
    app.MainLoop()
