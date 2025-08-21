from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._year = None

    def fillDDYear(self):
        years = self._model.getYears()
        for y in years:
            self._view._ddAnno.options.append(ft.dropdown.Option(y))

    def handleDDYearSelection(self, e):
        self._year = self._view._ddAnno.value

    def handleCreaGrafo(self,e):
        if self._year is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un anno!", color='red'))
            self._view.update_page()
            return
        nnodes, nedges = self._model.buildGraph(self._year)
        self._view._btnCerca.disabled = False
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nnodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nedges}"))
        best_driver = self._model.getBestDriver()
        self._view.txt_result.controls.append(ft.Text(f"Best driver is {best_driver[0].surname} with score {best_driver[1]}"))
        self._view.update_page()

    def handleCerca(self, e):
        k = self._view._txtIntK.value
        if k is None or k == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore K!", color='red'))
            return
        try:
            k = int(k)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserire un valore K numerico!", color='red'))
            return
        time = datetime.now()
        dream_team, tax = self._model.getDreamTeam(k)
        self._view.txt_result.controls.append(ft.Text(f"Il dream team è composto dai seguenti {k} piloti con tasso di sconfitta {tax}:"))
        for d in dream_team:
            self._view.txt_result.controls.append(ft.Text(d.__str__()))
        self._view.txt_result.controls.append(ft.Text(f"Tempo impiegato: {datetime.now()-time}"))
        self._view.update_page()
