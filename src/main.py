import flet
from automator import *
from myutil import *

data = None

def main(page: flet.Page):
    page.title = "SATP - David Mota"

    def on_start_button(link: str):

        global data

        UtilHolder.out_messages.clear()

        output_column.controls.append(flet.Text("Starting the process..."))
        data = process_form_responses(link)

        for index, group in enumerate(data):
            data_control.controls.append(flet.ExpansionPanel(
                header = flet.Text(f'Grupo {index + 1}'),
                content = flet.Text('\n'.join([key for key, value in group.items()])),
                key = str(index)
            ))
        
        if UtilHolder.add_message_flag == True:
            for text in UtilHolder.out_messages:
                output_column.controls.append(flet.Text(text))

        output_column.controls.append(flet.Text("Process done!"))
        page.update()

    def on_send_button(email: str, password: str):

        UtilHolder.out_messages.clear()

        auto_send_responses(email, password)

        if UtilHolder.add_message_flag == True:
            for text in UtilHolder.out_messages:
                output_column.controls.append(flet.Text(text))


        page.update()

    sheet_url_input = flet.TextField(label="Link da planilha")
    email_input = flet.TextField(label="Seu email")
    password_input = flet.TextField(label="A senha do email", password=True)

    button_row = flet.Row([
        flet.TextButton("Iniciar", on_click = lambda _: on_start_button(sheet_url_input.value)),
        flet.TextButton("Enviar Dados", on_click = lambda _: on_send_button(email_input.value, password_input.value))
    ])

    output_column = flet.Column(
        expand = True,
        scroll = flet.ScrollMode.ALWAYS,
        controls = [
            flet.Text("test")
        ]
    )

    output_container = flet.Container(
        width=500,
        height=300,
        border = flet.Border(
            top = flet.BorderSide(1, "black"),
            bottom = flet.BorderSide(1, "black"),
            left = flet.BorderSide(1, "black"),
            right = flet.BorderSide(1, "black")
        ),
        content = output_column
    )

    data_control = flet.ExpansionPanelList(expand=True)

    data_container = flet.Container(
        width=500,
        height=300,
        border = flet.Border(
            top = flet.BorderSide(1, "black"),
            bottom = flet.BorderSide(1, "black"),
            left = flet.BorderSide(1, "black"),
            right = flet.BorderSide(1, "black")
        ),
        content = flet.Column([data_control], expand=True, scroll=True)
    )

    page.add(
        sheet_url_input,
        email_input,
        password_input,
        button_row,
        flet.Row([
            output_container,
            data_container
        ])
    )

flet.app(main)