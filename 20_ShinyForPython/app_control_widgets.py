from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.h2("Input Widgets"),
    # ui.input_slider(id="n", label="N", min=0, max=100, value=[20, 30], animate=True),
    # ui.input_checkbox(id = "check", label="Check", value=True),
    # ui.input_numeric(id = "num", label="Num", min=10, max=30, value=25, step=5),
    # ui.input_password(id='inp_pw', label='Txt Input'),
    # ui.input_checkbox_group(id='chk_grp', label='Checkbox Group', choices=['Choice1', 'Choice2'], selected='Choice1'),
    # ui.input_radio_buttons(id='chk_grp', label='Radio Button Group', choices=['Choice1', 'Choice2'], selected='Choice1'),
    ui.input_date_range(id='date', label='Date'),
    ui.h2("Output Widgets"),
    ui.output_text_verbatim("txt"),
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"{input.chk_grp()}"


app = App(app_ui, server)
