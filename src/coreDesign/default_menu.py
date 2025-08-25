
class DefaultMenu:

    def create_menu(self):
        menu = QMenu()
        new_file_act = QAction("Novo arquivo", self)
        new_file_act.setShortcut("Ctrl+N")
        new_file_act.triggered.connect(self.new_file)
        menu.addAction(new_file_act)

        open_file_act = QAction("Abrir Arquivo", self)
        open_file_act.setShortcut("Ctrl+O")
        open_file_act.triggered.connect(self.showDialogAndOpenFile)
        menu.addAction(open_file_act)

        save_file_act = QAction("Salvar Arquivo", self)
        save_file_act.setShortcut("Ctrl+S")
        save_file_act.triggered.connect(self.saveFile)
        menu.addAction(save_file_act)

        menu.setFixedWidth(210)
        return menu