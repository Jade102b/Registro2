import flet as ft

AUTOR = 'Brisa Maribel V'
SISTEMA = 'SweetManager v1.0'
LIBRERIA = 'Flet (flet.dev) con Python 3'
CATEGORIAS = ('Queques', 'Tortas', 'Brownies', 'Galletas', 'Pies y Tartas', 'Postres Frios')
ELABORACIONES = ('Artesanal / Tradicional', 'Sin Azucar / Keto', 'Vegano')

def main(page: ft.Page):
    page.title = 'Sistema de Registro e Inventario para una Pasteleria / Reposteria'
    page.window.width = 920
    page.window.height = 780
    page.scroll = ft.ScrollMode.AUTO
    page.padding = ft.Padding.all(20)
    page.theme_mode = ft.ThemeMode.LIGHT

    nombre_postre = ft.TextField(label='Nombre / Descripcion del Postre', hint_text='Ej: Torta de Chocolate, Queque de Vainilla')
    ingredientes = ft.TextField(label='Ingredientes / Notas Especiales', multiline=True, min_lines=3, max_lines=5, hint_text='Detalles, alergenos, decoracion, requerimientos especiales...')

    categoria_dropdown = ft.Dropdown(label='Categoria de Postre', options=[ft.dropdown.Option(c) for c in CATEGORIAS], value=CATEGORIAS[0], width=300)
    elaboracion_radio = ft.RadioGroup(content=ft.Row([ft.Radio(value=e, label=e) for e in ELABORACIONES], spacing=15, wrap=True), value=ELABORACIONES[0])
    sin_gluten = ft.Checkbox(label='Apto para Celiacos / Sin Gluten')
    incluye_empaque = ft.Checkbox(label='Incluye Empaque de Regalo')

    stock_field = ft.TextField(label='Cantidad Producida / Stock', value='1', keyboard_type=ft.KeyboardType.NUMBER, width=200)
    stock_min_alert = ft.TextField(label='Umbral de Stock Bajo (para alerta)', value='5', keyboard_type=ft.KeyboardType.NUMBER, width=200)
    dulzor_slider = ft.Slider(label='Nivel de Dulzor / Dificultad (%)', value=50, min=0, max=100, divisions=10, width=400)
    dulzor_text = ft.Text(value='50%')

    def on_dulzor_change(e):
        dulzor_text.value = str(int(dulzor_slider.value)) + '%'
        page.update()
    dulzor_slider.on_change = on_dulzor_change

    tarjeta_resultado = ft.Container(content=ft.Column([], spacing=10, scroll=ft.ScrollMode.AUTO), padding=ft.Padding.all(15), bgcolor=ft.Colors.SURFACE, border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT), border_radius=10, visible=False)

    # Flet 1.0 mantiene los dialogos en una pila interna y solo los retira cuando
    # el cliente confirma el cierre. Sin este control, un doble clic rapido
    # apilaria dos dialogos identicos encima del otro.
    dialogo_montado = False

    def mostrar_dialogo(dialogo):
        nonlocal dialogo_montado
        if dialogo_montado:
            return
        dialogo_montado = True
        al_cerrar = dialogo.on_dismiss

        def limpiar(e):
            nonlocal dialogo_montado
            dialogo_montado = False
            if al_cerrar is not None:
                al_cerrar(e)

        dialogo.on_dismiss = limpiar
        page.show_dialog(dialogo)
        page.update()

    def cerrar_dialogo(e=None):
        page.pop_dialog()
        page.update()

    def abrir_acerca(e=None):
        # cada apertura crea una instancia nueva del dialogo
        mostrar_dialogo(ft.AlertDialog(
            modal=True,
            title=ft.Text('Acerca de / Creditos'),
            content=ft.Column([
                ft.Text('Autor / Desarrollador: ' + AUTOR),
                ft.Text('Libreria de desarrollo utilizada: ' + LIBRERIA),
                ft.Text('Nombre del Sistema: ' + SISTEMA),
                ft.Text('Version: 1.0'),
            ], tight=True, spacing=10),
            actions=[ft.TextButton('Cerrar', on_click=cerrar_dialogo)],
            actions_alignment=ft.MainAxisAlignment.END,
        ))

    async def salir(e=None):
        await page.window.close()

    async def limpiar_formulario(e=None):
        nombre_postre.value = ''
        ingredientes.value = ''
        categoria_dropdown.value = CATEGORIAS[0]
        elaboracion_radio.value = ELABORACIONES[0]
        sin_gluten.value = False
        incluye_empaque.value = False
        stock_field.value = '1'
        stock_min_alert.value = '5'
        dulzor_slider.value = 50
        dulzor_text.value = '50%'
        tarjeta_resultado.visible = False
        tarjeta_resultado.content.controls.clear()
        page.update()
        await nombre_postre.focus()


    def registrar_postre(e=None):
        try:
            stock_val = int(stock_field.value) if stock_field.value.strip() else 0
        except ValueError:
            stock_val = 0
        dulce_val = int(dulzor_slider.value)
        nombre_val = nombre_postre.value.strip() or 'Sin nombre'
        ingr_val = ingredientes.value.strip() or 'Ninguna'
        tarjeta_resultado.content.controls.clear()
        tarjeta_resultado.content.controls.extend([
            ft.Text('Ficha del Postre Registrado', weight=ft.FontWeight.BOLD, size=16),
            ft.Divider(),
            ft.Text('Nombre / Descripcion: ' + nombre_val),
            ft.Text('Categoria: ' + str(categoria_dropdown.value)),
            ft.Text('Tipo de Elaboracion: ' + str(elaboracion_radio.value)),
            ft.Text('Ingredientes / Notas Especiales: ' + ingr_val),
            ft.Text('Sin Gluten / Apto Celiacos: Si' if sin_gluten.value else 'Sin Gluten / Apto Celiacos: No'),
            ft.Text('Incluye Empaque de Regalo: Si' if incluye_empaque.value else 'Incluye Empaque de Regalo: No'),
            ft.Text('Cantidad Producida / Stock: ' + str(stock_val)),
            ft.Text('Nivel de Dulzor/Dificultad: ' + str(dulce_val) + '%'),
        ])
        tarjeta_resultado.visible = True
        page.update()

    def alerta_stock(e=None):
        try:
            stock_val = int(stock_field.value) if stock_field.value.strip() else 0
            umbral_val = int(stock_min_alert.value) if stock_min_alert.value.strip() else 0
        except ValueError:
            stock_val = 0
            umbral_val = 0
        nombre_val = nombre_postre.value.strip() or 'Producto actual'
        lineas = []
        if stock_val <= umbral_val:
            lineas = [
                ft.Icon(icon=ft.Icons.WARNING, color=ft.Colors.AMBER, size=30),
                ft.Text('Stock bajo detectado para: ' + nombre_val),
                ft.Text('Stock actual: ' + str(stock_val) + ' | Umbral configurado: ' + str(umbral_val)),
                ft.Text('Se recomienda reponer o priorizar produccion.'),
            ]
        else:
            lineas = [
                ft.Icon(icon=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=30),
                ft.Text('Stock en niveles normales para: ' + nombre_val),
                ft.Text('Stock actual: ' + str(stock_val) + ' | Umbral configurado: ' + str(umbral_val)),
                ft.Text('No hay alerta de stock en este momento.'),
            ]
        mostrar_dialogo(ft.AlertDialog(
            modal=True,
            title=ft.Text('Alerta de Stock'),
            content=ft.Column(lineas, tight=True, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[ft.TextButton('Cerrar', on_click=cerrar_dialogo)],
            actions_alignment=ft.MainAxisAlignment.END,
        ))

    page.appbar = ft.AppBar(title=ft.Text(SISTEMA), bgcolor=ft.Colors.PRIMARY_CONTAINER, actions=[ft.TextButton('Limpiar Formulario', on_click=limpiar_formulario, icon=ft.Icons.CLEANING_SERVICES), ft.TextButton('Salir', on_click=salir, icon=ft.Icons.EXIT_TO_APP), ft.IconButton(icon=ft.Icons.INFO, tooltip='Acerca de / Creditos', on_click=abrir_acerca)])


    formulario = ft.Column([
        ft.Text('Registro de Postres', weight=ft.FontWeight.BOLD, size=18),
        nombre_postre,
        ingredientes,
        ft.Row([categoria_dropdown], spacing=10),
        ft.Text('Tipo de Elaboracion:', weight=ft.FontWeight.BOLD),
        elaboracion_radio,
        ft.Row([sin_gluten, incluye_empaque], spacing=20, wrap=True),
        ft.Row([stock_field, stock_min_alert], spacing=15, wrap=True),
        ft.Row([dulzor_slider, dulzor_text], alignment=ft.MainAxisAlignment.START),
        ft.Row([
            ft.FilledButton('Registrar Postre', on_click=registrar_postre, icon=ft.Icons.ADD),
            ft.OutlinedButton('Alerta de Stock', on_click=alerta_stock, icon=ft.Icons.WARNING),
            ft.OutlinedButton('Informacion del Sistema / Autor', on_click=abrir_acerca, icon=ft.Icons.PERSON),
        ], spacing=10, wrap=True),
        ft.Divider(),
        tarjeta_resultado,
    ], spacing=15)

    page.add(formulario)

ft.run(main)
