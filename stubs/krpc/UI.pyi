
class UI:
    class FontStyle:
        normal = 0
        bold = 1
        italic = 2
        bold_and_italic = 3
    
    class MessagePosition:
        bottom_center = 0
        top_center = 1
        top_left = 2
        top_right = 3
    
    class TextAlignment:
        left = 0
        right = 1
        center = 2
    
    class TextAnchor:
        lower_center = 0
        lower_left = 1
        lower_right = 2
        middle_center = 3
        middle_left = 4
        middle_right = 5
        upper_center = 6
        upper_left = 7
        upper_right = 8
    
    class Button:
        @property
        def rect_transform(self) -> UI.RectTransform: ...

        @property
        def text(self) -> UI.Text: ...

        @property
        def clicked(self) -> bool: ...

        @clicked.setter
        def clicked(self, this: UI.Button, value: bool): ...

        @property
        def visible(self) -> bool: ...

        @visible.setter
        def visible(self, this: UI.Button, value: bool): ...

        def remove(self): ...

    
    class Canvas:
        @property
        def rect_transform(self) -> UI.RectTransform: ...

        @property
        def visible(self) -> bool: ...

        @visible.setter
        def visible(self, this: UI.Canvas, value: bool): ...

        def add_panel(self, visible: bool = True) -> UI.Panel: ...

        def add_text(self, content: str, visible: bool = True) -> UI.Text: ...

        def add_input_field(self, visible: bool = True) -> UI.InputField: ...

        def add_button(self, content: str, visible: bool = True) -> UI.Button: ...

        def remove(self): ...

    
    class InputField:
        @property
        def rect_transform(self) -> UI.RectTransform: ...

        @property
        def value(self) -> str: ...

        @value.setter
        def value(self, this: UI.InputField, value: str): ...

        @property
        def text(self) -> UI.Text: ...

        @property
        def changed(self) -> bool: ...

        @changed.setter
        def changed(self, this: UI.InputField, value: bool): ...

        @property
        def visible(self) -> bool: ...

        @visible.setter
        def visible(self, this: UI.InputField, value: bool): ...

        def remove(self): ...

    
    class Panel:
        @property
        def rect_transform(self) -> UI.RectTransform: ...

        @property
        def visible(self) -> bool: ...

        @visible.setter
        def visible(self, this: UI.Panel, value: bool): ...

        def add_panel(self, visible: bool = True) -> UI.Panel: ...

        def add_text(self, content: str, visible: bool = True) -> UI.Text: ...

        def add_input_field(self, visible: bool = True) -> UI.InputField: ...

        def add_button(self, content: str, visible: bool = True) -> UI.Button: ...

        def remove(self): ...

    
    class RectTransform:
        @property
        def position(self) -> tuple[float, float]: ...

        @position.setter
        def position(self, this: UI.RectTransform, value: tuple[float, float]): ...

        @property
        def local_position(self) -> tuple[float, float, float]: ...

        @local_position.setter
        def local_position(self, this: UI.RectTransform, value: tuple[float, float, float]): ...

        @property
        def size(self) -> tuple[float, float]: ...

        @size.setter
        def size(self, this: UI.RectTransform, value: tuple[float, float]): ...

        @property
        def upper_right(self) -> tuple[float, float]: ...

        @upper_right.setter
        def upper_right(self, this: UI.RectTransform, value: tuple[float, float]): ...

        @property
        def lower_left(self) -> tuple[float, float]: ...

        @lower_left.setter
        def lower_left(self, this: UI.RectTransform, value: tuple[float, float]): ...

        def anchor(self, this: UI.RectTransform, value: tuple[float, float]): ...
        anchor = property(None, anchor)

        @property
        def anchor_max(self) -> tuple[float, float]: ...

        @anchor_max.setter
        def anchor_max(self, this: UI.RectTransform, value: tuple[float, float]): ...

        @property
        def anchor_min(self) -> tuple[float, float]: ...

        @anchor_min.setter
        def anchor_min(self, this: UI.RectTransform, value: tuple[float, float]): ...

        @property
        def pivot(self) -> tuple[float, float]: ...

        @pivot.setter
        def pivot(self, this: UI.RectTransform, value: tuple[float, float]): ...

        @property
        def rotation(self) -> tuple[float, float, float, float]: ...

        @rotation.setter
        def rotation(self, this: UI.RectTransform, value: tuple[float, float, float, float]): ...

        @property
        def scale(self) -> tuple[float, float, float]: ...

        @scale.setter
        def scale(self, this: UI.RectTransform, value: tuple[float, float, float]): ...

    
    class Text:
        @property
        def rect_transform(self) -> UI.RectTransform: ...

        @property
        def available_fonts(self) -> list[str]: ...

        @property
        def content(self) -> str: ...

        @content.setter
        def content(self, this: UI.Text, value: str): ...

        @property
        def font(self) -> str: ...

        @font.setter
        def font(self, this: UI.Text, value: str): ...

        @property
        def size(self) -> int: ...

        @size.setter
        def size(self, this: UI.Text, value: int): ...

        @property
        def style(self) -> UI.FontStyle: ...

        @style.setter
        def style(self, this: UI.Text, value: UI.FontStyle): ...

        @property
        def alignment(self) -> UI.TextAnchor: ...

        @alignment.setter
        def alignment(self, this: UI.Text, value: UI.TextAnchor): ...

        @property
        def line_spacing(self) -> float: ...

        @line_spacing.setter
        def line_spacing(self, this: UI.Text, value: float): ...

        @property
        def color(self) -> tuple[float, float, float]: ...

        @color.setter
        def color(self, this: UI.Text, value: tuple[float, float, float]): ...

        @property
        def visible(self) -> bool: ...

        @visible.setter
        def visible(self, this: UI.Text, value: bool): ...

        def remove(self): ...

    
    @property
    def stock_canvas(self) -> UI.Canvas: ...

    def add_canvas(self) -> UI.Canvas: ...

    def message(self, content: str, duration: float = 1, position: UI.MessagePosition = 2, color: tuple[float, float, float] = (1, 0.92, 0.016), size: float = 20): ...

    def clear(self, client_only: bool = False): ...


