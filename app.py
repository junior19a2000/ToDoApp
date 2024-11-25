import flet as ft
import pandas as pd
import gspread
import datetime

def main(page: ft.Page):
    activity_to_delete = None

    def update_bar():
        progressbar1.value = len(done_activities.controls) / len(new_activities.controls + done_activities.controls) if len(new_activities.controls + done_activities.controls) != 0 else 0.0

    def create_sheet(e):
        gs = gspread.service_account(filename = r"D:\Programs\Python\Flet\credentials.json")
        sheets = gs.open_by_key("1XmL9FLRSQAqmmvZweBPLBG3Sk_Bh73VHT1UKTHwd74s")
        sheets_names = [sheet.title for sheet in sheets.worksheets()]

        matrix1 = []
        for i in new_activities.controls:
            matrix1.append(i.controls[1].value)
        matrix1 = pd.DataFrame(matrix1)
        matrix2 = []
        for i in done_activities.controls:
            matrix2.append(i.controls[1].value)
        matrix2 = pd.DataFrame(matrix2)
        matrix3 = pd.concat([matrix1, matrix2], axis = 1, ignore_index = True).fillna("")
        matrix3.columns = ['Actividades pendientes', 'Actividades realizadas']

        date = str(datetime.datetime.now()).split(" ")[0]
        if date not in sheets_names:
            sheet = sheets.add_worksheet(title = date, rows = "50", cols = "20")
            sheet.update([matrix3.columns.values.tolist()] + matrix3.values.tolist())
        else:
            sheet = sheets.worksheet(date)
            sheet.update([matrix3.columns.values.tolist()] + matrix3.values.tolist())
            
    def add_activity(e):
        activity = ft.Row(
            controls = [ft.Checkbox(label = "", on_change = done_activity),
                        ft.TextField(label = "", value = textfield1.value, expand = True, disabled = True),
                        ft.IconButton(icon = ft.icons.CREATE_OUTLINED, on_click = edit_activity),
                        ft.IconButton(icon = ft.icons.DELETE_OUTLINE, on_click = show_dialog),
            ],
            spacing = 10,
        )
        new_activities.controls.append(activity)
        textfield1.value = ""
        update_bar()
        page.update()

    def done_activity(e):
        for activity in new_activities.controls[:]:
            if activity.controls[0].value:  
                new_activities.controls.remove(activity)
                done_activities.controls.append(activity)
                break
        for activity in done_activities.controls[:]:
            if not activity.controls[0].value:  
                done_activities.controls.remove(activity)
                new_activities.controls.append(activity)
                break
        update_bar()
        page.update()

    def edit_activity(e):
        for activity in new_activities.controls[:]:
            if e.control in activity.controls:
                if activity.controls[1].disabled:
                    activity.controls[1].disabled = False
                    activity.controls[2].icon = ft.icons.SPELLCHECK
                else:
                    activity.controls[1].disabled = True
                    activity.controls[2].icon = ft.icons.CREATE_OUTLINED
                break
        for activity in done_activities.controls[:]:
            if e.control in activity.controls:
                if activity.controls[1].disabled:
                    activity.controls[1].disabled = False
                    activity.controls[2].icon = ft.icons.SPELLCHECK
                else:
                    activity.controls[1].disabled = True
                    activity.controls[2].icon = ft.icons.CREATE_OUTLINED
                break
        page.update()

    def delete_activity(e):
        nonlocal activity_to_delete
        if activity_to_delete in new_activities.controls:
            new_activities.controls.remove(activity_to_delete)
        else:
            done_activities.controls.remove(activity_to_delete)
        page.close(alertdialog1)
        update_bar()
        page.update()

    def no_delete_activity(e):
        page.close(alertdialog1)

    def show_dialog(e):
        nonlocal activity_to_delete
        for activity in new_activities.controls + done_activities.controls:
            if e.control in activity.controls:
                activity_to_delete = activity
                break
        page.open(alertdialog1)
        
    page.title = "Samantinita v1.0.0"
    page.appbar = ft.AppBar(
        leading = ft.IconButton(icon = ft.icons.MENU, on_click = lambda e: page.open(drawer)),
        leading_width = 40,
        title = ft.Text("Bonito día !"),
        actions = [
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
        ],
    )
    textfield1 = ft.TextField(hint_text = "¿Qué quieres hacer hoy bebé?", expand = True)
    progressbar1 = ft.ProgressBar(value = 0.0, bar_height = 50, border_radius = ft.border_radius.all(30))
    new_activities = ft.Column()
    done_activities = ft.Column()
    column1 = ft.Column(
        controls = [
            ft.Row(
                controls = [textfield1, ft.FloatingActionButton(icon = ft.icons.ADD, on_click = add_activity)],
                spacing = 20,
                expand = True,
            ),
            progressbar1,
            ft.Tabs(
                selected_index = 0,
                animation_duration = 250,
                tabs = [
                    ft.Tab(
                        text = "Actividades por hacer",
                        content = new_activities,
                    ),
                    ft.Tab(
                        text = "Actividades ya realizadas",
                        content = done_activities,
                    ),
                ],
                expand = 0,
            ),
        ]
    )
    page.add(column1)

    alertdialog1 = ft.AlertDialog(
        modal = True,
        title = ft.Text("😱"),
        content = ft.Text("¿Segura de que quieres eliminar esta actividad?"),
        actions = [
            ft.TextButton("Si", on_click = delete_activity),
            ft.TextButton("No", on_click = no_delete_activity),
        ],
        actions_alignment = ft.MainAxisAlignment.END,
    )

    drawer = ft.NavigationDrawer(
        controls = [
            ft.FilledButton("Registrar información", icon = "add", on_click = create_sheet),
        ]
    )

ft.app(main)