import sys
import scanner
from scanner import Scanner
from Parser import Parser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QDockWidget, QMenu, QMenuBar, QAction,
                             QFileDialog, QVBoxLayout, QWidget, QPlainTextEdit, QLabel, QTableWidget, QTableWidgetItem,
                             QTabWidget)
from PyQt5.QtGui import QFont
# from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window
        self.setWindowTitle('Analizador - 202111576')
        self.setGeometry(100, 100, 1200, 800)

        # Apply the custom style sheet
        self.init_style_sheet()

        # Add widgets and additional UI settings
        self.init_ui()

    def init_style_sheet(self):
        style_sheet = """
        QMainWindow {
            background-color: #3a3a3a;
        }
        QPlainTextEdit, QTextEdit {
            background-color: #232629;
            color: #e6e6e6;
            border: 1px solid #76797c;
            border-radius: 2px;
        }
        QTableWidget {
            background-color: #232629;
            color: #e6e6e6;
            border: 1px solid #76797c;
            border-radius: 2px;
            gridline-color: #5b5e6d;
            alternate-background-color: #31363b;
        }
        QHeaderView::section {
            background-color: #31363b;
            color: #e6e6e6;
            padding: 5px;
            border: 1px solid #76797c;
        }
        QMenuBar {
            background-color: #31363b;
            color: #e6e6e6;
        }
        QMenuBar::item:selected {
            background-color: #3daee9;
            color: #e6e6e6;
        }
        QMenu {
            background-color: #31363b;
            color: #e6e6e6;
            border: 1px solid #76797c;
        }
        QMenu::item:selected {
            background-color: #3daee9;
            color: #e6e6e6;
        }
        QTabWidget::pane {
            border: 1px solid #76797c;
            border-radius: 2px;
        }
        QTabBar::tab {
            background-color: #31363b;
            color: #e6e6e6;
            padding: 5px;
            border: 1px solid #76797c;
            border-bottom-color: #31363b;
            border-top-left-radius: 2px;
            border-top-right-radius: 2px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: #3daee9;
            color: #e6e6e6;
        }
        """
        self.setStyleSheet(style_sheet)

    def init_ui(self):
        self.tabs = QTabWidget()

        # Code editor
        self.code_editor = QPlainTextEdit(self)
        self.code_editor.setFont(QFont("Courier", 12))

        # Sentences viewer
        self.sentences_viewer = QTextEdit(self)
        self.sentences_viewer.setReadOnly(True)

        # Tokens table
        self.tokens_table = QTableWidget(self)
        self.tokens_table.setColumnCount(4)
        self.tokens_table.setHorizontalHeaderLabels(['No.', 'Tipo', 'Linea', 'Lexema'])

        # Errors table
        self.errors_table = QTableWidget(self)
        self.errors_table.setColumnCount(5)
        self.errors_table.setHorizontalHeaderLabels(['Tipe', 'Linea', 'Columna', 'Token', 'Descripcion'])

        # Add tabs
        self.tabs.addTab(self.code_editor, "Codigo")
        self.tabs.addTab(self.tokens_table, "Tokens")
        self.tabs.addTab(self.errors_table, "Errores")
        self.tabs.addTab(self.sentences_viewer, "Senencias Generadas BD")

        self.setCentralWidget(self.tabs)

        # Menu
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("Archivo")
        self.analysis_menu = self.menu_bar.addMenu("Analizar")
        self.view_menu = self.menu_bar.addMenu("Ver")

        # File menu actions
        self.new_action = QAction("Nuevo", self)
        self.open_action = QAction("Abrir", self)
        self.save_action = QAction("Guardar", self)
        self.save_as_action = QAction("Guardar Como", self)
        self.exit_action = QAction("Salir", self)

        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        # Analysis menu actions
        self.analyze_action = QAction("Generar Sentencias MongoDb", self)
        self.analysis_menu.addAction(self.analyze_action)

        # Connect actions to functions
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.save_as_action.triggered.connect(self.save_file_as)
        self.new_action.triggered.connect(self.new_file)
        self.exit_action.triggered.connect(self.close)
        self.analyze_action.triggered.connect(self.analyze_code)

    def new_file(self):
        if self.code_editor.document().isModified():
            pass 

        self.code_editor.clear()

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.code_editor.setPlainText(file.read())

    def save_file(self):
        if not self.code_editor.document().isModified():
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.code_editor.toPlainText())

    def save_file_as(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo como", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.code_editor.toPlainText())

    def analyze_code(self):
        input_str = self.code_editor.toPlainText()
        scanner_instance = scanner.Scanner(input_str)
        tokens = scanner_instance.tokenize()  # Obtener los tokens
        parser = Parser(tokens)  # Crear una instancia del analizador con los tokens

        try:
            result = parser.parse()
            print(result)

            mongodb_statements = []
            for stmt in result:
                if stmt[0] == "CREATE_DB":
                    mongodb_statements.append("use " + stmt[1])
                    print("CREATE_DB:", stmt[1])
                elif stmt[0] == "DROP_DB":
                    mongodb_statements.append("db.dropDatabase()")
                    print("DROP_DB")
                elif stmt[0] == "CREATE_COLLECTION":
                    mongodb_statements.append(f"db.createCollection('{stmt[1]}')")
                    print("CREATE_COLLECTION:", stmt[1])
                elif stmt[0] == "DROP_COLLECTION":
                    mongodb_statements.append(f"db.{stmt[1]}.drop()")
                elif stmt[0] == "INSERT_ONE":
                    mongodb_statements.append(f"db.{stmt[1]}.insertOne({stmt[2]})")
                elif stmt[0] == "UPDATE_ONE":
                    mongodb_statements.append(f"db.{stmt[1]}.updateOne({stmt[2]}, {stmt[3]})")
                elif stmt[0] == "DELETE_ONE":
                    mongodb_statements.append(f"db.{stmt[1]}.deleteOne({stmt[2]})")
                elif stmt[0] == "FIND_ALL":
                    mongodb_statements.append(f"db.{stmt[1]}.find()")
                elif stmt[0] == "FIND_ONE":
                    mongodb_statements.append(f"db.{stmt[1]}.findOne()")

            self.sentences_viewer.setPlainText("\n".join(mongodb_statements))
            self.show_tokens(parser.tokens)
            self.tokens_table.update()
        except Exception as e:
            self.update_error_table(f"Error inesperado: {str(e)}")
            self.errors_table.update()
        print("Result:", result)

    def update_error_table(self, error_msg):
        self.errors_table.setRowCount(1)
        self.errors_table.setItem(0, 0, QTableWidgetItem("Error"))
        self.errors_table.setItem(0, 1, QTableWidgetItem("-"))
        self.errors_table.setItem(0, 2, QTableWidgetItem("-"))
        self.errors_table.setItem(0, 3, QTableWidgetItem("-"))
        self.errors_table.setItem(0, 4, QTableWidgetItem(error_msg))

    def show_tokens(self, tokens):
        scanner = Scanner(self.code_editor.toPlainText())
        tokens = scanner.tokenize()
        print("Tokens:", tokens)  # Imprime la variable tokens aquí para ver su valor
        
        if isinstance(tokens, list):
            self.tokens_table.setRowCount(len(tokens))
            for i, token in enumerate(tokens):
                self.tokens_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.tokens_table.setItem(i, 1, QTableWidgetItem(token[0]))
                self.tokens_table.setItem(i, 2, QTableWidgetItem(str(token[2])))
                self.tokens_table.setItem(i, 3, QTableWidgetItem(token[1]))
        else:
            print("Error: tokens no es una lista")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())