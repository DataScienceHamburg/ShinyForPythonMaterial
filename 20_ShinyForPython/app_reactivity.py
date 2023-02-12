from shiny import App, render, ui, reactive

app_ui = ui.page_fluid(
    ui.h2("Reactivity"),
    ui.input_slider("n", "N", 0, 100, 20),
    ui.output_text_verbatim("result1"),
    ui.output_text_verbatim("result2"),
)


def server(input, output, session):
    
    @reactive.Calc
    def reactive_result():
        return f"n*2 is {input.n() * 2}"
       
    @output
    @render.text
    def result1():
        return reactive_result()
    
    @output
    @render.text
    def result2():
        return reactive_result()


app = App(app_ui, server)
