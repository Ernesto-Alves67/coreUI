"""
markdown_converter.py — conversor Markdown → HTML puro (sem dependências Qt).

Suporta as principais tags Markdown:
    - Títulos: # H1 até ###### H6
    - Negrito: **texto** ou __texto__
    - Itálico: *texto* ou _texto_
    - Negrito + Itálico: ***texto***
    - Código inline: `código`
    - Blocos de código: ```...```
    - Listas não-ordenadas: - item  /  * item  /  + item
    - Listas ordenadas: 1. item
    - Citações (blockquote): > texto
    - Links: [texto](url)
    - Imagens: ![alt](url)
    - Régua horizontal: --- / *** / ___
    - Parágrafos (linhas separadas por linha em branco)
"""

import re


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def _escape_html(text: str) -> str:
    """Escapa caracteres especiais HTML."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


# ---------------------------------------------------------------------------
# Regra de conversão
# ---------------------------------------------------------------------------

class MarkdownRule:
    """
    Encapsula uma regra de substituição de Markdown → HTML.

    Parâmetros
    ----------
    pattern:
        Expressão regular a ser buscada no texto.
    replacement:
        String de substituição (com grupos de captura ``\\1``, etc.) ou
        callable ``(re.Match) -> str``.
    flags:
        Flags do módulo ``re`` (ex.: ``re.MULTILINE``).
    """

    def __init__(self, pattern: str, replacement, flags: int = 0):
        self.regex = re.compile(pattern, flags)
        self.replacement = replacement

    def apply(self, text: str) -> str:
        if callable(self.replacement):
            return self.regex.sub(self.replacement, text)
        return self.regex.sub(self.replacement, text)


# ---------------------------------------------------------------------------
# Constantes de expressões regulares pré-compiladas
# ---------------------------------------------------------------------------

_RE_UL_ITEM = re.compile(r"^[-*+] (.+)$")
_RE_OL_ITEM = re.compile(r"^\d+\. (.+)$")
_RE_PARA_SPLIT = re.compile(r"\n{2,}")
_RE_BLOCK_TAG = re.compile(
    r"^<(h[1-6]|ul|ol|li|blockquote|pre|hr|p)", re.IGNORECASE
)


# ---------------------------------------------------------------------------
# Funções auxiliares de conversão
# ---------------------------------------------------------------------------
def _convert_lists(text: str) -> str:
    """Converte listas Markdown em tags HTML ``<ul>``/``<ol>``."""
    lines = text.split("\n")
    result = []
    in_ul = False
    in_ol = False

    for line in lines:
        ul_match = _RE_UL_ITEM.match(line)
        ol_match = _RE_OL_ITEM.match(line)

        if ul_match:
            if in_ol:
                result.append("</ol>")
                in_ol = False
            if not in_ul:
                result.append("<ul>")
                in_ul = True
            result.append(f"<li>{ul_match.group(1)}</li>")
        elif ol_match:
            if in_ul:
                result.append("</ul>")
                in_ul = False
            if not in_ol:
                result.append("<ol>")
                in_ol = True
            result.append(f"<li>{ol_match.group(1)}</li>")
        else:
            if in_ul:
                result.append("</ul>")
                in_ul = False
            if in_ol:
                result.append("</ol>")
                in_ol = False
            result.append(line)

    if in_ul:
        result.append("</ul>")
    if in_ol:
        result.append("</ol>")

    return "\n".join(result)


def _convert_paragraphs(text: str) -> str:
    """Envolve blocos de texto simples em tags ``<p>``."""
    blocks = _RE_PARA_SPLIT.split(text)
    wrapped = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if _RE_BLOCK_TAG.match(block):
            wrapped.append(block)
        else:
            block = block.replace("\n", "<br/>\n")
            wrapped.append(f"<p>{block}</p>")
    return "\n".join(wrapped)


def _build_default_rules() -> list:
    """Retorna a lista padrão de regras inline (exceto blocos de código)."""
    rules = []

    # Títulos H1–H6 (do maior para o menor, para evitar ambiguidade)
    for level in range(6, 0, -1):
        hashes = "#" * level
        rules.append(MarkdownRule(
            rf"^{hashes} (.+)$",
            rf"<h{level}>\1</h{level}>",
            flags=re.MULTILINE,
        ))

    # Régua horizontal: ---, ***, ___
    rules.append(MarkdownRule(
        r"^([-*_]){3,}\s*$",
        "<hr/>",
        flags=re.MULTILINE,
    ))

    # Citações (blockquote) — linhas que começam com &gt; (já escapado)
    rules.append(MarkdownRule(
        r"^&gt;\s?(.*)$",
        r"<blockquote>\1</blockquote>",
        flags=re.MULTILINE,
    ))

    # Negrito + itálico: ***texto***
    rules.append(MarkdownRule(
        r"\*\*\*(.+?)\*\*\*",
        r"<strong><em>\1</em></strong>",
    ))

    # Negrito: **texto** ou __texto__
    rules.append(MarkdownRule(r"\*\*(.+?)\*\*", r"<strong>\1</strong>"))
    rules.append(MarkdownRule(r"__(.+?)__", r"<strong>\1</strong>"))

    # Itálico: *texto* ou _texto_
    rules.append(MarkdownRule(r"\*(.+?)\*", r"<em>\1</em>"))
    rules.append(MarkdownRule(r"_(.+?)_", r"<em>\1</em>"))

    # Código inline: `código`
    # O texto já foi HTML-escapado antes da aplicação das regras,
    # portanto não é necessário escapar novamente aqui.
    rules.append(MarkdownRule(r"`(.+?)`", r"<code>\1</code>"))

    # Imagens: ![alt](url)  — deve vir antes dos links
    rules.append(MarkdownRule(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        r'<img src="\2" alt="\1"/>',
    ))

    # Links: [texto](url)
    rules.append(MarkdownRule(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
    ))

    return rules


# ---------------------------------------------------------------------------
# Conversor principal
# ---------------------------------------------------------------------------

class MarkdownConverter:
    """
    Converte texto Markdown em HTML.

    O conversor pode ser estendido adicionando ou inserindo novas
    ``MarkdownRule`` via ``add_rule()`` e ``insert_rule()``.

    Exemplo::

        converter = MarkdownConverter()
        html = converter.convert("# Título\\n\\nParágrafo com **negrito**.")
    """

    def __init__(self):
        self._rules: list = _build_default_rules()

    # ------------------------------------------------------------------
    # API pública para extensão
    # ------------------------------------------------------------------

    def add_rule(self, rule: MarkdownRule) -> None:
        """Adiciona uma regra de conversão ao final da lista."""
        self._rules.append(rule)

    def insert_rule(self, index: int, rule: MarkdownRule) -> None:
        """Insere uma regra de conversão em uma posição específica."""
        self._rules.insert(index, rule)

    # ------------------------------------------------------------------
    # Conversão
    # ------------------------------------------------------------------

    def convert(self, markdown_text: str) -> str:
        """Converte *markdown_text* em uma string HTML."""
        # 1. Extrai e guarda blocos de código (preserva conteúdo interno)
        code_blocks: dict = {}
        counter = [0]

        def _stash_code_block(m: re.Match) -> str:
            key = f"\x00CODEBLOCK{counter[0]}\x00"
            lang = m.group(1) or ""
            body = _escape_html(m.group(2))
            tag = f' class="language-{lang}"' if lang else ""
            code_blocks[key] = f"<pre><code{tag}>{body}</code></pre>"
            counter[0] += 1
            return key

        text = re.sub(
            r"```(\w*)\n(.*?)```",
            _stash_code_block,
            markdown_text,
            flags=re.DOTALL,
        )

        # 2. Escapa HTML no texto restante
        text = _escape_html(text)

        # 3. Converte listas (antes das regras inline para preservar hifens)
        text = _convert_lists(text)

        # 4. Aplica regras inline
        for rule in self._rules:
            text = rule.apply(text)

        # 5. Restaura blocos de código
        for key, html in code_blocks.items():
            text = text.replace(key, html)

        # 6. Envolve blocos soltos em <p>
        text = _convert_paragraphs(text)

        return text
