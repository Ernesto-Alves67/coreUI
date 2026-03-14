"""
markdown_viewer.py — widget customizado leve para exibir textos em Markdown.

Usa ``QTextBrowser`` como base para renderizar o HTML gerado por
``MarkdownConverter``. Não depende de WebEngineView.

Exemplo de uso::

    viewer = MarkdownViewer()
    viewer.set_markdown("# Olá\\n\\nIsso é **negrito** e *itálico*.")
"""

from PySide6.QtWidgets import QTextBrowser, QSizePolicy

from .markdown_converter import MarkdownConverter, MarkdownRule


class MarkdownViewer(QTextBrowser):
    """
    Widget customizado leve para exibir textos em Markdown.

    Herda de ``QTextBrowser`` para renderizar HTML sem WebEngineView.
    O conversor interno (``self.converter``) pode ser acessado diretamente
    para adicionar regras personalizadas via ``add_rule()`` / ``insert_rule()``.

    Parâmetros
    ----------
    markdown_text:
        Texto Markdown opcional exibido na criação do widget.
    parent:
        Widget pai opcional.

    Exemplo::

        viewer = MarkdownViewer("# Título\\n\\nTexto com **negrito**.")
        layout.addWidget(viewer)
    """

    def __init__(self, markdown_text: str = "", parent=None):
        super().__init__(parent)
        self.converter = MarkdownConverter()
        self.setReadOnly(True)
        self.setOpenExternalLinks(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._apply_default_style()

        if markdown_text:
            self.set_markdown(markdown_text)

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def set_markdown(self, markdown_text: str) -> None:
        """Converte *markdown_text* e exibe o HTML resultante no widget."""
        html = self._build_full_html(self.converter.convert(markdown_text))
        self.setHtml(html)

    def get_markdown_html(self, markdown_text: str) -> str:
        """Retorna o HTML gerado a partir de *markdown_text* sem exibir."""
        return self.converter.convert(markdown_text)

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------

    def _apply_default_style(self) -> None:
        self.setStyleSheet(
            """
            QTextBrowser {
                background-color: #ffffff;
                color: #222222;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                padding: 8px;
                border: none;
            }
            """
        )

    def _build_full_html(self, body: str) -> str:
        """Envolve *body* em um documento HTML completo com estilos embutidos."""
        return (
            "<html><head><style>"
            "body { font-family: 'Segoe UI', Arial, sans-serif;"
            "       font-size: 14px; color: #222; }"
            "h1, h2, h3, h4, h5, h6 { margin-top: 0.6em; margin-bottom: 0.2em; }"
            "h1 { font-size: 2em; border-bottom: 2px solid #ddd;"
            "     padding-bottom: 4px; }"
            "h2 { font-size: 1.5em; border-bottom: 1px solid #eee;"
            "     padding-bottom: 2px; }"
            "h3 { font-size: 1.2em; }"
            "p  { margin: 0.4em 0; line-height: 1.6; }"
            "code { background: #f4f4f4; padding: 1px 4px; border-radius: 3px;"
            "       font-family: Consolas, 'Courier New', monospace;"
            "       font-size: 13px; }"
            "pre  { background: #f4f4f4; padding: 10px; border-radius: 4px;"
            "       font-family: Consolas, 'Courier New', monospace;"
            "       font-size: 13px; }"
            "blockquote { border-left: 4px solid #ccc; margin: 0.5em 0;"
            "             padding: 4px 12px; color: #555;"
            "             background: #fafafa; }"
            "ul, ol { padding-left: 1.5em; margin: 0.4em 0; }"
            "li     { margin: 0.2em 0; }"
            "hr     { border: none; border-top: 1px solid #ddd; margin: 1em 0; }"
            "a      { color: #0066cc; text-decoration: none; }"
            "a:hover { text-decoration: underline; }"
            "img    { max-width: 100%; }"
            "strong { font-weight: bold; }"
            "em     { font-style: italic; }"
            "</style></head>"
            f"<body>{body}</body></html>"
        )
