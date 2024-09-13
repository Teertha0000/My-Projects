import math
import flet as ft


def main(page: ft.Page):
    page.title = "Calculator"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Set the initial window size
    page.window_width = 400  # Increased window width
    page.window_height = 660  # Increased window height

    expression_display = ft.Text(value="", text_align=ft.TextAlign.RIGHT, width=30060, size=20, selectable=True)
    textbox = ft.Text(value="0", text_align=ft.TextAlign.RIGHT, width=50060, size=40, weight=ft.FontWeight.BOLD,
                      selectable=True, max_lines=1)

    def adjust_text_size(text):
        max_length = 15  # Adjust this value based on your preference
        if len(text) > max_length:
            textbox.size = 40 - (len(text) - max_length) * 1.5  # Decrease size by 2 for each extra character
            if textbox.size < 10:  # Ensure the text size doesn't get too small
                textbox.size = 10
        else:
            textbox.size = 40  # Reset to the original size if the text is short enough
        page.update()

    def validate_input(e):
        if e.data and not (e.data.isdigit() or e.data == "."):
            textbox.value = textbox.value[:-1]
        adjust_text_size(textbox.value)
        page.update()

    textbox.on_change = validate_input

    def button_click(e):
        global result
        if "=" in expression_display.value:
            expression_display.value = ""
        if e.control.data == "C":
            textbox.value = "0"
            expression_display.value = ""
        elif e.control.data == "=":
            try:
                expression_display.value += textbox.value
                # Replace Unicode characters with Python operators before evaluating
                eval_expression = expression_display.value.replace(u"\u00F7", "/").replace(u"\u00D7", "*").replace("^",
                                                                                                                   "**")
                result = str(eval(eval_expression))
                # Remove trailing .0 if present
                if result.endswith('.0'):
                    result = result[:-2]
                textbox.value = result
                expression_display.value = f"{expression_display.value}="
            except SyntaxError:
                textbox.value = "Invalid Expression"
            except ZeroDivisionError:
                textbox.value = "Can Not Divide by Zero"
            except OSError:
                textbox.value = "Error"
        elif e.control.data == "%":
            try:
                value = float(textbox.value)
                result = str(value / 100)
                # Remove trailing .0 if present
                if result.endswith('.0'):
                    result = result[:-2]
                textbox.value = result
            except ValueError:
                textbox.value = "Error"
        elif e.control.data in ["sin", "cos", "tan", "sec", "csc", "cot"]:
            try:
                value = float(textbox.value)
                if e.control.data == "sin":
                    expression_display.value = f"sin({textbox.value})="
                    result = math.sin(math.radians(value))
                elif e.control.data == "cos":
                    expression_display.value = f"cos({textbox.value})="
                    result = math.cos(math.radians(value))
                elif e.control.data == "tan":
                    expression_display.value = f"tan({textbox.value})="
                    result = math.tan(math.radians(value))
                elif e.control.data == "sec":
                    expression_display.value = f"sec({textbox.value})="
                    result = 1 / math.cos(math.radians(value))
                elif e.control.data == "csc":
                    expression_display.value = f"csc({textbox.value})="
                    result = 1 / math.sin(math.radians(value))
                elif e.control.data == "cot":
                    expression_display.value = f"cot({textbox.value})="
                    result = 1 / math.tan(math.radians(value))
                result_str = str(result)
                # Remove trailing .0 if present
                if result_str.endswith('.0'):
                    result_str = result_str[:-2]
                textbox.value = result_str
            except:
                textbox.value = "Error"
        elif e.control.data == u"\u00AB":
            textbox.value = textbox.value[:-1]
        elif e.control.data == "+/-":
            if "-" in textbox.value[0]:
                textbox.value = f'{textbox.value.replace("-", "")}'
            else:
                textbox.value = f'-{textbox.value}'
        elif e.control.data in ["+", "-", u"\u00F7", u"\u00D7"]:
            if expression_display.value == "":
                expression_display.value = textbox.value + e.control.data
            else:
                expression_display.value += textbox.value + e.control.data
            textbox.value = " " + str(
                eval(expression_display.value[:-1].replace(u"\u00F7", "/").replace(u"\u00D7", "*")))
        elif e.control.data == "x²":
            try:
                value = float(textbox.value)
                expression_display.value = f"({textbox.value})²="
                result = str(value ** 2)
                # Remove trailing .0 if present
                if result.endswith('.0'):
                    result = result[:-2]
                textbox.value = result
            except ValueError:
                textbox.value = "Error"
        elif e.control.data == "xʸ":
            expression_display.value += textbox.value + "^"
            textbox.value = ""
        elif e.control.data == "10ˣ":
            try:
                value = float(textbox.value)
                expression_display.value = f"10^{textbox.value}="
                result = str(10 ** value)
                # Remove trailing .0 if present
                if result.endswith('.0'):
                    result = result[:-2]
                textbox.value = result
            except ValueError:
                textbox.value = "Error"
        elif e.control.data == "²√x":
            try:
                value = float(textbox.value)
                expression_display.value = f"√({textbox.value})="
                result = str(math.sqrt(value))
                # Remove trailing .0 if present
                if result.endswith('.0'):
                    result = result[:-2]
                textbox.value = result
            except ValueError:
                textbox.value = "Error"
        elif e.control.data == "1/x":
            try:
                expression_display.value = f"1/({textbox.value})="
                value = float(textbox.value)
                result = str(1 / value)
                # Remove trailing .0 if present
                if result.endswith('.0'):
                    result = result[:-2]
                textbox.value = result
            except ZeroDivisionError:
                textbox.value = "Can Not Divide by Zero"
            except ValueError:
                textbox.value = "Error"
        elif e.control.data == "π":
            textbox.value = str(math.pi)
        else:
            if textbox.value == "0" or " " in textbox.value:
                textbox.value = e.control.data
            else:
                textbox.value = textbox.value + e.control.data
        adjust_text_size(textbox.value)
        page.update()

    menubar = ft.MenuBar(
        style=ft.MenuStyle(
            alignment=ft.alignment.top_center,
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("◿" + "  Trigonometry"),
                # leading=ft.Icon(ft.icons.CALCULATE_ROUNDED),
                controls=[

                    ft.MenuItemButton(
                        content=ft.Text("        sin         ", size=16),
                        data="sin",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("        cos         ", size=16),
                        data="cos",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("        tan         ", size=16),
                        data="tan",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("        sec         ", size=16),
                        data="sec",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("        csc         ", size=16),
                        data="csc",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("        cot         ", size=16),
                        data="cot",
                        on_click=button_click,
                    ),

                ],
            ),

            ft.SubmenuButton(
                content=ft.Text("    ···"),
                # leading=ft.Icon(ft.icons.CALCULATE_ROUNDED),
                controls=[

                    ft.MenuItemButton(
                        content=ft.Text("   x²", size=16),
                        data="x²",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("   xʸ", size=16),
                        data="xʸ",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("  10ˣ", size=16),
                        data="10ˣ",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text(" ²√x", size=16),
                        data="²√x",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text(" 1/x", size=16),
                        data="1/x",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("   π", size=16),
                        data="π",
                        on_click=button_click,
                    ),

                ],
            ),
        ],
    )

    additional_menubar = ft.MenuBar(
        style=ft.MenuStyle(
            alignment=ft.alignment.top_center,
        ),
        controls=[
            ft.SubmenuButton(
                # content=ft.Text("Additional Functions"),
                leading=ft.Icon(ft.icons.FUNCTIONS),
                controls=[

                    ft.MenuItemButton(
                        content=ft.Text("x²", size=16),
                        data="x²",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("xʸ", size=16),
                        data="xʸ",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("10ˣ", size=16),
                        data="10ˣ",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("²√x", size=16),
                        data="²√x",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("1/x", size=16),
                        data="1/x",
                        on_click=button_click,
                    ),

                    ft.MenuItemButton(
                        content=ft.Text("π", size=16),
                        data="π",
                        on_click=button_click,
                    ),

                ],
            ),
        ],
    )

    buttons = [
        ["%", "C", u"\u00AB", u"\u00F7"],  # Unicode for division
        ["7", "8", "9", u"\u00D7"],  # Unicode for multiplication
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["+/-", "0", ".", "="],
    ]

    button_row = []
    for row in buttons:
        button_col = []
        for label in row:
            if label in "0123456789":
                color = ft.colors.BLUE_200  # Light blue for number buttons
            else:
                color = ""  # Darker blue for operation buttons
            button_col.append(
                ft.FloatingActionButton(text=label, data=label, on_click=button_click, bgcolor=color, expand=True,
                                        width=80, height=80))
        button_row.append(ft.Row(button_col, alignment=ft.MainAxisAlignment.CENTER))

    page.add(
        ft.Column(
            [
                ft.Column([expression_display], alignment=ft.MainAxisAlignment.CENTER),  # Expression display
                ft.Container(content=textbox, clip_behavior=ft.ClipBehavior.ANTI_ALIAS),
                # Center the input box and make it copyable
                ft.Column([menubar], alignment=ft.MainAxisAlignment.CENTER),  # Center the input box,
                ft.Column(button_row, alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


ft.app(target=main)
