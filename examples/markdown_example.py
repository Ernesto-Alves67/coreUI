"""
Exemplo de uso do MarkdownViewer — widget customizado leve para exibir
textos em Markdown sem WebEngineView.

Execute diretamente:
    python examples/markdown_example.py
"""

import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from coreDesign.markdown_viewer import MarkdownViewer
from coreDesign.markdown_converter import MarkdownConverter, MarkdownRule
from coreDesign.default_window import DefaultWindow


SAMPLE_MARKDOWN = """# Bem-vindo ao MarkdownViewer

Este é um widget **customizado** e *leve* para exibir Markdown em aplicações
PySide6, sem a necessidade de WebEngineView.

## Funcionalidades suportadas

### Formatação de texto

- **Negrito** com `**texto**` ou `__texto__`
- *Itálico* com `*texto*` ou `_texto_`
- ***Negrito e itálico*** com `***texto***`
- `código inline` com crases

### Listas

Lista não-ordenada:
- Item A
- Item B
- Item C

Lista ordenada:
1. Primeiro
2. Segundo
3. Terceiro

### Links e imagens

[Visite o GitHub](https://github.com/Ernesto-Alves67/coreUI)

### Citações

> "Simplicidade é o máximo da sofisticação."
> — Leonardo da Vinci

### Bloco de código

```python
def saudacao(nome: str) -> str:
    return f"Olá, {nome}!"

print(saudacao("Mundo"))
```

### Régua horizontal

---

### Títulos de H1 a H6

# H1
## H2
### H3
#### H4
##### H5
###### H6
"""


class MarkdownExampleWindow(DefaultWindow):
    def __init__(self):
        super().__init__()
        self.update_title("MarkdownViewer — Exemplo")
        self.resize(800, 600)

        layout = QVBoxLayout()
        self.set_content_layout(layout)

        self.viewer = MarkdownViewer(SAMPLE_MARKDOWN)
        layout.addWidget(self.viewer)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkdownExampleWindow()
    window.show()
    sys.exit(app.exec())
