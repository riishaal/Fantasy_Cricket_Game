import sys
import sqlite3
from PyQt5 import QtWidgets
from fantasy_cricket_gui import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class FantasyCricketApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # DB Connection
        self.conn = sqlite3.connect("fantasy_cricket.db")
        self.cursor = self.conn.cursor()

        # Variables
        self.total_points = 100
        self.used_points = 0
        self.selected_players = []

        # Signals
        self.ui.batRadio.toggled.connect(self.load_players)
        self.ui.bwlRadio.toggled.connect(self.load_players)
        self.ui.allRadio.toggled.connect(self.load_players)
        self.ui.wkRadio.toggled.connect(self.load_players)

        self.ui.btnAdd.clicked.connect(self.add_player)
        self.ui.btnRemove.clicked.connect(self.remove_player)
        self.ui.btnClear.clicked.connect(self.clear_team)
        self.ui.btnEvaluate.clicked.connect(self.evaluate_score)
        self.ui.btnSave.clicked.connect(self.save_team)

        self.ui.actionNewTeam.triggered.connect(self.clear_team)
        self.ui.actionOpenTeam.triggered.connect(self.open_team)
        self.ui.actionSaveTeam.triggered.connect(self.save_team)

        self.load_players()
        self.update_points()
        self.show()

    def load_players(self):
        self.ui.availableList.clear()
        category = ""
        if self.ui.batRadio.isChecked():
            category = "BAT"
        elif self.ui.bwlRadio.isChecked():
            category = "BWL"
        elif self.ui.allRadio.isChecked():
            category = "ALL"
        elif self.ui.wkRadio.isChecked():
            category = "WK"

        query = "SELECT player FROM stats WHERE ctg = ?"
        self.cursor.execute(query, (category,))
        players = self.cursor.fetchall()
        for player in players:
            if player[0] not in self.selected_players:
                self.ui.availableList.addItem(player[0])

    def add_player(self):
        selected_item = self.ui.availableList.currentItem()
        if not selected_item:
            return

        player = selected_item.text()
        if len(self.selected_players) >= 11:
            QMessageBox.warning(self, "Limit Reached", "You can only select 11 players.")
            return

        # Only one WK allowed
        self.cursor.execute("SELECT ctg FROM stats WHERE player = ?", (player,))
        category = self.cursor.fetchone()[0]
        if category == "WK":
            count_wk = sum(
                1 for p in self.selected_players if self.cursor.execute("SELECT ctg FROM stats WHERE player = ?", (p,)).fetchone()[0] == "WK"
            )
            if count_wk >= 1:
                QMessageBox.warning(self, "Limit Reached", "Only one WK is allowed.")
                return

        self.cursor.execute("SELECT value FROM stats WHERE player = ?", (player,))
        value = self.cursor.fetchone()[0]
        if self.used_points + value > self.total_points:
            QMessageBox.warning(self, "Points Exceeded", "Not enough points to add this player.")
            return

        self.selected_players.append(player)
        self.ui.selectedList.addItem(player)
        self.used_points += value
        self.update_points()
        self.load_players()

    def remove_player(self):
        selected_item = self.ui.selectedList.currentItem()
        if not selected_item:
            return
        player = selected_item.text()
        self.selected_players.remove(player)
        self.ui.selectedList.takeItem(self.ui.selectedList.row(selected_item))

        self.cursor.execute("SELECT value FROM stats WHERE player = ?", (player,))
        value = self.cursor.fetchone()[0]
        self.used_points -= value
        self.update_points()
        self.load_players()

    def update_points(self):
        self.ui.usedPoints.setText(str(round(self.used_points, 2)))
        self.ui.availPoints.setText(str(round(self.total_points - self.used_points, 2)))

    def clear_team(self):
        self.selected_players.clear()
        self.ui.selectedList.clear()
        self.used_points = 0
        self.update_points()
        self.load_players()
        self.ui.teamNameInput.clear()

    def save_team(self):
        name = self.ui.teamNameInput.text()
        if not name:
            QMessageBox.warning(self, "Missing Info", "Please enter a team name.")
            return
        if len(self.selected_players) != 11:
            QMessageBox.warning(self, "Invalid Team", "A team must have exactly 11 players.")
            return
        players = ", ".join(self.selected_players)
        self.cursor.execute("INSERT OR REPLACE INTO teams VALUES (?, ?, ?)", (name, players, self.used_points))
        self.conn.commit()
        QMessageBox.information(self, "Team Saved", f"Team '{name}' saved successfully.")

    def open_team(self):
        self.cursor.execute("SELECT name FROM teams")
        teams = [row[0] for row in self.cursor.fetchall()]
        if not teams:
            QMessageBox.information(self, "No Teams", "No teams found in the database.")
            return
        team, ok = QtWidgets.QInputDialog.getItem(self, "Open Team", "Select a team:", teams, 0, False)
        if ok and team:
            self.cursor.execute("SELECT players, value FROM teams WHERE name = ?", (team,))
            data = self.cursor.fetchone()
            self.clear_team()
            self.ui.teamNameInput.setText(team)
            self.selected_players = data[0].split(", ")
            self.used_points = data[1]
            self.update_points()
            self.ui.selectedList.addItems(self.selected_players)
            self.load_players()

    def evaluate_score(self):
        if len(self.selected_players) != 11:
            QMessageBox.warning(self, "Invalid Team", "Team must have exactly 11 players.")
            return

        match_ids = self.cursor.execute("SELECT DISTINCT match_id FROM match").fetchall()
        if not match_ids:
            QMessageBox.warning(self, "No Matches", "No match data found.")
            return
        match_ids = [str(row[0]) for row in match_ids]
        match_id, ok = QtWidgets.QInputDialog.getItem(self, "Select Match", "Choose match ID:", match_ids, 0, False)
        if not ok:
            return

        score = 0
        for player in self.selected_players:
            self.cursor.execute("SELECT * FROM match WHERE match_id = ? AND player = ?", (match_id, player))
            stats = self.cursor.fetchone()
            if not stats:
                continue
            # Scoring rules
            scored, faced, fours, sixes = stats[2:6]
            bowled, maiden, given, wkts = stats[6:10]
            catches, stumping, ro = stats[10:13]

            score += scored // 2
            if scored >= 50:
                score += 5
            if scored >= 100:
                score += 10
            if faced > 0:
                sr = (scored / faced) * 100
                if 80 <= sr <= 100:
                    score += 2
                elif sr > 100:
                    score += 4

            score += wkts * 10
            if wkts >= 3:
                score += 5
            if wkts >= 5:
                score += 10

            if bowled > 0:
                econ = (given / bowled) * 6
                if 3.5 <= econ <= 4.5:
                    score += 4
                elif 2 <= econ < 3.5:
                    score += 7
                elif econ < 2:
                    score += 10

            score += catches * 10
            score += stumping * 10
            score += ro * 10

        QMessageBox.information(self, "Team Score", f"Total Score for match {match_id}: {score}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FantasyCricketApp()
    sys.exit(app.exec_())
