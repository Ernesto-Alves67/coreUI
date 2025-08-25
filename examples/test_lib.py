from PySide6.QtWidgets import(
     QTextEdit, QTabWidget, 
     QApplication, QLabel,
     QHBoxLayout, QVBoxLayout, QWidget, QLabel,
     QTextEdit, QTabWidget, QTableWidget,
     QTableWidgetItem, QHeaderView
)
from coreDesign.default_window import DefaultWindow
import sys


def create_table_tab():
    """Cria e retorna um QWidget com um QTableWidget dentro."""
    table_widget = QTableWidget()
    
    # Define o número de linhas e colunas
    table_widget.setColumnCount(3)
    table_widget.setRowCount(4)
    
    # Define os cabeçalhos da tabela
    table_widget.setHorizontalHeaderLabels(["ID", "Produto", "Preço"])
    
    # Dados de exemplo
    data = [
        ("001", "Caneta", "R$ 2,50"),
        ("002", "Caderno", "R$ 15,00"),
        ("003", "Borracha", "R$ 1,25"),
        ("004", "Lápis", "R$ 1,00")
    ]
    
    # Preenche a tabela com os dados
    for row_idx, row_data in enumerate(data):
        for col_idx, item_data in enumerate(row_data):
            item = QTableWidgetItem(item_data)
            table_widget.setItem(row_idx, col_idx, item)
            
    # Ajusta o redimensionamento das colunas para preencher o espaço
    header = table_widget.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.Stretch)
    
    # Cria um widget container para a tabela e retorna
    table_container = QWidget()
    table_layout = QVBoxLayout(table_container)
    table_layout.addWidget(table_widget)
    
    return table_container

class TextEditorExample(DefaultWindow):
    def __init__(self):
        super().__init__()
        
        # Mude o título da janela
        self.update_title("Editor de Texto e Tabela")
        
        # Crie o widget de abas
        self.tab_container = QTabWidget()
        self.tab_container.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.tab_container.setMaximumHeight(150)
        
        # Crie os conteúdos para cada aba
        editor_tab = QWidget()
        editor_layout = QVBoxLayout(editor_tab)
        self.text_editor = QTextEdit()
        editor_layout.addWidget(self.text_editor)
        
        table_tab = create_table_tab()
        
        # Outras abas com conteúdo simples de exemplo
        placeholder_tab_2 = QWidget()
        placeholder_layout_2 = QVBoxLayout(placeholder_tab_2)
        placeholder_layout_2.addWidget(QLabel("Conteúdo da Aba 3"))

        placeholder_tab_3 = QWidget()
        placeholder_layout_3 = QVBoxLayout(placeholder_tab_3)
        placeholder_layout_3.addWidget(QLabel("Conteúdo da Aba 4"))
        
        placeholder_tab_4 = QWidget()
        placeholder_layout_4 = QVBoxLayout(placeholder_tab_4)
        placeholder_layout_4.addWidget(QLabel("Conteúdo da Aba 5"))
        
        # Adicione os widgets como abas
        self.tab_container.addTab(editor_tab, "Editor de Texto")
        self.tab_container.addTab(table_tab, "Tabela de Dados")
        self.tab_container.addTab(placeholder_tab_2, "Aba 3")
        self.tab_container.addTab(placeholder_tab_3, "Aba 4")
        self.tab_container.addTab(placeholder_tab_4, "Aba 5")
        
        content_widget = QWidget()
        content_widget.setObjectName("AreaDeConteudo")
        content_widget.setStyleSheet("background-color: red;")
        content_widget.setMouseTracking(True)

        self.content_layout.addWidget(content_widget)
        self.content_layout.addWidget(self.tab_container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela_editor = TextEditorExample()
    janela_editor.show()
    sys.exit(app.exec())