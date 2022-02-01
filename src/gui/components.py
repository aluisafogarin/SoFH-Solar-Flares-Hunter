class Components():
    def createToolBar(self):
        tool_bar = self.addToolBar("Download")

        button_download = QToolButton()
        button_download.setIcon(QtGui.QIcon(
            self.paths.generate_icon_path("download.png")))

        button_convert = QToolButton()
        button_convert.setIcon(QtGui.QIcon(
            self.paths.generate_icon_path("convert.png")))
        button_convert.connect()

        tool_bar.addWidget(button_download)
        tool_bar.addWidget(button_convert)

    # TODO Refactor menu bar
    def createMenuBar(self):
        self.menu_bar = self.menuBar()

        file_menu = self.menu_bar.addMenu("File")
        settings_menu = self.menu_bar.addMenu("Settings")
        about_menu = self.menu_bar.addMenu("About")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+E")
        exit_action.triggered.connect(lambda: QApplication.Quit())

        file_menu.addAction(exit_action)

        return menu_bar

    def createCentralWidget(self):
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)

        return setCentralWidget(central_widget)

    def createIconButtonGrid(self, icon):
        button = QToolButton()
        button.setIcon(QtGui.QIcon(self.paths.generate_icon_path(icon)))

        return button
