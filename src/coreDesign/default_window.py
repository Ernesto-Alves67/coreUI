import sys
import logging
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, QPoint, QEvent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DefaultWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgb(150, 150, 150);")
        self.setGeometry(100, 100, 600, 450)
        self.border_size = 5

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        self.title_bar = QWidget()
        self.title_bar.setObjectName("BarraDeTitulo")
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("background-color: #333; color: white;")
        self.title_bar.setMouseTracking(True)
        title_bar_layout = QHBoxLayout(self.title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(0)
        self.title_label = QLabel("Movimento e Redimensionamento Nativo")
        title_bar_layout.addWidget(self.title_label)
        title_bar_layout.addStretch()

        self.minimize_button = QPushButton("−");
        # self.minimize_button.setFixedSize(30, 25);
        self.minimize_button.setStyleSheet("background-color: #555; color: white; border: none; font-size: 16px;");
        self.minimize_button.clicked.connect(self.showMinimized);
        title_bar_layout.addWidget(self.minimize_button)
        self.maximize_button = QPushButton("□");
        self.maximize_button.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding));
        self.maximize_button.setContentsMargins(0, 0, 20, 0);
        # self.maximize_button.setFixedSize(30, 25);
        self.maximize_button.setStyleSheet("background-color: #555; color: white; border: none; font-size: 16px;");
        self.maximize_button.clicked.connect(self.toggle_maximize_restore);
        title_bar_layout.addWidget(self.maximize_button)
        self.close_button = QPushButton("X");
        # self.close_button.setFixedSize(30, 25);
        self.close_button.setStyleSheet("background-color: #f00; color: white; border: none; font-size: 16px;");
        self.close_button.clicked.connect(self.close);
        title_bar_layout.addWidget(self.close_button)
        title_bar_layout.setStretchFactor(self.title_label, 15)

        self.content_widget = QWidget()
        self.content_widget.setObjectName("mainContent")
        self.content_layout = None
        # self.content_layout = QVBoxLayout(self.content_widget)
        # self.content_layout.setContentsMargins(0, 0, 0, 0)
        # self.content_layout.setSpacing(0)

        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.content_widget)



        # # logging.info("Instalando event filter na BarraDeTitulo e AreaDeConteudo")
        self.title_bar.installEventFilter(self)
        self.content_widget.installEventFilter(self)
        self.installEventFilter(self)

    def update_title(self, new_title: str):
        """
        Atualiza o texto do título na barra de título.
        
        @param new_title: Novo texto para o título da janela.
        """
        self.title_label.setText(new_title)

    def set_content_layout(self, new_layout):
        """
        Substitui o layout do content_widget pelo novo_layout.
        """
        self.content_layout = new_layout
        current_layout = self.content_widget.layout()
        if current_layout is not None:
            current_layout.deleteLater()

        self.content_widget.setLayout(new_layout)

        new_layout.setContentsMargins(0, 0, 0, 0)
        new_layout.setSpacing(0)


    def toggle_maximize_restore(self):
        if self.isMaximized(): self.showNormal()
        else: self.showMaximized()
        
    def get_edge(self, pos: QPoint):
        rect = self.rect()
        left = pos.x() < self.border_size
        top = pos.y() < self.border_size
        right = pos.x() > rect.width() - self.border_size
        bottom = pos.y() > rect.height() - self.border_size

        # if top and left: return Qt.TopEdge | Qt.LeftEdge
        if top and right: return Qt.TopEdge | Qt.RightEdge
        if bottom and left: return Qt.BottomEdge | Qt.LeftEdge
        if bottom and right: return Qt.BottomEdge | Qt.RightEdge
        if left: return Qt.LeftEdge
        # if top: return Qt.TopEdge
        if right: return Qt.RightEdge
        if bottom: return Qt.BottomEdge
        return None

    def eventFilter(self, watched_object, event):
        obj_name = watched_object.objectName() or "QMainWindow"

        if event.type() == QEvent.Type.MouseMove:
            global_pos = event.globalPosition().toPoint()
            pos_na_janela = self.mapFromGlobal(global_pos)
            
            edge = self.get_edge(pos_na_janela)
            if edge:
                if edge == (Qt.TopEdge | Qt.LeftEdge) or edge == (Qt.BottomEdge | Qt.RightEdge): self.setCursor(Qt.SizeFDiagCursor)
                elif edge == (Qt.TopEdge | Qt.RightEdge) or edge == (Qt.BottomEdge | Qt.LeftEdge): self.setCursor(Qt.SizeBDiagCursor)
                elif edge == Qt.LeftEdge or edge == Qt.RightEdge: self.setCursor(Qt.SizeHorCursor)
                else: self.setCursor(Qt.SizeVerCursor)
            else:
                self.unsetCursor()

        elif event.type() == QEvent.Type.Leave:
            # logging.info(f"Mouse saiu do widget {obj_name}. Restaurando cursor.")
            self.unsetCursor()

        elif event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                global_pos = event.globalPosition().toPoint()
                pos_na_janela = self.mapFromGlobal(global_pos)
                edge = self.get_edge(pos_na_janela)

                if edge:
                    self.windowHandle().startSystemResize(edge)
                elif self.title_bar.rect().contains(self.title_bar.mapFromGlobal(global_pos)):
                    self.windowHandle().startSystemMove()

        return super().eventFilter(watched_object, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = DefaultWindow()
    janela.show()
    sys.exit(app.exec())